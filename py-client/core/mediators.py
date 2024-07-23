from abc import abstractmethod, ABCMeta
import os
from collections import deque


class NetworkLayer:
    def __init__(self):
        self.mediators = []

    def register_mediator(self, mediator):
        self.mediators.append(mediator)

    def send_special_event(self, event_type, event, source_mediator):
        if source_mediator.server_side_flag() == 1:
            target_mtype = 0
        else:
            target_mtype = 1

        for a_mediator in self.mediators:
            if a_mediator.server_side_flag() == target_mtype:  # used to avoid broadcasting to all
                a_mediator.post(event_type, event, enable_event_forwarding=False)


class Mediator(metaclass=ABCMeta):

    def __init__(self):
        self.ident = None
        self.listeners = {}
        self.event_queue = deque()

    @staticmethod
    def gen_id():
        return os.urandom(6).hex()

    def register(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unregister(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)
            if not self.listeners[event_type]:
                del self.listeners[event_type]

    @staticmethod
    def is_special_event(event_type):
        return event_type.startswith('cross_')

    @abstractmethod
    def server_side_flag(self):
        raise NotImplementedError

    def _basic_notify(self, event_type, event):
        if event_type in self.listeners:
            for listener_cb in self.listeners[event_type]:
                listener_cb(event)

    def post(self, event_type, event, enable_event_forwarding=True):
        print(f'  postage event [{event_type}, {event}] sur Mediator:', self.ident)
        self.event_queue.append((event_type, event, enable_event_forwarding))

    def update(self) -> int:
        y = cpt = len(self.event_queue)
        while cpt > 0:
            event_type, event, enable_event_forwarding = self.event_queue.popleft()
            if self.is_special_event(event_type) and enable_event_forwarding:
                self.handle_special_event(event_type, event)
            else:
                self._basic_notify(event_type, event)
            cpt -= 1
        return y

    @abstractmethod
    def handle_special_event(self, event_type, event):
        raise NotImplementedError


class ClientMediator(Mediator):
    def __init__(self, component_name, network_layer):
        super().__init__()
        self.ident = self.gen_id()
        self.component_name = component_name
        self.network_layer = network_layer

    def server_side_flag(self):
        return 0

    def handle_special_event(self, event_type, event):
        print(f"Special event [{event_type}, {event}] forwarded by {self.component_name}", self.ident)
        self.network_layer.send_special_event(event_type, event, self)


class ServerMediator(Mediator):
    def __init__(self, network_layer):
        super().__init__()
        self.ident = self.gen_id()
        self.network_layer = network_layer

    def server_side_flag(self):
        return 1

    def handle_special_event(self, event_type, event):
        print(f"Special event [{event_type}, {event}] forwarded by server")
        self.network_layer.send_special_event(event_type, event, self)
