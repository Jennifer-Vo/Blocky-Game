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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains some sample tests for Assignment 2.
Please use this as a starting point to check your work and write your own
tests!
"""
from typing import List, Optional, Tuple
import os
import pygame
import pytest
from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE
from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten, generate_goals
from renderer import Renderer
from settings import COLOUR_LIST
from block import Block
from player import _get_block, create_players, HumanPlayer, RandomPlayer, SmartPlayer

def set_children(block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
        -> None:
    """Set the children at <level> for <block> using the given <colours>.

    Precondition:
        - len(colours) == 4
        - block.level + 1 <= block.max_depth
    """
    size = block._child_size()
    positions = block._children_positions()
    level = block.level + 1
    depth = block.max_depth

    block.children = []  # Potentially discard children
    for i in range(4):
        b = Block(positions[i], size, colours[i], level, depth)
        block.children.append(b)


@pytest.fixture
def renderer() -> Renderer:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    return Renderer(750)


@pytest.fixture
def child_block() -> Block:
    """Create a reference child block with a size of 750 and a max_depth of 0.
    """
    return Block((0, 0), 750, COLOUR_LIST[0], 0, 0)


@pytest.fixture
def board_16x16() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_swap0() -> Block:
    """Create a reference board that is swapped along the horizontal plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    return board


@pytest.fixture
def board_16x16_rotate1() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def flattened_board_16x16() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]]
    ]


def test_block_to_squares_leaf(child_block) -> None:
    """Test that a board with only one block can be correctly trasnlated into
    a square that would be rendered onto the screen.
    """
    squares = _block_to_squares(child_block)
    expected = [(COLOUR_LIST[0], (0, 0), 750)]

    assert squares == expected


def test_block_to_squares_reference(board_16x16) -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    # The order the squares appear may differ based on the implementation, so
    # we use a set here.
    squares = set(_block_to_squares(board_16x16))
    expected = {((1, 128, 181), (563, 0), 188),
                ((199, 44, 58), (375, 0), 188),
                ((199, 44, 58), (375, 188), 188),
                ((255, 211, 92), (563, 188), 188),
                ((138, 151, 71), (0, 0), 375),
                ((199, 44, 58), (0, 375), 375),
                ((255, 211, 92), (375, 375), 375)
                }

    assert squares == expected


def test_JEN_smart_player(board_16x16) -> None:
    goal = BlobGoal((138, 151, 71))
    player = SmartPlayer(2, goal, 2)
    player._proceed = True
    score1 = goal.score(board_16x16)
    move = player.generate_move(board_16x16)
    while move is SMASH:
        move.generate_move()
    score2 = goal.score(board_16x16)
    assert move is not None
    assert score2 >= score1

def test_JEN_random_player(board_16x16) -> None:
    goal = BlobGoal((138, 151, 71))
    player = SmartPlayer(2, goal, 2)
    player._proceed = True
    move = player.generate_move(board_16x16)
    assert move is PASS or SMASH or COMBINE or ROTATE_COUNTER_CLOCKWISE or \
    ROTATE_CLOCKWISE or SWAP_VERTICAL or SWAP_HORIZONTAL

def test_JEN_smart_player_not_smart_moves(board_16x16) -> None:
    goal = PerimeterGoal((199, 44, 58))
    player = SmartPlayer(3, goal, 10)
    player._proceed = True
    move = player.generate_move(board_16x16)
    assert move is not COMBINE
    assert move is not ROTATE_CLOCKWISE
    assert move is not ROTATE_COUNTER_CLOCKWISE
    assert move is not SWAP_HORIZONTAL
    assert move is not SWAP_VERTICAL
    assert move is PASS or SMASH

class TestRender:
    """A collection of methods that show you a way to save the boards in your
    test cases to image (i.e., PNG) files.

    NOTE: this requires that your blocky._block_to_squares function is working
    correctly.
    """
    def test_render_reference_board(self, renderer, board_16x16) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('reference-board.png')

    def test_render_reference_board_swap0(self, renderer, board_16x16,
                                          board_16x16_swap0) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        # Render the reference board swapped
        renderer.draw_board(_block_to_squares(board_16x16_swap0))
        renderer.save_to_file('reference-swap-0.png')

        # Render what your swap does to the reference board
        board_16x16.swap(0)
        renderer.clear()
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('your-swap-0.png')

    def test_render_reference_board_rotate1(self, renderer, board_16x16,
                                            board_16x16_rotate1) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        # Render the reference board swapped
        renderer.draw_board(_block_to_squares(board_16x16_rotate1))
        renderer.save_to_file('reference-rotate-1.png')

        # Render what your swap does to the reference board
        board_16x16.swap(0)
        renderer.clear()
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('your-rotate-1.png')


