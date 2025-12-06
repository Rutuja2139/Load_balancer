import socket, threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

with open("server1_private.pem","rb") as f:
    priv = RSA.import_key(f.read())
decipher = PKCS1_OAEP.new(priv)

with open("lb_public.pem","rb") as f:
    lb_pub = RSA.import_key(f.read())
cipher_lb = PKCS1_OAEP.new(lb_pub)

def handle_client(conn, addr):
    try:
        data = conn.recv(256)
        print("Encrypted data received from orchestrator:",data)

        msg = decipher.decrypt(data).decode()
        print("Decrypted message from orchestrator:", msg)

        resp = "Response from Server 1"
        enc_resp = cipher_lb.encrypt(resp.encode())
        conn.send(enc_resp)
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost",9001))
s.listen(5)
print("Server 1 running on port 9001...")

while True:
    c,a = s.accept()
    threading.Thread(target=handle_client, args=(c,a)).start()

