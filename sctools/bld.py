import string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
from typing import Tuple

BLD_CFG_EDGES = {
    "start": {
        "U": "red",
        "L": "blue",
        "F": "white",
        "R": "green",
        "B": "yellow",
        "D": "orange"
    },
    "memo_schema": [
        "UB", "UR", "UF", "UL", 
        "LU", "LF", "LD", "LB",
        "FU", "FR", "FD", "FL",
        "RU", "RB", "RD", "RF",
        "BU", "BL", "BD", "BR",
        "DF", "DR", "DB", "DL"
    ]
}

_POS_TO_MEMO = dict(zip(BLD_CFG_EDGES["memo_schema"], string.ascii_uppercase))
_PAIR_TO_MEMO = {(BLD_CFG_EDGES["start"][k[0]], BLD_CFG_EDGES["start"][k[1]]): v for k, v in _POS_TO_MEMO.items()}
_IDX_TO_PAIR = dict(zip(range(0, 24), _PAIR_TO_MEMO.keys()))

BLD_EDGES_ENCODER = dict(
    pos_to_memo=_POS_TO_MEMO, 
    pair_to_memo=_PAIR_TO_MEMO,
    idx_to_pair=_IDX_TO_PAIR,
)

class Trainer:

    def get_random_edge(self) -> Tuple[str, str]:
        pick = int(np.random.rand() * 24)
        return BLD_EDGES_ENCODER["idx_to_pair"][pick]
    
    def check_edge_memo_letter(self, pair: Tuple[str, str], letter: str):
        ref_letter = self.get_memo_letter_from_pair(pair)
        return ref_letter.lower() == letter.lower()
    
    def get_memo_letter_from_pair(self, pair: Tuple[str, str]):
        return BLD_EDGES_ENCODER["pair_to_memo"][pair]

    def draw_edge(self, edge: Tuple, print_correct: bool = False):

        if print_correct:
            print(BLD_EDGES_ENCODER["pair_to_memo"][edge])

        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        square_d = patches.Rectangle((0, -1), 1, 1, edgecolor='black', facecolor=edge[0])
        square_f = patches.Rectangle((0, 0), 1, 1, edgecolor='black', facecolor=edge[1])

        ax.add_patch(square_f)
        ax.add_patch(square_d)

        ax.set_axis_off()

        ax.set_xlim(-0, 1)
        ax.set_ylim(-1, 1)

        ax.set_aspect('equal', adjustable='box')  # Ensures equal aspect ratio

        return fig