class TestBlock:
    """A collection of methods that test the Block class.

    NOTE: this is a small subset of tests - just because you pass them does NOT
    mean you have a fully working implementation of the Block class.
    """
    def test_smash_on_child(self, child_block) -> None:
        """Test that a child block cannot be smashed.
        """
        child_block.smash()

        assert len(child_block.children) == 0
        assert child_block.colour == COLOUR_LIST[0]

    def test_smash_on_parent_with_no_children(self, board_16x16) -> None:
        """Test that a block not at max_depth and with no children can be
        smashed.
        """
        block = board_16x16.children[1]
        block.smash()

        assert len(block.children) == 4
        assert block.colour is None

        for child in block.children:
            if len(child.children) == 0:
                # A leaf should have a colour
                assert child.colour is not None
                # Colours should come from COLOUR_LIST
                assert child.colour in COLOUR_LIST
            elif len(child.children) == 4:
                # A parent should not have a colour
                assert child.colour is None
            else:
                # There should only be either 0 or 4 children (RI)
                assert False

    def test_swap0(self, board_16x16, board_16x16_swap0) -> None:
        """Test that the reference board can be correctly swapped along the
        horizontal plane.
        """
        board_16x16.swap(0)
        assert board_16x16 == board_16x16_swap0

    def test_rotate1(self, board_16x16, board_16x16_rotate1) -> None:
        """Test that the top-right block of reference board on level 1 can be
        correctly rotated clockwise.
        """
        board_16x16.children[0].rotate(1)
        assert board_16x16 == board_16x16_rotate1


class TestPlayer:
    """A collection of methods for testing the methods and functions in the
    player module.

     NOTE: this is a small subset of tests - just because you pass them does NOT
     mean you have a fully working implementation.
    """
    def test_get_block_top_left(self, board_16x16) -> None:
        """Test that the correct block is retrieved from the reference board
        when requesting the top-left corner of the board.
        """
        top_left = (0, 0)
        assert _get_block(board_16x16, top_left, 0) == board_16x16
        assert _get_block(board_16x16, top_left, 1) == board_16x16.children[1]

    def test_get_block_top_right(self, board_16x16) -> None:
        """Test that the correct block is retrieved from the reference board
        when requesting the top-right corner of the board.
        """
        top_right = (board_16x16.size - 1, 0)
        assert _get_block(board_16x16, top_right, 0) == board_16x16
        assert _get_block(board_16x16, top_right, 1) == board_16x16.children[0]
        assert _get_block(board_16x16, top_right, 2) == \
            board_16x16.children[0].children[0]


class TestGoal:
    """A collection of methods for testing the sub-classes of Goal.

     NOTE: this is a small subset of tests - just because you pass them does NOT
     mean you have a fully working implementation of the Goal sub-classes.
    """
    def test_block_flatten(self, board_16x16, flattened_board_16x16) -> None:
        """Test that flattening the reference board results in the expected list
        of colours.
        """
        result = _flatten(board_16x16)

        # We are expected a "square" 2D list
        for sublist in result:
            assert len(result) == len(sublist)

        assert result == flattened_board_16x16

    def test_blob_goal(self, board_16x16) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 1),
            (COLOUR_LIST[1], 4),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 5)
        ]

        # Set up a goal for each colour and check the results
        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(board_16x16) == expected

    def test_perimeter_goal(self, board_16x16):
        correct_scores = [
            (COLOUR_LIST[0], 2),
            (COLOUR_LIST[1], 5),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 5)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_16x16) == expected

