import socket
import sys
import threading

import pygame

from GameModel import GameModel, EMPTY_CELL
from core.events import game_events_enum, EvManager, EngineEvTypes, EvListener, Emitter


ev_mger = EvManager.instance()


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
previewImg = None
running = True

mouse = None
selection = [None, None]


def updatePlayer(player):
    if player == 'X':
        previewImg = previewCrossImg
    else:
        previewImg = previewCircleImg
    return previewImg


def verifyWinner(model, player):
    if GameModel.test_winner(model.board, player):
        print('final board:', model.serialize())
        playSound('resetSound.wav')
        model.score[player] += 1
        return True


def playSound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()


client_socket = None
receiver_thread = None


def receive_updates(clisocket):
    global game_model_obj, ev_mger, running

    while running:
        data = clisocket.recv(1024)
        if not data:
            break
        serial = data.decode()
        print(f'Received shared variable update: {serial}')

        # -------------
        #  replace local game model
        # -------------
        game_model_obj.sync_state(serial)
        print(f'Network has updated model: {game_model_obj.serialize()}')
        ev_mger.post(EngineEvTypes.NetwReceive)


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


# ---------------------
#  mes def
# ---------------------
class GameGodObject(EvListener):
    def on_netw_receive(self, ev):
        global previewImg, game_model_obj, client_socket
        previewImg = updatePlayer(game_model_obj.curr_player)

        if game_model_obj.endgame == 't' and local_pl == 'X':
            game_model_obj.reset_game()
            m = game_model_obj.serialize()
            client_socket.sendall(m.encode())

    def on_update(self, ev):
        # TODO use events board cange to handle the logic
        global running, mouse, selection
        global game_model_obj
        won = None
        mouse = pygame.mouse.get_pos()
        row, col = int(mouse[0] / 100), int(mouse[1] / 100)
        selection[0] = row
        selection[1] = col
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                stop_network()

            elif GameModel.test_full_board(game_model_obj.board):
                # TODO why have we replaced this?
                # model.reset_board()
                game_model_obj.reset_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if row < 3 and col < 3 and game_model_obj.board[row][col] == EMPTY_CELL:
                    if game_model_obj.curr_player == local_pl:
                        game_model_obj.play_move(row, col)
                        won = verifyWinner(game_model_obj, game_model_obj.curr_player)
                        if not won:  # if won, we will push infos later, without increm turn
                            game_model_obj.next_turn()
                            m = game_model_obj.serialize()
                            client_socket.sendall(m.encode())

                elif 250 < mouse[0] < 282 and 310 < mouse[1] < 342:
                    game_model_obj.reset_game()
        if won:
            pygame.time.wait(500)
            m = game_model_obj.serialize()
            print('»» Sending:', m)
            client_socket.sendall(m.encode())
            print()


class GameView(EvListener):
    def __init__(self, mod):
        super().__init__()
        self.ref_model = mod

    def _draw_board(self, ref_board):
        for row in range(3):
            for col in range(3):
                pos = (row * 100 + 6, col * 100 + 6)
                if ref_board[row][col] == 'X':
                    screen.blit(crossImg, pos)
                elif ref_board[row][col] == 'O':
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

    def _draw_bottom_menu(self, mouse):
        pygame.draw.rect(screen, dark_grey, (0, 300, 300, 50))
        pygame.draw.rect(screen, light_grey, (5, 305, 290, 40))
        screen.blit(restartImg, (250, 310))
        if 250 < mouse[0] < 282 and 310 < mouse[1] < 342:
            screen.blit(restartHoveredImg, (248, 308))
        screen.blit(X_score, (40, 310))
        screen.blit(O_score, (190, 310))
        scoreboard = font.render(': %d x %d :' % (self.ref_model.score['X'], self.ref_model.score['O']), True, background_color,
                                 light_grey)
        screen.blit(scoreboard, (72, 310))

    def _draw_move_preview(self, row, col, previewImg):
        if self.ref_model.board[row][col] == EMPTY_CELL:
            screen.blit(previewImg, (row * 100 + 6, col * 100 + 6))

    def on_paint(self, ev):
        global mouse, selection
        screen.fill(background_color)
        self._draw_board(self.ref_model.board)
        self._draw_bottom_menu(mouse)
        if selection[0] < 3 and selection[1] < 3:
            self._draw_move_preview(selection[0], selection[1], previewImg)


def init_game(mode_de_jeu, refmodel):
    global previewImg

    if mode_de_jeu != 0:  # réseau
        raise NotImplementedError

    start_client()

    pygame.mouse.set_pos(150, 175)
    previewImg = updatePlayer(refmodel.curr_player)


# ----------------------
#  longue init. then game loop
# ----------------------
game_model_obj = GameModel()

ev_mger.setup()
gamectrl = GameGodObject()
gamectrl.turn_on()
gameview = GameView(game_model_obj)
gameview.turn_on()

if sys.argv[1] == 'player1':
    local_pl, remote_pl = 'X', 'O'
else:
    local_pl, remote_pl = 'O', 'X'
init_game(0, game_model_obj)

while running:
    ev_mger.post(EngineEvTypes.Update)
    ev_mger.post(EngineEvTypes.Paint)
    ev_mger.update()
    pygame.display.update()
