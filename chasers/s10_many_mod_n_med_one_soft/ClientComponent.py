from NetwReadyModel import NetwReadyModel
from ext_mediators import ClientMediator


class ClientComponent:
    def __init__(self, netlayer, player_sym):
        self.mediator = ClientMediator(player_sym, netlayer)
        self._model = NetwReadyModel(self.mediator, player_sym)
        self.mediator.register('cross_sync_state', self.on_cross_sync_state)
        self.player_sym = player_sym

    def disp_model(self):
        self._model.display()

    def input_play(self):
        curr_pl = self.player_sym
        possib = self._model.get_possible_mvt(curr_pl)
        for i, val in enumerate(possib):
            print(f'  {i + 1}. ', val)
        inp = input(f'where to move {curr_pl} ? [type q to quit]')
        if inp == 'q':
            self.mediator.post('game_ends', None)
            return None
        return possib[int(inp) - 1]

    def commit_move(self, wanted_cell):
        self._model.move_pl(self.player_sym, wanted_cell)
        self._model.display()

    # callback
    def on_cross_sync_state(self, evcontent):
        print(f' client {self.mediator.ident} va charger un state!')
        self._model.load_state(evcontent)
