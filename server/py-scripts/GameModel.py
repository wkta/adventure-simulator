EMPTY_CELL = '.'


class GameModel:

    def __init__(self):
        self.endgame = 'f'
        self.curr_player = 'X'
        self.board = [[EMPTY_CELL for _ in range(3)],
                      [EMPTY_CELL for _ in range(3)],
                      [EMPTY_CELL for _ in range(3)]]
        self.score = {'X': 0, 'O': 0}

    def play_move(self, row, col):
        if self.board[row][col] != EMPTY_CELL:
            raise ValueError
        self.board[row][col] = self.curr_player
        
        if self.test_winner(self.curr_player):
            self.endgame='t'
        else:
            self.curr_player = 'O' if self.curr_player == 'X' else 'X'
    
    @staticmethod
    def test_winner(board, player):
        return ((board[0][0] == player and board[0][1] == player and board[0][2] == player) or
                (board[1][0] == player and board[1][1] == player and board[1][2] == player) or
                (board[2][0] == player and board[2][1] == player and board[2][2] == player) or
                (board[0][0] == player and board[1][0] == player and board[2][0] == player) or
                (board[0][1] == player and board[1][1] == player and board[2][1] == player) or
                (board[0][2] == player and board[1][2] == player and board[2][2] == player) or
                (board[0][0] == player and board[1][1] == player and board[2][2] == player) or
                (board[0][2] == player and board[1][1] == player and board[2][0] == player))
    
    @staticmethod
    def test_full_board(board):
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY_CELL:
                    return False
        return True

    def _reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = EMPTY_CELL

    def reset_game(self):
        self.endgame = 'f'
        self.curr_player = 'X'
        self._reset_board()

    def serialize(self):
        nested = self.board
        flatlist = [self.endgame, self.curr_player, '|']
        for sublist in nested:
            for element in sublist:
                flatlist.append(element)
        return ''.join(flatlist) + '|' + str(self.score['X']) + ',' + str(self.score['O'])

    @classmethod
    def deserialize(cls, data):
        tmp = data.split('|')
        if len(tmp) != 3 or len(tmp[1]) != 9 or len(tmp[0]) != 2:
            raise ValueError("Invalid serial! Check your data format")

        new_instance = cls()
        prefix, data, rest = data.split('|')
        new_instance.curr_player = prefix[1]
        new_instance.endgame = prefix[0]

        index = 0
        for i in range(3):
            for j in range(3):
                new_instance.board[i][j] = data[index]
                index += 1
        tuple_sc = rest.split(',')
        new_instance.score['X'] = int(tuple_sc[0])
        new_instance.score['O'] = int(tuple_sc[1])

        return new_instance

