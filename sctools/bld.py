import string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon

from matplotlib.figure import Figure
from typing import Tuple, Literal, Union


BLD_CFG = {
    "start": {
        "U": "red",
        "L": "blue",
        "F": "white",
        "R": "green",
        "B": "yellow",
        "D": "orange"
    },
    "edges_memo_schema": [
        "UB", "UR", "UF", "UL", 
        "LU", "LF", "LD", "LB",
        "FU", "FR", "FD", "FL",
        "RU", "RB", "RD", "RF",
        "BU", "BL", "BD", "BR",
        "DF", "DR", "DB", "DL"
    ],
    "corners_memo_schema": [
        "ULB", "UBR", "URF", "UFL",
        "LBU", "LUF", "LFD", "LDB",
        "FLU", "FUR", "FRD", "FDL",
        "RFU", "RUB", "RDF", "RBD",
        "BRU", "BUL", "BLD", "BDR",
        "DLF", "DFR", "DRB", "DBL"
    ]
}

_EDGES_POS_TO_MEMO = dict(zip(BLD_CFG["edges_memo_schema"], string.ascii_uppercase))

_EDGES_TUPLE_TO_MEMO = {
    (
        BLD_CFG["start"][k[0]], 
        BLD_CFG["start"][k[1]]
    ): v for k, v in _EDGES_POS_TO_MEMO.items()
}
_EDGES_IDX_TO_TUPLE = dict(zip(range(0, 24), _EDGES_TUPLE_TO_MEMO.keys()))

BLD_EDGES_ENCODER = dict(
    pos_to_memo=_EDGES_POS_TO_MEMO, 
    tuple_to_memo=_EDGES_TUPLE_TO_MEMO,
    idx_to_tuple=_EDGES_IDX_TO_TUPLE,
)

_CORNERS_POS_TO_MEMO = dict(zip(BLD_CFG["corners_memo_schema"], string.ascii_uppercase))

_CORNERS_TUPLE_TO_MEMO = {
    (
        BLD_CFG["start"][k[0]], 
        BLD_CFG["start"][k[1]],
        BLD_CFG["start"][k[2]]
    ): v for k, v in _CORNERS_POS_TO_MEMO.items()
}
_CORNERS_IDX_TO_TUPLE = dict(zip(range(0, 24), _CORNERS_TUPLE_TO_MEMO.keys()))

BLD_CORNERS_ENCODER = dict(
    pos_to_memo=_CORNERS_POS_TO_MEMO, 
    tuple_to_memo=_CORNERS_TUPLE_TO_MEMO,
    idx_to_tuple=_CORNERS_IDX_TO_TUPLE,
)

class Trainer:

    def get_random_piece(self, 
                         ptype: Literal["edge", "corner"] = "edge") -> Tuple[str, str]:

        pick = int(np.random.rand() * 24)
        if ptype == "edge": 
            return BLD_EDGES_ENCODER["idx_to_tuple"][pick]
        elif ptype == "corner":
            return BLD_CORNERS_ENCODER["idx_to_tuple"][pick]          
    
    def check_piece_memo_letter(self, 
                                tuple: Union[Tuple[str, str], Tuple[str, str, str]], 
                                letter: str,
                                ptype: Literal["edge", "corner"] = "edge"):

        if ptype == "edge":
            ref_letter = self.get_edge_memo_letter_from_tuple(tuple)
        elif ptype == "corner":
            ref_letter = self.get_corner_memo_letter_from_tuple(tuple)
        else:
            raise NotImplementedError
        
        return ref_letter.lower() == letter.lower()
    
    def get_edge_memo_letter_from_tuple(self, tuple: Tuple[str, str]) -> str:
        return BLD_EDGES_ENCODER["tuple_to_memo"][tuple]

    def get_corner_memo_letter_from_tuple(self, tuple: Tuple[str, str]) -> str:
        return BLD_CORNERS_ENCODER["tuple_to_memo"][tuple]

    def draw_edge(self, edge: Tuple[str, str], print_correct: bool = False):

        if print_correct:
            print(BLD_EDGES_ENCODER["tuple_to_memo"][edge])

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

    def draw_corner(self, corner: Tuple[str, str, str], print_correct: bool = False):
        
        if print_correct:
            print(BLD_CORNERS_ENCODER["tuple_to_memo"][corner])

        fig = Figure(figsize=(2, 2))
        ax = fig.add_subplot(111)

        # Define the vertices of the cube faces
        top_face = [(0.5, 1), (1, 0.75), (0.5, 0.5), (0, 0.75)]
        left_face = [(0, 0.75), (0.5, 0.5), (0.5, 0), (0, 0.25)]
        right_face = [(1, 0.75), (1, 0.25), (0.5, 0), (0.5, 0.5)]

        # Draw each face
        ax.add_patch(Polygon(top_face, closed=True, edgecolor='black', facecolor=corner[0], alpha=0.8))
        ax.add_patch(Polygon(left_face, closed=True, edgecolor='black', facecolor=corner[2], alpha=0.5))
        ax.add_patch(Polygon(right_face, closed=True, edgecolor='black', facecolor=corner[1], alpha=0.5))

        # Remove axis ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Set axis limits
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)

        # Ensure equal aspect ratio
        ax.set_aspect('equal', adjustable='box')

        return fig