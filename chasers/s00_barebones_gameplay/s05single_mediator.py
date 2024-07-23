import json
import random
from Mediator import Mediator
from s00gameplay import Model


class ModelWithEvents(Model):
    def __init__(self, med):
        super().__init__()
        self.mediator = med

    def move_pl(self, sym, ij_target):
        y = super().move_pl(sym, ij_target)
        self.mediator.post('player_moves', json.dumps({'cell': ij_target, 'who': sym}))
        if y:
            actor_msg = '{"who":"p1"}' if sym == 'p1' else '{"who":"p2"}'
            self.mediator.post('player_scores', actor_msg)
            if self.winner is not None:
                self.mediator.post('player_wins', actor_msg)


if __name__ == '__main__':
    my_mediator = Mediator()
    wm = ModelWithEvents(my_mediator)
    wm.display()

    curr_pl = random.choice(('p1', 'p2'))
    while True:
        possib = wm.get_possible_mvt(curr_pl)
        k = len(possib)
        for i, val in enumerate(possib):
            print(f'  {i + 1}. ', val)
        inp = input(f'where to move {curr_pl} ? [type q to quit]')
        if inp == 'q':
            break
        wanted_cell = possib[int(inp) - 1]
        wm.move_pl(curr_pl, wanted_cell)
        wm.display()
        curr_pl = 'p1' if curr_pl == 'p2' else 'p2'