def test_JEN_swap_horizontal() -> None:

    board = Block((0, 0), 20, None, 0, 2)

    child1 = Block((10, 0), 10, None, 1, 2)
    child2 = Block((0, 0), 10, (10, 20, 30), 1, 2)
    child3 = Block((0, 10), 10, (100, 200, 300), 1, 2)
    child4 = Block((10, 10), 10, (1000, 2000, 3000), 1, 2)

    child11 = Block((15, 0), 5, (1, 2, 3), 2, 2)
    child12 = Block((10, 0), 5, (11, 22, 33), 2, 2)
    child13 = Block((10, 5), 5, (111, 222, 333), 2, 2)
    child14 = Block((15, 5), 5, (1111, 2222, 3333), 2, 2)

    child1.children = [child11, child12, child13, child14]

    board.children = [child1, child2, child3, child4]

    board.swap(0)

    assert board.children[0].colour == (10, 20, 30)
    assert board.children[1].colour is None
    assert board.children[3].colour == (100, 200, 300)
    assert board.children[2].colour == (1000, 2000, 3000)
    assert board.children[1].children[0].colour == (1, 2, 3)
    assert board.children[1].children[1].colour == (11, 22, 33)
    assert board.children[1].children[2].colour == (111, 222, 333)
    assert board.children[1].children[3].colour == (1111, 2222, 3333)

    assert board.children[0].position == (10, 0)
    assert board.children[1].position == (0, 0)
    assert board.children[2].position == (0, 10)
    assert board.children[3].position == (10, 10)
    assert board.children[1].children[0].position == (5, 0)
    assert board.children[1].children[1].position == (0, 0)
    assert board.children[1].children[2].position == (0, 5)
    assert board.children[1].children[3].position == (5, 5)


def test_JEN_swap_vertical() -> None:
    board = Block((0, 0), 20, None, 0, 2)

    child1 = Block((10, 0), 10, None, 1, 2)
    child2 = Block((0, 0), 10, (10, 20, 30), 1, 2)
    child3 = Block((0, 10), 10, (100, 200, 300), 1, 2)
    child4 = Block((10, 10), 10, (1000, 2000, 3000), 1, 2)

    child11 = Block((15, 0), 5, (1, 2, 3), 2, 2)
    child12 = Block((10, 0), 5, (11, 22, 33), 2, 2)
    child13 = Block((10, 5), 5, (111, 222, 333), 2, 2)
    child14 = Block((15, 5), 5, (1111, 2222, 3333), 2, 2)

    child1.children = [child11, child12, child13, child14]

    board.children = [child1, child2, child3, child4]

    board.swap(1)

    assert board.children[2].colour == (10, 20, 30)
    assert board.children[3].colour is None
    assert board.children[1].colour == (100, 200, 300)
    assert board.children[0].colour == (1000, 2000, 3000)
    assert board.children[3].children[0].colour == (1, 2, 3)
    assert board.children[3].children[1].colour == (11, 22, 33)
    assert board.children[3].children[2].colour == (111, 222, 333)
    assert board.children[3].children[3].colour == (1111, 2222, 3333)

    assert board.children[0].position == (10, 0)
    assert board.children[1].position == (0, 0)
    assert board.children[2].position == (0, 10)
    assert board.children[3].position == (10, 10)
    assert board.children[3].children[0].position == (15, 10)
    assert board.children[3].children[1].position == (10, 10)
    assert board.children[3].children[2].position == (10, 15)
    assert board.children[3].children[3].position == (15, 15)


def test_JEN_rotate_1() -> None:
    board = Block((0, 0), 20, None, 0, 2)

    child1 = Block((10, 0), 10, None, 1, 2)
    child2 = Block((0, 0), 10, (10, 20, 30), 1, 2)
    child3 = Block((0, 10), 10, (100, 200, 300), 1, 2)
    child4 = Block((10, 10), 10, (1000, 2000, 3000), 1, 2)

    child11 = Block((15, 0), 5, (1, 2, 3), 2, 2)
    child12 = Block((10, 0), 5, (11, 22, 33), 2, 2)
    child13 = Block((10, 5), 5, (111, 222, 333), 2, 2)
    child14 = Block((15, 5), 5, (1111, 2222, 3333), 2, 2)

    child1.children = [child11, child12, child13, child14]

    board.children = [child1, child2, child3, child4]

    board.rotate(1)

    assert board.children[0].colour == (10, 20, 30)
    assert board.children[1].colour == (100, 200, 300)
    assert board.children[3].colour is None
    assert board.children[2].colour == (1000, 2000, 3000)
    assert board.children[3].children[0].colour == (11, 22, 33)
    assert board.children[3].children[1].colour == (111, 222, 333)
    assert board.children[3].children[2].colour == (1111, 2222, 3333)
    assert board.children[3].children[3].colour == (1, 2, 3)

    assert board.children[0].position == (10, 0)
    assert board.children[1].position == (0, 0)
    assert board.children[2].position == (0, 10)
    assert board.children[3].position == (10, 10)
    assert board.children[3].children[0].position == (15, 10)
    assert board.children[3].children[1].position == (10, 10)
    assert board.children[3].children[2].position == (10, 15)
    assert board.children[3].children[3].position == (15, 15)


