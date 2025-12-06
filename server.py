#import socket
#create a socket object
#bind it to host and port 
#listen for incoming connections
#accept a connection and recieve message
#send response back to client
#close connection
import socket
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("localhost",9999))

server_socket.listen(1)

conn,addr=server_socket.accept()

print("connected with:",addr)

data=conn.recv(1024).decode()

print("recieved",data)

conn.send("message recieved!".encode())

conn.close()

