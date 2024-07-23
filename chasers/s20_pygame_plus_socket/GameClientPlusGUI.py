from NetwReadyModel import NetwReadyModel
from ext_mediators import ClientMediator
import glvars
import pygame


P1_COLOR = 'blue'
P2_COLOR = 'red'


class GameClientPlusGUI:
    def __init__(self, netlayer, player_sym):
        self.mediator = ClientMediator(player_sym, netlayer)
        self._model = NetwReadyModel(self.mediator, player_sym)

        self.mediator.register('cross_sync_state', self.on_cross_sync_state)
        self.mediator.register('paint', self.on_paint)

    @property
    def local_player(self):
        return self._model.localplayer

    def disp_model(self):
        glvars.screen.fill('gray')
        cellsize = 64
        p1_pos = self._model.positions['p1']
        p2_pos = self._model.positions['p2']
        ai_pos = self._model.positions['ai']

        # draw squares + entities
        for lig in range(4):
            for c in range(6):
                a, b = c*64, lig*64
                pygame.draw.rect(
                    glvars.screen, 'black',
                    (a, b, cellsize-1, cellsize-1),
                    0  # filled shape
                )
                if c == p1_pos[0] and lig == p1_pos[1]:
                    pygame.draw.rect(
                        glvars.screen, P1_COLOR,
                        (a, b, 30, 30), 6  # line width 6
                    )
                elif c == p2_pos[0] and lig == p2_pos[1]:
                    pygame.draw.rect(
                        glvars.screen, P2_COLOR,
                        (a, b, 30, 30), 6
                    )

    def get_player_loc(self) -> tuple:
        return self._model.positions[self.local_player]

    def request_move(self, wanted_cell):
        possib = self._model.get_possible_mvt(self.local_player)
        print(wanted_cell)
        if wanted_cell not in possib:
            raise ValueError('invalid cell requested')
        self._model.remote_move_pl(*wanted_cell)

    # -------------------------
    # callbacks
    # -------------------------
    def on_cross_sync_state(self, evcontent):
        print(f' client {self.mediator.ident} va charger un state!')
        self._model.load_state(evcontent)

    def on_paint(self, evcontent):
        self.disp_model()
