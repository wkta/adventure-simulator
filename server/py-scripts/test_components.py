from game_objects import Point3D


class ClientComponent:
    def __init__(self, mediator):
        self.mediator = mediator
        print('un client instancié avec mediator ... ', self.mediator.ident)
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.point = None

        self.mediator.register('move', self.on_move)
        self.mediator.register('cross_move', self.on_cross_move)
        self.mediator.register('cross_player_wins', self.on_player_wins)
        self.mediator.register('cross_sync_state', self.on_cross_sync_state)

    def kill_player(self):
        print('client component vient de kill')
        self.mediator.post('cross_player_dies', None)

    def play_move(self, row, col, symbol):
        if self.board[row][col] == '':
            self.board[row][col] = symbol
            print(f"{self.mediator.component_name} plays  ({row}, {col}), symbol: {symbol}")
            self.mediator.post('move', (row, col, symbol))
        else:
            print(f"{self.mediator.component_name} cannot play ({row}, {col}) is occupied!")

    def print_board(self):
        for row in self.board:
            print(' '.join(cell or '.' for cell in row))
        print()

    # ---------------
    # callbacks
    # ---------------
    def on_cross_sync_state(self, event):
        print('client reception cross_sync_state')
        if self.point:
            self.point.sync_state(event)

    def on_cross_move(self, ev):
        print(' ### dans on_cross_move ClientComponent')

    def on_player_wins(self, ev):
        print(' ### dans on_player_wins ! ClientComponent')

    def on_move(self, move):
        print(' ### dans on_move ClientComponent')
        row, col, symbol = move
        self.board[row][col] = symbol
        print(f"{self.mediator.component_name} receives notification :: ({row}, {col}) with {symbol}")
        self.print_board()


class ServerComponent:
    def __init__(self, mediator):
        self.mediator = mediator
        print('un serveur instancié avec mediator ... ', self.mediator.ident)
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.three_d_point = Point3D(11.2, 5.1, 3.0, mediator)

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
        # self.three_d_point.sync_state(event)
        self.serial = event
        print('new serial the server uses:', event)

    def on_cross_player_dies(self, event):
        print('server recoit info mort', event)
