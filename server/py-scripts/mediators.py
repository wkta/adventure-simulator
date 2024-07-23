import random
from test_components import ServerComponent
from game_objects import json_dumps, json_loads


# like a "polyfill"
class DequeReplacement:  
    def __init__(self, iterable=None):
        self._deque = list(iterable) if iterable else []

    def append(self, item):
        self._deque.append(item)

    def appendleft(self, item):
        self._deque.insert(0, item)

    def pop(self):
        if not self._deque:
            raise IndexError("pop from an empty deque")
        return self._deque.pop()

    def popleft(self):
        if not self._deque:
            raise IndexError("pop from an empty deque")
        return self._deque.pop(0)

    def extend(self, iterable):
        self._deque.extend(iterable)

    def extendleft(self, iterable):
        for item in reversed(iterable):
            self.appendleft(item)

    def clear(self):
        self._deque.clear()

    def remove(self, value):
        self._deque.remove(value)

    def rotate(self, n=1):
        n = n % len(self._deque)
        self._deque = self._deque[-n:] + self._deque[:-n]

    def __len__(self):
        return len(self._deque)

    def __iter__(self):
        return iter(self._deque)

    def __repr__(self):
        return f"ListDeque({self._deque})"

    def __getitem__(self, index):
        return self._deque[index]

    def __setitem__(self, index, value):
        self._deque[index] = value

    def __delitem__(self, index):
        del self._deque[index]

    def insert(self, index, value):
        self._deque.insert(index, value)

    def count(self, value):
        return self._deque.count(value)

    def index(self, value, start=0, stop=None):
        return self._deque.index(value, start, stop if stop is not None else len(self._deque))


deque = DequeReplacement


def process_data(etype, content):
    return etype+'#'+json_dumps(content) #f'{etype},'+str(content)


class NetworkLayer:
    def __init__(self):
        self.mediators = []

    def register_mediator(self, mediator):
        self.mediators.append(mediator)

    # in the simulation anymore we used :
    # def send_special_event(self, event_type, event, source_mediator):
    #     if source_mediator.server_side_flag() == 1:
    #         target_mtype = 0
    #     else:
    #         target_mtype = 1
    #     for a_mediator in self.mediators:
    #         if a_mediator.server_side_flag() == target_mtype:
    #             a_mediator.post(event_type, event, enable_event_forwarding=False)

    def send_special_event(self, event_type, event, source_mediator):
        message = process_data(event_type, event)
        # Call JavaScript function to send data
        print('netw layer pushing::', message)
        __pragma__('js', '{}', 'sendToClients')(message)

    def inject_packed_ev(self, serialized_event):
        tmp = serialized_event.split('#')
        evtype = tmp[0]
        evcontent = json_loads(tmp[1])
        for m in self.mediators:
            m.post(evtype, evcontent, False)


class Mediator:
    def __init__(self):
        self.ident = None
        self.listeners = {}
        self.event_queue = deque()

    @staticmethod
    def gen_id():
        omega = [chr(c) for c in range(ord('a'),ord('z')+1) ] + [str(e) for e in range(0,10)]
        #return os.urandom(6).hex()
        lst = [random.choice(omega) for _ in range(12)]
        return "".join(lst)

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

    # abstractmethod
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

    def handle_special_event(self, event_type, event):
        raise NotImplementedError


class ServerMediator(Mediator):
    def __init__(self, network_layer):
        super().__init__()
        self.ident = self.gen_id()
        self.network_layer = network_layer
        network_layer.mediators.append(self)

    def server_side_flag(self):
        return 1

    def handle_special_event(self, event_type, event):
        print(f"Special event [{event_type}, {event}] forwarded by server")
        self.network_layer.send_special_event(event_type, event, self)


nl_obj = NetworkLayer()
server_mediator = ServerMediator(nl_obj)


def refresh_event_queue():
    global server_mediator
    server_mediator.update()


if '__name__' == '__main__':
    print('xxxxxAAAAAAAAAAAAAAAAAAAAAAxxxxxxxx')
    print()

    server = ServerComponent(server_mediator)

    server.evolve_vector()

    server_mediator.update()  # will send data over the wire

    # server_mediator.update()
    # server_mediator.update()
