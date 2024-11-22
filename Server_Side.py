import socket
import os
from time import time
from network_analysis import NetworkAnalysis

HOST = 'localhost'
PORT = 3300
BUFFER_SIZE = 5000 * 1024
BASE_DIR = './server_files'


network_analysis = NetworkAnalysis()  # NA
network_analysis.initialize()  # NA

def handle_upload(conn, data):
    _, file_name, file_size = data.split()
    file_size = int(file_size)
    conn.sendall("READY".encode('utf-8'))
    start_time = time()
    with open(os.path.join(BASE_DIR, file_name), 'wb') as file:
        received = 0
        while received < file_size:
            chunk = conn.recv(BUFFER_SIZE)
            file.write(chunk)
            received += len(chunk)
    transfer_time = time() - start_time
    network_analysis.logTransfer("UPLOAD", file_name, file_size, transfer_time)
    print(f"File {file_name} uploaded successfully.")
    network_analysis.displaySummary() #NA



def handle_download(conn, data):
    _, file_name = data.split()
    file_path = os.path.join(BASE_DIR, file_name)
    if not os.path.exists(file_path):
        conn.sendall(f"ERROR File {file_name} not found.".encode('utf-8'))
        return
    
    file_size = os.path.getsize(file_path)
    conn.sendall(f"{file_size}".encode('utf-8'))
    start_time = time()
    with open(file_path, 'rb') as file:
        while chunk := file.read(BUFFER_SIZE):
            conn.sendall(chunk)
    transfer_time = time() - start_time
    network_analysis.logTransfer("DOWNLOAD", file_name, file_size, transfer_time)
    print(f"File {file_name} downloaded successfully.")
    network_analysis.displaySummary() #NA


def handle_delete(conn, data):
    _, file_name = data.split()
    file_path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        network_analysis.logTransfer("DELETE", file_name, 0, 0)  # Log the delete action
        conn.sendall(f"File {file_name} deleted successfully.".encode('utf-8'))
    else:
        conn.sendall(f"ERROR File {file_name} not found.".encode('utf-8'))
    network_analysis.displaySummary() #NA



def handle_list_directory(conn):
    files = os.listdir(BASE_DIR)
    conn.sendall("\n".join(files).encode('utf-8'))

    network_analysis.logTransfer("LIST_DIR", "N/A", 0, 0) #NA
    network_analysis.displaySummary() #NA



def handle_subfolder(conn, data):
    _, action, path = data.split()
    full_path = os.path.join(BASE_DIR, path)
    if action == 'create':
        os.makedirs(full_path, exist_ok=True)
        conn.sendall(f"Subfolder {path} created.".encode('utf-8'))
        network_analysis.logTransfer("SUBFOLDER_CREATE", path, 0, 0)
    elif action == 'delete':
        if os.path.isdir(full_path):
            os.rmdir(full_path)
            conn.sendall(f"Subfolder {path} deleted.".encode('utf-8'))
            network_analysis.logTransfer("SUBFOLDER_DELETE", path, 0, 0) #NA
        else:
            conn.sendall(f"ERROR Subfolder {path} not found.".encode('utf-8'))

    network_analysis.displaySummary()



def handle_client(conn):
    try:
        while True:
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break
            if data.startswith("UPLOAD"):
                handle_upload(conn, data)
            elif data.startswith("DOWNLOAD"):
                handle_download(conn, data)
            elif data.startswith("DELETE"):
                handle_delete(conn, data)
            elif data == "DIR":
                handle_list_directory(conn)
            elif data.startswith("SUBFOLDER"):
                handle_subfolder(conn, data)
            else:
                conn.sendall("ERROR Unknown command.".encode('utf-8'))
    except Exception as e:
        print(f"Error with client: {e}")
    finally:
        conn.close()
        
        network_analysis.save()  # NA


def main():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}...")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            handle_client(conn)
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        network_analysis.save() #NA
        network_analysis.displaySummary()   #NA
        server_socket.close() #NA


if __name__ == "__main__":
    main()
