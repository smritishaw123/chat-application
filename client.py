import socket

HOST = 'localhost'  # The server's hostname or IP address
PORT = 65432        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    username = input("Enter your username: ")
    print(f"Connected to server as {username}")

    while True:
        message = input(f"{username}: ")
        s.sendall(f"{username}: {message}".encode('utf-8'))
        if message.lower() == "/quit":
            break

print("Closing connection...")


