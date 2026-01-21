
import sys
sys.path.insert(0, r"C:\Users\win 10\AppData\Roaming\Python\Python313\site-packages")

import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

with open("client_private.pem", "rb") as f:
    client_private_key = RSA.import_key(f.read())
with open("lb_public.pem", "rb") as f:
    lb_public_key = RSA.import_key(f.read())

encrypt_cipher = PKCS1_OAEP.new(lb_public_key)
decrypt_cipher = PKCS1_OAEP.new(client_private_key)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8000))

message = input("Enter message for server: ")
encrypted_message = encrypt_cipher.encrypt(message.encode())
print("Encrypted message being sent:", encrypted_message)

client_socket.send(encrypted_message)

encrypted_response = client_socket.recv(4096)
response = decrypt_cipher.decrypt(encrypted_response)
print("Response from the server:", response.decode())

client_socket.close()
