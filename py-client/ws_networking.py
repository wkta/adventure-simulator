import threading
import websocket
from core.events import EngineEvTypes, EvManager, EvListener

client_socket = None
receiver_thread = None


class NetwPusher(EvListener):
    def on_netw_send(self, ev):
        send_data((ev.evt+'#"'+ev.serial+'"').encode())  # after the sym #: you need to find real json format!!!

    def on_exit_network(self, ev):
        stop_network()

    def turn_on(self):
        super().turn_on()
        start_client()


def on_message(ws, message):
    ev_manager = EvManager.instance()
    serial = message
    print(f'Received shared variable update: {serial}')
    ev_manager.post(EngineEvTypes.NetwReceive, serial=serial)


def on_error(ws, error):
    print(f"WebSocket error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")


def on_open(ws):
    global client_socket
    client_socket = ws
    print("WebSocket connection opened")


def receive_updates():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8080/artificial.js",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()


def start_client():
    global receiver_thread
    receiver_thread = threading.Thread(target=receive_updates)
    receiver_thread.start()


def stop_network():
    global receiver_thread, client_socket
    if receiver_thread:
        receiver_thread.join()
    if client_socket:
        client_socket.close()


def send_data(x):
    global client_socket
    if client_socket:
        client_socket.send(x)