def test_smash() -> None:
    block = Block((0, 0), 750, (0, 0, 0), 0, 10)
    block.smash()
    lst = block.children
    assert lst != []
    if lst[0].children == []:
        assert lst[0].colour in COLOUR_LIST
    else:
        assert lst[0].colour is None


def test_generate_goals() -> None:
    lst = generate_goals(2)
    assert len(lst) == 2
    assert lst[0] != lst[1]
    t1 = type(lst[0])
    t2 = type(lst[1])
    assert t1 == t2
    goals = generate_goals(3)
    assert goals[1].colour in COLOUR_LIST


def test_get_block() -> None:
    block = Block((0, 0), 16, None, 0, 5)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 5)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 5)
    b3 = Block((0, 8), 8, None, 1, 5)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 5)
    block.children = [b1, b2, b3, b4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 5)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 5)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 5)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 5)
    b3.children = [b31, b32, b33, b34]
    x = _get_block(block, (3, 7), 2)
    y = _get_block(block, (7, 10), 2)
    a = _get_block(block, (8, 8), 1)
    b = _get_block(block, (16, 8), 1)
    z = _get_block(block, (15, 13), 5)
    assert b is None
    assert a.position == (8, 8)
    assert y.position == (4, 8)
    assert x.position == (0, 0)
    assert z.position == (8, 8)


def test_create_players() -> None:
    lst = create_players(1, 1, [3, 1])
    assert len(lst) == 4
    assert isinstance(lst[0], HumanPlayer)
    assert isinstance(lst[1], RandomPlayer)
    assert isinstance(lst[2], SmartPlayer)


def test_JEN_update_children_positions() -> None:
    block = Block((0, 0), 16, None, 0, 5)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 5)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 5)
    b3 = Block((0, 8), 8, None, 1, 5)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 5)
    block.children = [b1, b2, b3, b4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 5)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 5)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 5)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 5)
    b3.children = [b31, b32, b33, b34]
    # noinspection PyProtectedMember
    block._update_children_positions((2, 5))
    assert b33.position == (2, 17)
    assert b34.position == (6, 17)
    assert b1.position == (10, 5)
    assert block.position == (2, 5)

def test_JEN_block_to_squares() -> None:
    block1 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, None, 1, 2)
    c4 = Block((8, 8), 8, None, 1, 2)
    block1.children = [c1, c2, c3, c4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    c3.children = [b31, b32, b33, b34]
    b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
    b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
    b43 = Block((8, 12), 4, (255, 211, 92), 2, 2)
    b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
    c4.children = [b41, b42, b43, b44]
    lst = _block_to_squares(block1)
    assert ((1, 128, 181), (4, 8), 4) in lst

def test_JEN_swap() -> None:
    block = Block((0, 0), 16, (1, 128, 181), 0, 2)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    b3 = Block((0, 8), 8, (1, 128, 181), 1, 2)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 2)
    block.children = [b1, b2, b3, b4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    b3.children = [b31, b32, b33, b34]
    assert b31.swap(0) is False
    assert b4.swap(1) is False
    assert b3.swap(0)
    assert b32.position == (4, 8)
    assert block.swap(1)
    assert b32.position == (4, 0)


def test_JEN_rotate() -> None:
    block = Block((0, 0), 16, (1, 128, 181), 0, 2)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    b3 = Block((0, 8), 8, (1, 128, 181), 1, 2)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 2)
    block.children = [b1, b2, b3, b4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    b3.children = [b31, b32, b33, b34]
    assert b31.rotate(1) is False
    assert b4.rotate(3) is False
    assert b3.rotate(1)
    assert b32.position == (4, 8)
    assert block.rotate(3)
    assert b32.position == (8, 8)

def test_JEN_paint() -> None:
    block = Block((0, 0), 16, (1, 128, 181), 0, 2)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    b3 = Block((0, 8), 8, (1, 128, 181), 1, 2)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 2)
    block.children = [b1, b2, b3, b4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    b3.children = [b31, b32, b33, b34]
    color = (255, 211, 92)
    assert block.paint(color) is False
    assert b2.paint(color) is False
    assert b33.paint(color) is False
    assert b31.paint(color) is True
    assert b31.colour == color


def test_JEN_combine() -> None:
    block = Block((0, 0), 16, (1, 128, 181), 0, 2)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    b3 = Block((0, 8), 8, (1, 128, 181), 1, 2)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 2)
    block.children = [b1, b2, b3, b4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    b3.children = [b31, b32, b33, b34]
    b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
    b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
    b43 = Block((8, 12), 4, (255, 211, 92), 2, 2)
    b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
    b4.children = [b41, b42, b43, b44]
    assert b34.combine() is False
    assert block.combine() is False
    assert b3.combine()
    assert b4.combine() is False
    assert block.combine
    assert block.combine() is False

def test_JEN_create_copy() -> None:
    block = Block((0, 0), 16, None, 0, 5)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 5)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 5)
    b3 = Block((0, 8), 8, None, 1, 5)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 5)
    block.children = [b1, b2, b3, b4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 5)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 5)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 5)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 5)
    b3.children = [b31, b32, b33, b34]
    b = block.create_copy()
    assert id(b) != id(block)
    assert b.position == block.position
    assert b.size == block.size
    assert b.max_depth == block.max_depth
    assert b.level == block.level
    assert b.colour == block.colour
    assert b.children == block.children
    assert id(b.children[1]) != id(b2)
    assert b.children[1].position == b2.position
    assert b.children[1].size == b2.size
    assert b.children[1].max_depth == b2.max_depth
    assert b.children[1].level == b2.level
    assert b.children[1].colour == b2.colour
    assert id(b.children[2].children[0]) != id(b31)
    assert b.children[2].children[0].position == b31.position
    assert b.children[2].children[0].size == b31.size
    assert b.children[2].children[0].max_depth == b31.max_depth
    assert b.children[2].children[0].level == b31.level
    assert b.children[2].children[0].colour == b31.colour

