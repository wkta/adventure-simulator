import sys
sys.path.append('..')
from Mediator import Mediator


class ClientMediator(Mediator):
    def __init__(self, component_name, network_layer):
        super().__init__()
        self.ident = self.gen_id()
        self.component_name = component_name
        self.network_layer = network_layer
        network_layer.register_mediator(self)

    def server_side_flag(self):
        return 0

    def handle_special_event(self, event_type, event):
        print(f"Special event [event_type={event_type}] is being forwarded, med:", self.ident)
        self.network_layer.broadcast(event_type, event, 1)


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
