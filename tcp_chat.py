import socket
import sys

def start_server(host='127.0.0.1', port=65432):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()
            print(f"Server is listening on {host}:{port}")

            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    try:
                        data = conn.recv(1024).decode('utf-8')
                        if not data or data.lower() == 'exit':
                            print("Connection closed by client.")
                            break
                        print(f"Client: {data}")
                        response = input("You: ")
                        conn.sendall(response.encode('utf-8'))
                        if response.lower() == 'exit':
                            print("Closing connection.")
                            break
                    except Exception as e:
                        print(f"Error during communication: {e}")
                        break
    except Exception as e:
        print(f"Server error: {e}")

def start_client(host='127.0.0.1', port=65432):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            while True:
                try:
                    message = input("You: ")
                    client_socket.sendall(message.encode('utf-8'))
                    if message.lower() == 'exit':
                        print("Closing connection.")
                        break
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data or data.lower() == 'exit':
                        print("Connection closed by server.")
                        break
                    print(f"Server: {data}")
                except Exception as e:
                    print(f"Error during communication: {e}")
                    break
    except Exception as e:
        print(f"Client error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py [server|client] [host] [port]")
        sys.exit(1)

    mode = sys.argv[1].lower()
    host = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 65432

    if mode == 'server':
        start_server(host, port)
    elif mode == 'client':
        start_client(host, port)
    else:
        print("Invalid mode. Use 'server' or 'client'.")
        sys.exit(1)