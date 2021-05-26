import getpass
import socket
import threading


def handle_reply_from_server(conn):
    while True:
        msg_from_server = conn.recv(1024).decode()
        if msg_from_server:
            print("\r" + msg_from_server)
            print("\ryou: ", end='')


with socket.socket() as connection:
    input_server_ip = input("Enter a server IP address to connect to: ")
    connection.connect((input_server_ip, 5545))
    while True:
        threading.Thread(target=handle_reply_from_server, args=(connection,)).start()
        input_data = input("you: ")
        if input_data:
            msg_to_send = getpass.getuser() + ": " + input_data
            connection.send(msg_to_send.encode())
        else:
            break
    print("Connection lost.")
