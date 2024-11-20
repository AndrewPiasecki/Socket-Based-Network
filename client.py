# THIS FILE IS FOR TESTING ONLY!!!

import socket
import os
import time

HOST = 'localhost'  
PORT = 3300
BUFFER_SIZE = 1024


def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print("Connected to the server.")
        return client_socket
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        return None

def send_message(client_socket, message):
    try:
        client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")

def receive_message(client_socket):
    try:
        data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        return data
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

def upload_file(client_socket, file_path):
    if not os.path.exists(file_path):
        print("File does not exist.")
        return
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    send_message(client_socket, f"UPLOAD {file_name} {file_size}")
    response = receive_message(client_socket)
    if response != "READY":
        print(f"Server response: {response}")
        return
    with open(file_path, 'rb') as file:
        while chunk := file.read(BUFFER_SIZE):
            client_socket.sendall(chunk)
    print("File uploaded successfully.")

def download_file(client_socket, file_name):
    # Send download request to the server
    send_message(client_socket, f"DOWNLOAD {file_name}")
    
    # Receive the server's response (either the file size or an error)
    response = receive_message(client_socket)
    
    if response.startswith("ERROR"):
        # If the response is an error, print and return
        print(f"Server response: {response}")
        return
    
    # At this point, we expect the response to be the file size (as a string)
    try:
        file_size = int(response)  # Try to parse the file size
    except ValueError:
        # If the response is not a valid number, print the error and return
        print(f"Unexpected server response: {response}")
        return
    
    # Now, proceed with downloading the file
    with open(file_name, 'wb') as file:
        received = 0
        while received < file_size:
            chunk = client_socket.recv(BUFFER_SIZE)
            if not chunk:
                break  # If no data is received, exit
            file.write(chunk)
            received += len(chunk)
    
    print(f"File {file_name} downloaded successfully.")

def delete_file(client_socket, file_name):
    send_message(client_socket, f"DELETE {file_name}")
    response = receive_message(client_socket)
    print(f"Server response: {response}")

#DIR
def list_directory(client_socket):
    send_message(client_socket, "DIR")
    response = receive_message(client_socket)
    print(f"Files and directories:\n{response}")

#create or delete a subfolder
def manage_subfolder(client_socket, action, path):
    send_message(client_socket, f"SUBFOLDER {action} {path}")
    response = receive_message(client_socket)
    print(f"Server response: {response}")

def main():
    print("File Sharing Client")
    while True:
        print("\nOptions:")
        print("1. Upload a file")
        print("2. Download a file")
        print("3. Delete a file")
        print("4. List directory")
        print("5. Create/Delete subfolder")
        print("6. Quit")
        choice = input("Enter your choice: ")

        if choice == "6":
            print("Exiting")
            break

        client_socket = connect_to_server()
        if not client_socket:
            continue
          # skips if connection fails

        if choice == "1": #upload
            file_path = input("Enter the file path to upload: ")
            upload_file(client_socket, file_path)
          
        elif choice == "2": #download
            file_name = input("Enter the file name to download: ")
            download_file(client_socket, file_name)
          
        elif choice == "3": #delete
            file_name = input("Enter the file name to delete: ")
            delete_file(client_socket, file_name)
          
        elif choice == "4": #list
            list_directory(client_socket)
          
        elif choice == "5": #create/delete subfolder
            action = input("Enter 'create' or 'delete': ")
            path = input("Enter the path/directory: ")
            manage_subfolder(client_socket, action, path)
          
        else: #oopsies
            print("Invalid choice. Please try again.")
        
        client_socket.close()

if __name__ == "__main__":
    main()