def test_JEN_flatten() -> None:
    blocky = Block((0, 0), 16, (1, 128, 181), 0, 0)
    assert _flatten(blocky) == [[(1, 128, 181)]]
    block = Block((0, 0), 16, None, 0, 1)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 1)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 1)
    b3 = Block((0, 8), 8, (1, 128, 181), 1, 1)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 1)
    block.children = [b1, b2, b3, b4]
    assert _flatten(block) == [[(199, 44, 58), (1, 128, 181)], [(1, 128, 181),
                                                                (255, 211, 92)]]
    block1 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, None, 1, 2)
    c4 = Block((8, 8), 8, None, 1, 2)
    block1.children = [c1, c2, c3, c4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    c3.children = [b31, b32, b33, b34]
    b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
    b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
    b43 = Block((8, 12), 4, (255, 211, 92), 2, 2)
    b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
    c4.children = [b41, b42, b43, b44]
    block2 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, (255, 211, 92), 1, 2)
    c4 = Block((8, 8), 8, (1, 128, 181), 1, 2)
    block2.children = [c1, c2, c3, c4]
    assert len(_flatten(block1)) == len(_flatten(block2))
    assert _flatten(block1) == [[(199, 44, 58), (199, 44, 58), (199, 44, 58),
                                 (255, 211, 92)], [(199, 44, 58), (199, 44, 58),
                                                   (1, 128, 181), (199, 44, 58)],
                                [(1, 128, 181), (1, 128, 181), (199, 44, 58),
                                 (255, 211, 92)], [(1, 128, 181), (1, 128, 181),
                                                   (255, 211, 92), (199, 44, 58)]]
    assert _flatten(block2) == [[(199, 44, 58), (199, 44, 58), (255, 211, 92), (255, 211, 92)],
                                [(199, 44, 58), (199, 44, 58), (255, 211, 92), (255, 211, 92)],
                                [(1, 128, 181), (1, 128, 181), (1, 128, 181), (1, 128, 181)],
                                [(1, 128, 181), (1, 128, 181), (1, 128, 181), (1, 128, 181)]]


def test_JEN_score_perimeter_goal() -> None:
    block1 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, None, 1, 2)
    c4 = Block((8, 8), 8, None, 1, 2)
    block1.children = [c1, c2, c3, c4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    c3.children = [b31, b32, b33, b34]
    b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
    b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
    b43 = Block((8, 12), 4, (255, 211, 92), 2, 2)
    b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
    c4.children = [b41, b42, b43, b44]
    block2 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, (255, 211, 92), 1, 2)
    c4 = Block((8, 8), 8, (1, 128, 181), 1, 2)
    block2.children = [c1, c2, c3, c4]
    block3 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, None, 1, 2)
    c4 = Block((8, 8), 8, (199, 44, 58), 1, 2)
    block3.children = [c1, c2, c3, c4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (0, 0, 0), 2, 2)
    c3.children = [b31, b32, b33, b34]
    b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
    b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
    b43 = Block((8, 12), 4, (0, 0, 0), 2, 2)
    b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
    c4.children = [b41, b42, b43, b44]
    goal1 = PerimeterGoal((199, 44, 58))
    goal2 = PerimeterGoal((255, 211, 92))
    goal3 = PerimeterGoal((0, 0, 0))
    assert goal1.score(block1) == 8
    assert goal2.score(block1) == 4
    assert goal2.score(block2) == 4
    assert goal3.score(block3) == 2
    assert goal3.score(block1) == 0


