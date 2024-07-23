"""
sketch for the 'chasers' POC
"""
import sys
sys.path.append('..')
from Model import Model
import random


if __name__ == '__main__':
    wm = Model()
    wm.display()
    curr_pl = random.choice(('p1', 'p2'))
    while True:
        possib = wm.get_possible_mvt(curr_pl)
        k = len(possib)
        for i, val in enumerate(possib):
            print(f'  {i+1}. ', val)
        inp = input(f'where to move {curr_pl} ? [type q to quit]')
        if inp == 'q':
            break

        wanted_cell = possib[int(inp)-1]
        wm.move_pl(curr_pl, wanted_cell)
        wm.display()
        curr_pl = 'p1' if curr_pl == 'p2' else 'p2'