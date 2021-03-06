import getpass
import socket
import threading
import urllib.request
from time import sleep
from threading import Event

number_of_connections = 0
ready_to_accept = Event()


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 53))
    return s.getsockname()[0]


def handle_msg_from_client(conn):
    while True:
        msg_from_client = conn.recv(1024).decode()
        if msg_from_client:
            print("\r" + msg_from_client)
            print("\ryou: ", end='')


def make_connection_with_client(sock_conn):
    global number_of_connections
    conn, addr = sock_conn.accept()
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
    external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
    print("External IP is: " + external_ip)
    connection.bind((get_host_ip(), 5545))
    print("Waiting for new connections to the server!")
    connection.listen()
    while True:
        if number_of_connections >= 2:
            print("Not accepting anymore connections!")
            ready_to_accept.wait()
            print("Ready to accept more connections!")
        else:
            threading.Thread(target=make_connection_with_client, args=(connection,)).start()
            try:
                while True:
                    sleep(0.5)
            except KeyboardInterrupt:
                exit(0)


