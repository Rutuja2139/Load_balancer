# Secure TCP Load Balancer

This project implements a "secure multi-threaded TCP load balancer" with support for  
Round Robin, Random, and Weighted Round Robin** scheduling algorithms, along with  
end-to-end encryption using RSA (2048-bit).

It demonstrates how a traffic orchestrator can securely distribute client requests to multiple backend servers.



# Features

- Secure communication using *RSA-2048 with PKCS1_OAEP*
- Supports three load balancing algorithms:
  - Round Robin  
  - Random  
  - Weighted Round Robin  
- Multi-threaded backend servers
- Separate key pairs for:
  - Client  
  - Load Balancer (Orchestrator)  
  - Each Backend Server
 
    
- Client encrypts message using *Load Balancer public key*
- Load Balancer decrypts using its *private key*
- Load Balancer forwards encrypted data to selected backend server
- Backend server decrypts using its *private key*
- Response is encrypted back to Load Balancer and then to Client



# Requirements

- Python 3.x  
- pycryptodome  

Install dependency:

```bash
pip install pycryptodome


--Keys are generated using:

=>python generate_keys.py
this generates RSA-2048 key pairs for:

Load Balancer

Client

Server 1

Server 2

Server 3

# How to Run
Step 1: Start Backend Servers

Open three terminals:

python server1.py
python server2.py
python server3.py

Step 2: Start Traffic Orchestrator
python traffic_orchestrator.py


Select algorithm:

1. Round Robin
2. Random
3. Weighted Round Robin

Step 3: Start Client
python client.py


Enter a message and observe encrypted communication and server selection.

- Load Balancing Algorithms

Round Robin: Sequential distribution across servers

Random: Random server selection

Weighted Round Robin: Servers with higher weight receive more requests

🔒 Security

RSA-2048 public key encryption

PKCS1_OAEP padding for secure encryption

Separate key pairs for each entity

End-to-end encrypted communication