def test_JEN_undiscovered_blob_size() -> None:
    board = [[(199, 44, 58), (199, 44, 58), (199, 44, 58),
              (255, 211, 92)], [(199, 44, 58), (199, 44, 58),
                                (1, 128, 181), (199, 44, 58)],
             [(1, 128, 181), (1, 128, 181), (199, 44, 58),
              (255, 211, 92)], [(1, 128, 181), (1, 128, 181),
                                (255, 211, 92), (199, 44, 58)]]
    visited = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
    pos = (0, 2)
    goal1 = BlobGoal((199, 44, 58))
    result = goal1._undiscovered_blob_size(pos, board, visited)
    assert result == 5
    assert visited[1][1] == 1

def test_JEN_undiscovered_blob_size2() -> None:
    blocky = Block((0, 0), 16, (199, 44, 58), 0, 1)
    by = _flatten(blocky)
    block = Block((0, 0), 16, None, 0, 1)
    b1 = Block((8, 0), 8, (1, 128, 181), 1, 1)
    b2 = Block((0, 0), 8, (199, 44, 58), 1, 1)
    b3 = Block((0, 8), 8, (1, 128, 181), 1, 1)
    b4 = Block((8, 8), 8, (255, 211, 92), 1, 1)
    block.children = [b1, b2, b3, b4]
    fb = _flatten(block)
    goal1 = BlobGoal((199, 44, 58))
    goal2 = BlobGoal((1, 128, 181))
    v = [[-1, -1], [-1, -1]]
    b = [[-1, -1], [-1, -1]]
    assert goal1._undiscovered_blob_size((0, 0), by, v) == 4
    assert goal2._undiscovered_blob_size((0, 1), fb, b) == 1

def test_JEN_score_blob_goal() -> None:
    block1 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, None, 1, 2)
    c4 = Block((8, 8), 8, None, 1, 2)
    block1.children = [c1, c2, c3, c4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    c3.children = [b31, b32, b33, b34]
    b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
    b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
    b43 = Block((8, 12), 4, (255, 211, 92), 2, 2)
    b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
    c4.children = [b41, b42, b43, b44]
    block2 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, (255, 211, 92), 1, 2)
    c4 = Block((8, 8), 8, (1, 128, 181), 1, 2)
    block2.children = [c1, c2, c3, c4]
    block3 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, None, 1, 2)
    c4 = Block((8, 8), 8, (199, 44, 58), 1, 2)
    block3.children = [c1, c2, c3, c4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
    b34 = Block((4, 12), 4, (0, 0, 0), 2, 2)
    c3.children = [b31, b32, b33, b34]
    b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
    b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
    b43 = Block((8, 12), 4, (0, 0, 0), 2, 2)
    b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
    c4.children = [b41, b42, b43, b44]
    goal1 = BlobGoal((199, 44, 58))
    goal2 = BlobGoal((255, 211, 92))
    goal3 = BlobGoal((0, 0, 0))
    block4 = Block((0, 0), 16, None, 0, 2)
    c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
    c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
    c3 = Block((0, 8), 8, None, 1, 2)
    c4 = Block((8, 8), 8, None, 1, 2)
    block4.children = [c1, c2, c3, c4]
    b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
    b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
    b33 = Block((0, 12), 4, (199, 44, 58), 2, 2)
    b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
    c3.children = [b31, b32, b33, b34]
    b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
    b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
    b43 = Block((8, 12), 4, (199, 44, 58), 2, 2)
    b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
    c4.children = [b41, b42, b43, b44]
    assert goal1.score(block1) == 5
    assert goal1.score(block4) == 10
    assert goal2.score(block1) == 1
    assert goal2.score(block2) == 4
    assert goal3.score(block3) == 2
    assert goal3.score(block1) == 0



if __name__ == '__main__':
    pytest.main(['example_tests.py'])
