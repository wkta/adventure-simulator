import sys
sys.path.append('..')
from Mediator import Mediator


class ServerMediator(Mediator):
    def __init__(self, network_layer):
        super().__init__()
        self.ident = self.gen_id()
        self.network_layer = network_layer
        network_layer.register_mediator(self)

    def server_side_flag(self):
        return 1

    def handle_special_event(self, event_type, event):
        print(f"Special event [{event_type}, {event}] forwarded by server")
        self.network_layer.broadcast(event_type, event, 0)
