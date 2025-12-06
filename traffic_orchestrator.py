

import socket
import random
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

servers = [("localhost", 9001, 3), ("localhost", 9002, 2), ("localhost", 9003, 1)]
current = 0
lock = threading.Lock()


with open("lb_private.pem", "rb") as f:
    lb_private_key = RSA.import_key(f.read())
lb_cipher_private = PKCS1_OAEP.new(lb_private_key)

with open("client_public.pem", "rb") as f:
    client_public_key = RSA.import_key(f.read())
client_cipher_public = PKCS1_OAEP.new(client_public_key)

server_public_keys = []
for i in range(1, 4):
    with open(f"server{i}_public.pem", "rb") as f:
        key = RSA.import_key(f.read())
        server_public_keys.append(PKCS1_OAEP.new(key))


print("Select Load Balancing Algorithm:")
print("1. Round Robin")
print("2. Random")
print("3. Weighted Round Robin")

choice = input("Enter choice (1/2/3): ").strip()

if choice == "1":
    algorithm = "round_robin"
elif choice == "2":
    algorithm = "random"
elif choice == "3":
    algorithm = "weighted"
else:
    print("Invalid choice, defaulting to Round Robin.")
    algorithm = "round_robin"

print(f"Using algorithm: {algorithm}\n")


def choose_server():
    global current

    if algorithm == "round_robin":
        with lock:
            server = servers[current][:2]
            current = (current + 1) % len(servers)
        print(f"[Round Robin] Selected: {server}")

    elif algorithm == "random":
        server = random.choice(servers)[:2]
        print(f"[Random] Selected: {server}")

    elif algorithm == "weighted":
        with lock:
            weighted_servers = []
            for s in servers:
                addr, port, weight = s
                weighted_servers.extend([(addr, port)] * weight)
            server = weighted_servers[current]
            current = (current + 1) % len(weighted_servers)
        print(f"[Weighted] Selected: {server}")

    return server


def handle_client(conn, addr):
    print(f"Client connected from: {addr}")

    try:
        
        encrypted_data = conn.recv(256)
        print("Encrypted data received from client:", encrypted_data)

        data = lb_cipher_private.decrypt(encrypted_data).decode()
        print(f"Decrypted from client: {data}")

        
        server = choose_server()
        print(f"Selected backend server: {server}")

        server_index = [s[:2] for s in servers].index(server)
        server_cipher = server_public_keys[server_index]

       
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect(server)
        encrypted_for_server = server_cipher.encrypt(data.encode())
        backend_socket.send(encrypted_for_server)
        print(f"Sent encrypted data to backend: {server}")

        
        encrypted_response = backend_socket.recv(256)
        response = lb_cipher_private.decrypt(encrypted_response).decode()
        print(f"Decrypted from server: {response}")

        
        encrypted_for_client = client_cipher_public.encrypt(response.encode())
        conn.send(encrypted_for_client)
        print("Response sent back to client (encrypted).")

    except Exception as e:
        print("Error while handling client:", e)

    finally:
        backend_socket.close()
        conn.close()


orchestrator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orchestrator_socket.bind(("localhost", 8000))
orchestrator_socket.listen(5)

print("Traffic Orchestrator running on port 8000...")

while True:
    conn, addr = orchestrator_socket.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

