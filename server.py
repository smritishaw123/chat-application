import socket
import threading

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432      

client_list = []
client_lock = threading.Lock()


def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                broadcast(data, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break


def broadcast(message, sender):
    with client_lock:
        for client in client_list:
            if client != sender:
                try:
                    client.sendall(message.encode('utf-8'))
                except:

                    remove_client(client)


def remove_client(client_socket):
    with client_lock:
        client_list.remove(client_socket)
        client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with client_lock:
            client_list.append(conn)
        print(f"Connected by {addr}")
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()