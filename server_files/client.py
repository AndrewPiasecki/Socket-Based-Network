import socket
import os

# Client Configuration
SERVER_HOST = 'localhost'  # or '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 1024

# Establish connection to server
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    return client_socket

# Authenticate with server
def authenticate(client_socket):
    username = input("Enter username: ")
    password = input("Enter password: ")

    client_socket.send(username.encode())
    client_socket.send(password.encode())

    response = client_socket.recv(1024).decode()
    print(response)

# Upload file to server
def upload_file(client_socket):
    filename = input("Enter the filename to upload: ")
    if not os.path.exists(filename):
        print("File does not exist!")
        return

    client_socket.send(b"upload")
    client_socket.send(filename.encode())
    
    with open(filename, 'rb') as f:
        while (chunk := f.read(BUFFER_SIZE)):
            client_socket.send(chunk)
    
    print("File uploaded successfully!")

# Download file from server
def download_file(client_socket):
    filename = input("Enter the filename to download: ")
    client_socket.send(b"download")
    client_socket.send(filename.encode())

    response = client_socket.recv(1024).decode()
    print(response)

    if response == "Sending the file...":
        with open(f"downloaded_{filename}", 'wb') as f:
            while (chunk := client_socket.recv(BUFFER_SIZE)):
                f.write(chunk)
        
        print(f"File {filename} downloaded successfully!")

# Delete file on server
def delete_file(client_socket):
    filename = input("Enter the filename to delete: ")
    if not os.path.exists(filename):
        print("File does not exist.")
        return
    
    client_socket.send(b"delete")
    client_socket.send(filename.encode())

    with open(filename, 'rb') as f:
        while (chunk := f.read(BUFFER_SIZE)):
            client_socket.send(chunk)

    response = client_socket.recv(1024).decode()
    print(response)

# Show files on server
def show_files(client_socket):
    client_socket.send(b"dir")
    response = client_socket.recv(1024).decode()
    print(response)

# Main client loop
def main():
    client_socket = connect_to_server()

    # Authenticate
    authenticate(client_socket)

    while True:
        command = input("").strip().lower()
        
        if command == 'upload':
            upload_file(client_socket)
        elif command == 'download':
            download_file(client_socket)
        elif command == 'delete':
            delete_file(client_socket)
        elif command == 'dir':
            show_files(client_socket)
        elif command == 'exit':
            client_socket.send(b"exit")
            client_socket.close()
            print("Goodbye!")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()uploadclient.pyimport socket
import os

# Client Configuration
SERVER_HOST = 'localhost'  # or '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 1024

# Establish connection to server
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    return client_socket

# Authenticate with server
def authenticate(client_socket):
    username = input("Enter username: ")
    password = input("Enter password: ")

    client_socket.send(username.encode())
    client_socket.send(password.encode())

    response = client_socket.recv(1024).decode()
    print(response)

# Upload file to server
def upload_file(client_socket):
    filename = input("Enter the filename to upload: ")
    if not os.path.exists(filename):
        print("File does not exist!")
        return

    client_socket.send(b"upload")
    client_socket.send(filename.encode())
    
    with open(filename, 'rb') as f:
        while (chunk := f.read(BUFFER_SIZE)):
            client_socket.send(chunk)
    
    print("File uploaded successfully!")

# Download file from server
def download_file(client_socket):
    filename = input("Enter the filename to download: ")
    client_socket.send(b"download")
    client_socket.send(filename.encode())

    response = client_socket.recv(1024).decode()
    print(response)

    if response == "Sending the file...":
        with open(f"downloaded_{filename}", 'wb') as f:
            while (chunk := client_socket.recv(BUFFER_SIZE)):
                f.write(chunk)
        
        print(f"File {filename} downloaded successfully!")

# Delete file on server
def delete_file(client_socket):
    filename = input("Enter the filename to delete: ")
    if not os.path.exists(filename):
        print("File does not exist.")
        return
    
    client_socket.send(b"delete")
    client_socket.send(filename.encode())

    with open(filename, 'rb') as f:
        while (chunk := f.read(BUFFER_SIZE)):
            client_socket.send(chunk)

    response = client_socket.recv(1024).decode()
    print(response)

# Show files on server
def show_files(client_socket):
    client_socket.send(b"dir")
    response = client_socket.recv(1024).decode()
    print(response)

# Main client loop
def main():
    client_socket = connect_to_server()

    # Authenticate
    authenticate(client_socket)

    while True:
        command = input("").strip().lower()
        
        if command == 'upload':
            upload_file(client_socket)
        elif command == 'download':
            download_file(client_socket)
        elif command == 'delete':
            delete_file(client_socket)
        elif command == 'dir':
            show_files(client_socket)
        elif command == 'exit':
            client_socket.send(b"exit")
            client_socket.close()
            print("Goodbye!")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()dirdir