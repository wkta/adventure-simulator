from GameModel import GameModel, EMPTY_CELL


scores = {'X': 1, 'O': -1, 'tie': 0}


def process_input(givenserial):  # computer_move

    model = GameModel.deserialize(givenserial)
    board = model.board
    # MiniMax algorithm to find the best move
    bestScore = 99999
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY_CELL:
                board[row][col] = 'O'
                score = minimax(board, 'X')
                board[row][col] = EMPTY_CELL
                if score < bestScore:
                    bestScore = score
                    bestMove = (row, col)
    board[bestMove[0]][bestMove[1]] = 'O'
    if GameModel.test_winner(board, 'O'):
        model.endgame = 't'
    model.curr_player = 'X'
    return model.serialize()


def minimax(board, cur_player):
    global scores

    # Calculate the board score
    if GameModel.test_winner(board, 'X'):
        return scores['X']
    elif GameModel.test_winner(board, 'O'):
        return scores['O']
    elif GameModel.test_full_board(board):
        return scores['tie']
    # Verify if it is the maximizing or minimizing player
    if cur_player == 'X':
        bestScore = -99999
        nextPlayer = 'O'
        minORmax = max
    else:
        bestScore = 99999
        nextPlayer = 'X'
        minORmax = min
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY_CELL:
                board[row][col] = cur_player
                score = minimax(board, nextPlayer)
                board[row][col] = EMPTY_CELL
                bestScore = minORmax(score, bestScore)
            # In case the 'AI' finds the best possible score
            if bestScore == scores[cur_player]:
                return bestScore
    return bestScore
