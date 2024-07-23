from NetwReadyModel import NetwReadyModel


class ServerComponent:
    def __init__(self, mediator):
        self.mediator = mediator
        self._model = NetwReadyModel(mediator, None)
        self.mediator.register('cross_push_changes', self.on_cross_push_changes)
        self.mediator.register('cross_move_player', self.on_cross_move_player)

    # important for being able to use the 'Massiv debug' function
    def disp_model(self):
        self._model.display()

    # ---------------
    # callbacks
    # ---------------
    def on_cross_push_changes(self, event):
        print('serv:reception event pour enregistrer model OK', event)
        self._model.load_state(event)
        self.mediator.post('cross_sync_state', self._model.serialize())

    def on_cross_move_player(self, event):
        lp, i_str, j_str = event.split('#')
        i = int(i_str)
        j = int(j_str)
        self._model.move_pl(lp, (i, j))
        self.mediator.post('cross_sync_state', self._model.serialize())
