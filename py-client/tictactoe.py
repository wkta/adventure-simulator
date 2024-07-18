import sys
from GameModel import GameModel, EMPTY_CELL
import pygame
import socket
import threading

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
blue = (78, 140, 243)
light_blue = (100, 100, 255)
red = (242, 89, 97)
light_red = (255, 100, 100)
dark_grey = (85, 85, 85)
light_grey = (100, 100, 100)
background_color = (225, 225, 225)
screen = pygame.display.set_mode((300, 350))
pygame.display.set_caption('my ttt game')
crossImg = pygame.image.load('crossImg.png')
circleImg = pygame.image.load('circleImg.png')
previewCrossImg = pygame.image.load('prev_crossImg.png')
previewCircleImg = pygame.image.load('prev_circleImg.png')
restartImg = pygame.image.load('restart.png')
restartHoveredImg = pygame.image.load('restart_hovered.png')
font = pygame.font.Font('freesansbold.ttf', 32)
X_score = pygame.image.load('X_scoreImg.png')
O_score = pygame.image.load('O_scoreImg.png')
buttom1 = None
buttom2 = None
logo = None

model = GameModel()
previewImg = None
def game(mode_de_jeu, local_player_sym):
    global model, previewImg
    if mode_de_jeu != 0:
        raise NotImplementedError
    pygame.mouse.set_pos(150, 175)
    previewImg = updatePlayer(model.curr_player)
    running = True
    while running:
        won = None
        mouse = pygame.mouse.get_pos()
        row, col = int(mouse[0] / 100), int(mouse[1] / 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                stop_network()

            elif model.test_full_board():
                model.reset_board()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if row < 3 and col < 3 and model.board[row][col] == EMPTY_CELL:
                    if model.curr_player == local_player_sym:
                        prevplayer = model.curr_player
                        model.play_move(row, col)

                        won = verifyWinner(prevplayer)
                        if not won:  # if won, we'll push infos later
                            m = model.serialize()
                            client_socket.sendall(m.encode())

                elif 250 < mouse[0] < 282 and 310 < mouse[1] < 342:
                    model.reset_game()
        screen.fill(background_color)
        drawBoard()
        drawBottomMenu(mouse)
        if won:
            pygame.time.wait(500)
            m = model.serialize()
            print('»» Sending:', m)
            client_socket.sendall(m.encode())
            print()

        elif row < 3 and col < 3:
            visualizeMove(row, col, previewImg)
        pygame.display.update()


def drawBoard():
    global model
    for row in range(3):
        for col in range(3):
            pos = (row * 100 + 6, col * 100 + 6)
            if model.board[row][col] == 'X':
                screen.blit(crossImg, pos)
            elif model.board[row][col] == 'O':
                screen.blit(circleImg, pos)
    width = 10
    color = dark_grey
    pygame.draw.line(screen, color, (100, 0), (100, 300), width)
    pygame.draw.line(screen, color, (200, 0), (200, 300), width)
    pygame.draw.line(screen, color, (0, 100), (300, 100), width)
    pygame.draw.line(screen, color, (0, 200), (300, 200), width)
    pygame.draw.rect(screen, color, (0, 0, 5, 300))
    pygame.draw.rect(screen, color, (0, 0, 300, 5))
    pygame.draw.rect(screen, color, (295, 0, 5, 300))


def drawBottomMenu(mouse):
    global model
    pygame.draw.rect(screen, dark_grey, (0, 300, 300, 50))
    pygame.draw.rect(screen, light_grey, (5, 305, 290, 40))
    screen.blit(restartImg, (250, 310))
    if 250 < mouse[0] < 282 and 310 < mouse[1] < 342:
        screen.blit(restartHoveredImg, (248, 308))
    screen.blit(X_score, (40, 310))
    screen.blit(O_score, (190, 310))
    scoreboard = font.render(': %d x %d :' % (model.score['X'], model.score['O']), True, background_color, light_grey)
    screen.blit(scoreboard, (72, 310))


def visualizeMove(row, col, previewImg):
    global model
    if model.board[row][col] == EMPTY_CELL:
        screen.blit(previewImg, (row * 100 + 6, col * 100 + 6))


def updatePlayer(player):
    if player == 'X':
        previewImg = previewCrossImg
    else:
        previewImg = previewCircleImg
    return previewImg


def isWinner(player):
    global model
    board = model.board
    return ((board[0][0] == player and board[0][1] == player and board[0][2] == player) or
            (board[1][0] == player and board[1][1] == player and board[1][2] == player) or
            (board[2][0] == player and board[2][1] == player and board[2][2] == player) or
            (board[0][0] == player and board[1][0] == player and board[2][0] == player) or
            (board[0][1] == player and board[1][1] == player and board[2][1] == player) or
            (board[0][2] == player and board[1][2] == player and board[2][2] == player) or
            (board[0][0] == player and board[1][1] == player and board[2][2] == player) or
            (board[0][2] == player and board[1][1] == player and board[2][0] == player))


def verifyWinner(player):
    global model
    if isWinner(player):
        print('final board:', model.serialize())
        playSound('resetSound.wav')
        model.score[player] += 1
        model.endgame = 't'
        return True


def playSound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()


def receive_updates(client_socket):
    global model, previewImg
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        serial = data.decode()
        print(f'Received shared variable update: {serial}')
        model = GameModel.deserialize(serial)

        previewImg = updatePlayer(model.curr_player)

        print(f'Updated model: {model.serialize()}')
        if model.endgame == 't' and local_pl == 'X':
            model.reset_game()
            m = model.serialize()
            client_socket.sendall(m.encode())


if sys.argv[1] == 'player1':
    local_pl, remote_pl = 'X', 'O'
else:
    local_pl, remote_pl = 'O', 'X'


client_socket = None
receiver_thread = None

def start_client():
    global client_socket, receiver_thread
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    receiver_thread = threading.Thread(target=receive_updates, args=(client_socket,))
    receiver_thread.start()


def stop_network():
    global receiver_thread, client_socket
    if receiver_thread:
        receiver_thread.join()
    if client_socket:
        client_socket.close()


start_client()

game(0, local_pl)
