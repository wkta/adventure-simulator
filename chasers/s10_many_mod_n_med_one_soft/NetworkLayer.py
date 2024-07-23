

class NetworkLayer:
    def __init__(self):
        self._mediators = []

    def register_mediator(self, mediator):
        self._mediators.append(mediator)

    # in the simulation we use :
    def broadcast(self, event_type, event, target_mtype):
        # target_mtype : who we target 1 to target the server
        for a_mediator in self._mediators:
            if a_mediator.server_side_flag() == target_mtype:
                a_mediator.post(event_type, event, enable_event_forwarding=False)

    # def send_special_event(self, event_type, event, source_mediator):
    #     message = process_data(event_type, event)
    #     # Call JavaScript function to send data
    #     print('netw layer pushing::', message)
    #     __pragma__('js', '{}', 'sendToClients')(message)
    #
    # def inject_packed_ev(self, serialized_event):
    #     tmp = serialized_event.split('#')
    #     evtype = tmp[0]
    #     evcontent = json_loads(tmp[1])
    #     for m in self.mediators:
    #         m.post(evtype, evcontent, False)
