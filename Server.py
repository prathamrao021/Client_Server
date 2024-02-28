import socket
import os
import sys 

def send_file_content(client_socket, filename):
    """
    Sends the content of a file to the client.

    Args:
        client_socket (socket.socket): The client socket.
        filename (str): The name of the file to send.
    """
    with open(filename, 'rb') as file:
        chunk = file.read(1024)
        while chunk:
            client_socket.send(chunk)
            chunk = file.read(1024)
    client_socket.send(b'END_OF_FILE')  # Signal the end of the file

def receive_file_content(client_socket, filename):
    """
    Receives the content of a file from the client.

    Args:
        client_socket (socket.socket): The client socket.
        filename (str): The name of the file to receive.
    """
    with open(filename, 'wb') as file:
        while True:
            chunk = client_socket.recv(1024)
            if chunk.endswith(b'END_OF_FILE'):
                chunk = chunk[:-len(b'END_OF_FILE')]
                file.write(chunk)
                break
            file.write(chunk)

def handle_client_connection(client_socket, server_socket):
    """
    Handles the client connection.

    Args:
        client_socket (socket.socket): The client socket.
        server_socket (socket.socket): The server socket.
    """
    try:
        while True:
            command = client_socket.recv(1024).decode()
            # print(command)
            
            if not command:
                break  # Connection closed by the client

            if command == 'exit':
                # print("fdvsdfv")
                break

            elif command.startswith('get'):
                _, filename = command.split()
                if os.path.isfile(filename):
                    client_socket.send('BEGIN'.encode())
                    send_file_content(client_socket, filename)
                    print("File sent successfully.")
                else:
                    client_socket.send(b'File not found')

            elif command.startswith('upload'):
                _, filename = command.split()
                receive_file_content(client_socket, 'new' + filename)
                print("File received successfully.")

    finally:
        server_socket.close()
        client_socket.close()

def start_server():
    """
    Starts the server.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 5160))
        server_socket.listen()
        print("Server is listening for incoming connections....")
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")
        handle_client_connection(client_socket, server_socket)
        print("Connection has been closed.")

if __name__ == '__main__':
    """
    Entry point of the script.
    """
    try:
        port = sys.argv[1]
    except:
        port = 5160
    start_server()
