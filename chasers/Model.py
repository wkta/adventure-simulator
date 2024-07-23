import random


class Model:
    MAXSCORE = 2

    def _find_free_random_loc(self):
        r_loc = (random.randint(0, 5), random.randint(0, 3))
        while r_loc in self.taken:
            r_loc = (random.randint(0, 5), random.randint(0, 3))
        return r_loc

    def __init__(self):
        self.winner = 0  # when this isnt zero, therefore game is over
        self.taken = set()
        self.world = [
            ['.' for _ in range(4)] for _ in range(6)
        ]

        self.positions = dict()
        for sym in ('p1', 'p2', 'ai'):
            self._spawn(sym)
        self.score = {
            'p1': 0, 'p2': 0
        }
        print('monde init. ok')

    def display(self):
        for ligne in range(4):
            for col in range(6):
                print(self.world[col][ligne].ljust(5), end='')
            print()
        x, y = self.score['p1'], self.score['p2']
        print(f'score p1: {x}  |  score p2: {y} ', end='')
        if self.winner != 0:
            print('WINNER ->', self.winner)
        else:
            print()

    def move_pl(self, sym, ij_target):
        dmg = False
        ci, cj = self.positions[sym]
        ti, tj = ij_target

        if self.world[ti][tj] == 'ai':
            self.score[sym] += 1
            if self.score[sym] >= self.__class__.MAXSCORE:
                self.winner = 1 if sym == 'p1' else 2
            dmg = True

        self.world[ci][cj] = '.'
        self.taken.remove((ci, cj))
        self.positions[sym] = ij_target
        self.world[ti][tj] = sym
        self.taken.add((ti, tj))
        if dmg:
            self._spawn('ai')
            return True
        return False

    def _spawn(self, sym):
        p = self._find_free_random_loc()
        self.taken.add(p)
        self.positions[sym] = p
        i, j = p
        self.world[i][j] = sym

    def get_possible_mvt(self, player):
        opponent = 'p1' if player == 'p2' else 'p2'
        omega = [tuple(self.positions[player]) for _ in range(4)]
        for k_rank, offset in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
            cval = self.positions[player]
            omega[k_rank] = (cval[0]+offset[0], cval[1]+offset[1])
        bad_loc = set()
        for elt in omega:
            if not (0 <= elt[0] < 6):
                bad_loc.add(elt)
            elif not (0 <= elt[1] < 4):
                bad_loc.add(elt)
            elif elt == self.positions[opponent]:
                bad_loc.add(elt)
        for y in bad_loc:
            omega.remove(y)
        return omega
