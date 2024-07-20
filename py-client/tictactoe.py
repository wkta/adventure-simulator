import sys
import pygame
import glvars
from GameModel import GameModel, EMPTY_CELL
from core.events import EvManager, EngineEvTypes, EvListener
import importlib
import json


pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
blue = (78, 140, 243)
light_blue = (100, 100, 255)
red = (242, 89, 97)
light_red = (255, 100, 100)
dark_grey = (85, 85, 85)
light_grey = (100, 100, 100)
screen = pygame.display.set_mode((300, 350))
pygame.display.set_caption('my ttt game')
font = pygame.font.Font('freesansbold.ttf', 32)
buttom1 = None
buttom2 = None
logo = None
running = True
mouse = None
selection = [None, None]


# --------------
#  load networking module
# --------------
with open('client-config.json') as fptr:
    jobj = json.load(fptr)
    target_host, transport = jobj['host'], jobj['transport_type']  # you can select either 'ws' or 'socket' for 2nd

# Dynamically load the appropriate module
networking_module = None
if transport == 'socket':
    networking_module = importlib.import_module('networking')
elif transport == 'ws':
    networking_module = importlib.import_module('ws_networking')
else:
    raise ValueError("Unsupported transport type")


class GameGodObject(EvListener):
    def on_netw_receive(self, ev):
        global game_model_obj
        serial = ev.serial
        game_model_obj.sync_state(serial)
        print(f'afer Network pyv event, we can update model: {game_model_obj.serialize()}')

        if game_model_obj.endgame == 't' and local_pl == 'X':
            game_model_obj.reset_game()
            self.pev(EngineEvTypes.NetwSend, serial=game_model_obj.serialize())
        else:
            self.pev(glvars.gevents.ActivePlayerChanges)

    def on_game_ends(self, ev):
        pygame.time.wait(500)
        print('»» Sending msg after won is True')
        self.pev(EngineEvTypes.NetwSend, serial=game_model_obj.serialize())

    def on_update(self, ev):
        # TODO use events board cange to handle the logic
        global running, mouse, selection
        global game_model_obj

        mouse = pygame.mouse.get_pos()
        row, col = int(mouse[0] / 100), int(mouse[1] / 100)
        selection[0] = row
        selection[1] = col
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                self.pev(glvars.gevents.ExitNetwork)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if row < 3 and col < 3 and game_model_obj.board[row][col] == EMPTY_CELL:
                    curr_pl = game_model_obj.curr_player
                    if curr_pl == local_pl:
                        game_model_obj.play_move(row, col)

                        won = GameModel.test_winner(game_model_obj.board, curr_pl)
                        if won:
                            self.pev(glvars.gevents.GameEnds, soundname='resetSound.wav')
                            game_model_obj.score[curr_pl] += 1
                        else:
                            if GameModel.test_full_board(game_model_obj.board):
                                # TODO why have we replaced this?
                                # model.reset_board()
                                game_model_obj.reset_game()
                                return
                            game_model_obj.next_turn()
                            self.pev(EngineEvTypes.NetwSend, serial=game_model_obj.serialize())

                elif 250 < mouse[0] < 282 and 310 < mouse[1] < 342:
                    game_model_obj.reset_game()


class GameView(EvListener):
    def __init__(self, mod):
        super().__init__()
        self.ref_model = mod
        self.preview_img = None
        self.bgcolor = glvars.BG_COLOR
        self.images = {
            'cross': pygame.image.load('crossImg.png'),
            'circle': pygame.image.load('circleImg.png'),
            'light_cross': pygame.image.load('prev_crossImg.png'),
            'light_circle': pygame.image.load('prev_circleImg.png'),

            'restart': pygame.image.load('restart.png'),
            'restart_hover': pygame.image.load('restart_hovered.png'),
            'X_score': pygame.image.load('X_scoreImg.png'),
            'O_score': pygame.image.load('O_scoreImg.png')
        }

    def _draw_board(self, ref_board):
        for row in range(3):
            for col in range(3):
                pos = (row * 100 + 6, col * 100 + 6)
                if ref_board[row][col] == 'X':
                    screen.blit(self.images['cross'], pos)
                elif ref_board[row][col] == 'O':
                    screen.blit(self.images['circle'], pos)
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
        screen.blit(self.images['restart'], (250, 310))
        if 250 < mouse[0] < 282 and 310 < mouse[1] < 342:
            screen.blit(self.images['restart_hover'], (248, 308))
        screen.blit(self.images['X_score'], (40, 310))
        screen.blit(self.images['O_score'], (190, 310))
        scoreboard = font.render(': %d x %d :' % (self.ref_model.score['X'], self.ref_model.score['O']), True, self.bgcolor,
                                 light_grey)
        screen.blit(scoreboard, (72, 310))

    def _draw_move_preview(self, row, col):
        if self.ref_model.board[row][col] == EMPTY_CELL:
            screen.blit(self.preview_img, (row * 100 + 6, col * 100 + 6))

    # --------------
    #  event handling
    # --------------
    def on_active_player_changes(self, ev):
        if self.ref_model.curr_player == 'X':
            self.preview_img = self.images['light_cross']
        else:
            self.preview_img = self.images['light_circle']

    def on_paint(self, ev):
        global mouse, selection
        screen.fill(self.bgcolor)
        self._draw_board(self.ref_model.board)
        self._draw_bottom_menu(mouse)
        if selection[0] < 3 and selection[1] < 3:
            self._draw_move_preview(selection[0], selection[1])


class SoundCtrl(EvListener):
    def __init__(self):
        super().__init__()
        # self.sounds = {
        # }

    def on_game_ends(self, ev):
        pygame.mixer.music.load(ev.soundname)
        pygame.mixer.music.play()


# ----------------------
#  longue init. then game loop
# ----------------------
if sys.argv[1] == 'player1':
    local_pl, remote_pl = 'X', 'O'
else:
    local_pl, remote_pl = 'O', 'X'

ev_mger = EvManager.instance()
ev_mger.setup(glvars.gevents)
game_model_obj = GameModel()

mode_de_jeu = 0  # vs remote player
pygame.mouse.set_pos(150, 175)
ev_mger.post(glvars.gevents.ActivePlayerChanges)
#if mode_de_jeu == 0:

netw_pusher = networking_module.NetwPusher()
netw_pusher.turn_on()
#else:
#    pass

sfx = SoundCtrl()
sfx.turn_on()

gamectrl = GameGodObject()
gamectrl.turn_on()
gameview = GameView(game_model_obj)
gameview.turn_on()

# game loop
while running:
    ev_mger.post(EngineEvTypes.Update)
    ev_mger.post(EngineEvTypes.Paint)
    ev_mger.update()
    pygame.display.update()
