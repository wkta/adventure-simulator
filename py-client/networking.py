import socket
import threading
from core.events import EngineEvTypes, EvManager


client_socket = None
receiver_thread = None


def receive_updates(clisocket):
    ev_manager = EvManager.instance()
    while True:
        data = clisocket.recv(1024)
        if not data:
            break
        serial = data.decode()
        print(f'Received shared variable update: {serial}')

        #  step before replacing local game model
        ev_manager.post(EngineEvTypes.NetwReceive, serial=serial)


def start_client():
    global client_socket, receiver_thread
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    receiver_thread = threading.Thread(target=receive_updates, args=(client_socket,))
    receiver_thread.start()


def stop_network():
    global receiver_thread, client_socket
    if receiver_thread:
        receiver_thread.join()
    if client_socket:
        client_socket.close()


def send_data(x):
    global client_socket
    client_socket.sendall(x)
