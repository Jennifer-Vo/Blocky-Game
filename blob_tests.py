from typing import List, Optional, Tuple
import os
import pygame
import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten
from goal import *
from player import _get_block
from player import *
from renderer import Renderer
from settings import COLOUR_LIST

class TestGoal:
    def test__undiscovered_blob_size_one_colour_one_block(self) -> None:
        board = [[COLOUR_LIST[0]]]
        visited = [[-1]]
        pos = (0, 0)
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 1
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0


    def test__undiscovered_blob_size_four_colours_four_blocks(self) -> None:
        board = [[COLOUR_LIST[0], COLOUR_LIST[1]],
                 [COLOUR_LIST[2], COLOUR_LIST[3]]]
        visited = [[-1, -1],
                   [-1, -1]]
        pos = (0, 0)
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 1
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (0, 1)
        visited = [[-1, -1],
                   [-1, -1]]
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 1
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (1, 0)
        visited = [[-1, -1],
                   [-1, -1]]
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 1
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (1, 1)
        visited = [[-1, -1],
                   [-1, -1]]
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 1
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0


    def test__undiscovered_blob_size_two_colours_four_blocks(self) -> None:
        board = [[COLOUR_LIST[0], COLOUR_LIST[0]],
                 [COLOUR_LIST[1], COLOUR_LIST[1]]]
        visited = [[-1, -1],
                   [-1, -1]]
        pos = (0, 0)
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 2
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (0, 1)
        visited = [[-1, -1],
                   [-1, -1]]
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 2
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (1, 0)
        visited = [[-1, -1],
                   [-1, -1]]
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 2
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (1, 1)
        visited = [[-1, -1],
                   [-1, -1]]
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 2
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0


    def test__undiscovered_blob_size_multiple_levels(self) -> None:
        board = [[COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1]],
                 [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1]],
                 [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[0]],
                 [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[0], COLOUR_LIST[0]]]
        visited = [[-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1]]
        pos = (0, 0)
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 4
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (0, 3)
        visited = [[-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1]]
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 4
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (3, 0)
        visited = [[-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1]]
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 5
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        pos = (3, 3)
        visited = [[-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1],
                   [-1, -1, -1, -1]]
        goal = BlobGoal(COLOUR_LIST[0])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 3
        goal = BlobGoal(COLOUR_LIST[1])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[2])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0
        goal = BlobGoal(COLOUR_LIST[3])
        score = goal._undiscovered_blob_size(pos, board, visited)
        assert score == 0

if __name__ == '__main__':
    pytest.main(['blob_tests.py'])
