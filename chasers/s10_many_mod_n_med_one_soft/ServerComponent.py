from NetwReadyModel import NetwReadyModel


class ServerComponent:
    def __init__(self, mediator):
        self.mediator = mediator
        self._model = NetwReadyModel(mediator, None)
        print('compo. serveur instancié')

        self.mediator.register('cross_push_changes', self.on_cross_push_changes)
        self.mediator.register('cross_move_player', self.on_cross_move_player)

    def disp_model(self):
        self._model.display()

    # def flag_winner(self):
    #     print('  serveur indication win')
    #     self.mediator.post('cross_player_wins', None)
    #
    # def process_move(self, move):
    #     row, col, symbol = move
    #     if self.board[row][col] == '':
    #         self.board[row][col] = symbol
    #         print(f"Server processing move: ({row}, {col}) with {symbol}")
    #         self.mediator.post('cross_move', move)
    #     else:
    #         print(f"Invalid move at ({row}, {col}), cell already occupied!")

    def evolve_vector(self):
        pass
        # x, y, z = self.three_d_point.components
        # y = y * -1
        # x = 2 * x
        # self.three_d_point.components = (x, y, z)

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
