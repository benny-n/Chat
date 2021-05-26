import getpass
import socket
import threading
from threading import Event

number_of_connections = 0
ready_to_accept = Event()


def handle_msg_from_client(conn):
    while True:
        msg_from_client = conn.recv(1024).decode()
        if msg_from_client:
            print("\r" + msg_from_client)
            print("\ryou: ", end='')


def make_connection_with_client(conn, addr):
    global number_of_connections
    number_of_connections += 1
    if number_of_connections == 2:
        ready_to_accept.clear()
    with conn:
        print('Connected by', addr)
        while True:
            threading.Thread(target=handle_msg_from_client, args=(conn,)).start()
            input_data = input("you: ")
            if input_data:
                msg_to_send = getpass.getuser() + ": " + input_data
                conn.send(msg_to_send.encode())
            else:
                break
        print('Connection with ' + str(addr) + ' ended')
    number_of_connections -= 1
    if number_of_connections < 2:
        ready_to_accept.set()


with socket.socket() as connection:
    print("Host IP is: " + str((socket.gethostbyname(socket.gethostname()))))
    connection.bind((socket.gethostbyname(socket.gethostname()), 5545))
    print("Waiting for new connections to the server!")
    connection.listen()
    while True:
        if number_of_connections >= 2:
            print("Not accepting anymore connections!")
            ready_to_accept.wait()
            print("Ready to accept more connections!")
        else:
            threading.Thread(target=make_connection_with_client, args=connection.accept()).start()


