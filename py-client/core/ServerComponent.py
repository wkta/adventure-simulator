from game_objects import Point3D


class ServerComponent:
    def __init__(self, mediator):
        self.mediator = mediator
        print('un serveur instancié avec mediator ... ', self.mediator.ident)
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.three_d_point = Point3D(None, None, None, mediator)

        self.mediator.register('move', self.process_move)
        self.mediator.register('cross_player_dies', self.on_cross_player_dies)
        self.mediator.register('cross_push_changes', self.on_cross_push_changes)

    def flag_winner(self):
        print('  serveur indication win')
        self.mediator.post('cross_player_wins', None)

    def process_move(self, move):
        row, col, symbol = move
        if self.board[row][col] == '':
            self.board[row][col] = symbol
            print(f"Server processing move: ({row}, {col}) with {symbol}")
            self.mediator.post('cross_move', move)
        else:
            print(f"Invalid move at ({row}, {col}), cell already occupied!")

    def evolve_vector(self):
        x, y, z = self.three_d_point.components
        y = y * -1
        x = 2 * x
        self.three_d_point.components = (x, y, z)

    # ---------------
    # callbacks
    # ---------------
    def on_cross_push_changes(self, event):
        self.three_d_point.sync_state(event)

    def on_cross_player_dies(self, event):
        print('server recoit info mort', event)
