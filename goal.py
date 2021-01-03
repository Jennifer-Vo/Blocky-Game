"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
# import math
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """

    save_col = list()
    goals = list()
    i = 0

    classes = random.randint(0, 1)
    while i < num_goals:
        r = random.choice(COLOUR_LIST)
        if r in save_col:
            continue
        save_col.append(r)

        if classes == 0:
            goals.append(PerimeterGoal(r))
        else:
            goals.append(BlobGoal(r))
        i += 1

    return goals


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    if block.children:
        child_f = []
        for i in range(4):
            tmp = _flatten(block.children[i])
            child_f.append(tmp)

        for i in range(child_f[1].__len__()):
            child_f[1][i] += child_f[2][i]
            child_f[0][i] += child_f[3][i]

        child_f[1] += child_f[0]

        return child_f[1]
    else:
        fla = []
        for _ in range(2 ** (block.max_depth - block.level)):
            tmp = []
            for _ in range(2 ** (block.max_depth - block.level)):
                tmp.append(block.colour)
            fla.append(tmp)
        return fla


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A goal in the game of Blocky. The player must aim to put the most
    possible units of a given colour c on the outer perimeter of the board.
    """
    def score(self, board: Block) -> int:
        """Return the current score for PerimeterGoal on the given board.
        The player’s score is the total number of unit cells of colour c that
        are on the perimeter. There is a premium on corner cells: they count
        twice towards the score.
        The score is always greater than or equal to 0.
        """
        data_fla = _flatten(board)
        b_score = 0
        for i in data_fla[0]:
            if i == self.colour:
                b_score += 1
        for i in data_fla[len(data_fla) - 1]:
            if i == self.colour:
                b_score += 1

        i = 0
        while i < data_fla.__len__():
            if self.colour == data_fla[i][len(data_fla) - 1]:
                b_score += 1
            if self.colour == data_fla[i][0]:
                b_score += 1
            i += 1
        return b_score

    def description(self) -> str:
        """Return a description of PerimeterGoal, including the target colour.
        """
        return 'PerimeterGoal: Aim to put the most possible units of colour ' \
               'on the outer perimeter of the board: ' \
               '{}'.format(colour_name(self.colour))


class BlobGoal(Goal):
    """A goal in the the game of Blocky. The player must aim for the largest
    “blob” of a given colour c. A blob is a group of connected blocks with the
    same colour.
    """
    def score(self, board: Block) -> int:
        """Return the current score for BlobGoal on the given board. The
        player’s score is the number of unit cells in the largest blob of
        colour c. Two blocks are connected if their sides touch; touching
        corners does not count.The score is always greater than or equal to 0.
        """
        data_fla = _flatten(board)
        b_score = 0

        for i in range(data_fla.__len__()):
            used = []
            for _ in range(data_fla.__len__()):
                tmp = [-1 for __ in range(data_fla.__len__())]
                used.append(tmp)

            for j in range(data_fla.__len__()):
                b_score = max(self._undiscovered_blob_size((i, j), data_fla,
                                                           used), b_score)
        return b_score

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """

        if pos[0] < 0 or pos[0] > (len(visited) - 1):
            return 0
        if pos[1] < 0 or pos[1] > (len(visited) - 1):
            return 0

        if visited[pos[0]][pos[1]] == 0:
            return 0
        if visited[pos[0]][pos[1]] == 1:
            return 0

        if board[pos[0]][pos[1]] != self.colour:
            visited[pos[0]][pos[1]] = 0
            return 0

        visited[pos[0]][pos[1]] = 1
        a = self._undiscovered_blob_size((pos[0], pos[1] - 1), board, visited)
        b = self._undiscovered_blob_size((pos[0], pos[1] + 1), board, visited)
        c = self._undiscovered_blob_size((pos[0] - 1, pos[1]), board, visited)
        d = self._undiscovered_blob_size((pos[0] + 1, pos[1]), board, visited)
        return 1 + a + b + c + d

    def description(self) -> str:
        """Return a description of BlobGoal, including the target colour.
        """
        return 'BlobGoal: Aim for the largest blob of {}'.format \
            (colour_name(self.colour))


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
