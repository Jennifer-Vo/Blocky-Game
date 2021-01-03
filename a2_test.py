from blocky import _block_to_squares
from block import Block
from goal import generate_goals, _flatten, PerimeterGoal, BlobGoal
from player import _get_block, create_players, HumanPlayer, RandomPlayer, SmartPlayer
from settings import COLOUR_LIST
from random import randint
from hypothesis import given
from hypothesis.strategies import integers


def test_block_to_squares() -> None:
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


# def test_make_children() -> None:
#     block = Block((0, 0), 750, (0, 0, 0), 0, 10)
#     lst = block._make_children()
#     assert lst[0].position == (375, 0)
#     assert lst[0].size == 375
#     assert lst[0].colour is None


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


def test_update_children_positions() -> None:
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


def test_swap() -> None:
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


def test_rotate() -> None:
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


# def test_combine_helper() -> None:
#     block = Block((0, 0), 16, (1, 128, 181), 0, 1)
#     b1 = Block((8, 0), 8, (1, 128, 181), 1, 1)
#     b2 = Block((0, 0), 8, (199, 44, 58), 1, 1)
#     b3 = Block((0, 8), 8, (1, 128, 181), 1, 1)
#     b4 = Block((8, 8), 8, (255, 211, 92), 1, 1)
#     block.children = [b1, b2, b3, b4]
#     assert block._combine_helper() == (1, 128, 181)


def test_paint() -> None:
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


def test_combine() -> None:
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

def test_create_copy() -> None:
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

def test_flatten() -> None:
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


def test_score_perimeter_goal() -> None:
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


def test_undiscovered_blob_size() -> None:
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


def test_undiscovered_blob_size2() -> None:
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


def test_score_blob_goal() -> None:
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

# @given(numbers=integers(min_value=1, max_value=1000))
# def test_random_player_generate_moves(numbers) -> None:
#     block = Block((0, 0), 16, None, 0, 2)
#     b1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
#     b2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
#     b3 = Block((0, 8), 8, (1, 128, 181), 1, 2)
#     b4 = Block((8, 8), 8, (255, 211, 92), 1, 2)
#     block.children = [b1, b2, b3, b4]
#     for _ in range(numbers):
#         i = randint(0, 3)
#         colours = [(1, 128, 181), (199, 44, 58), (255, 211, 92), (234, 62, 112)]
#         colour = colours[i]
#         i2 = randint(0, 1)
#         if i2 == 0:
#             g = PerimeterGoal(colour)
#         else:
#             g = BlobGoal(colour)
#         p1 = RandomPlayer(1, g)
#         p1._proceed = True
#         m = p1.generate_move(block)
#         x = [None, ('rotate', 1), ('rotate', 3), ('swap', 0), ('swap', 1),
#              ('smash', None), ('combine', None), ('paint', None), ('pass', None)]
#         assert m[:2] in x
#         assert block.children == [b1, b2, b3, b4]
#         assert b1 == Block((8, 0), 8, (1, 128, 181), 1, 2)
#         assert b2 == Block((0, 0), 8, (199, 44, 58), 1, 2)
#         assert b3 == Block((0, 8), 8, (1, 128, 181), 1, 2)
#         assert b4 == Block((8, 8), 8, (255, 211, 92), 1, 2)
#         assert m[-1] == _get_block(block, m[-1].position, m[-1].level)
#         assert p1._proceed is False
#         assert block.position == (0, 0)
#         assert block.children[0].position == (8, 0)
#         assert block.children[1].position == (0, 0)
#         assert block.children[2].position == (0, 8)
#         assert block.children[3].position == (8, 8)
#         assert block.colour == None
#         assert block.children[0].colour == (1, 128, 181)
#         assert block.children[1].colour == (199, 44, 58)
#         assert block.children[2].colour == (1, 128, 181)
#         assert block.children[3].colour == (255, 211, 92)
#         assert block.max_depth == 2
#         assert len(block.children) == 4
#         assert len(block.children[0].children) == 0
#         assert len(block.children[1].children) == 0
#         assert len(block.children[2].children) == 0
#         assert len(block.children[3].children) == 0

# @given(numbers=integers(min_value=1, max_value=1000))
# def test_random_player_generate_moves2(numbers) -> None:
#     block1 = Block((0, 0), 16, None, 0, 2)
#     c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
#     c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
#     c3 = Block((0, 8), 8, None, 1, 2)
#     c4 = Block((8, 8), 8, None, 1, 2)
#     block1.children = [c1, c2, c3, c4]
#     b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
#     b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
#     b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
#     b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
#     c3.children = [b31, b32, b33, b34]
#     b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
#     b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
#     b43 = Block((8, 12), 4, (255, 211, 92), 2, 2)
#     b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
#     c4.children = [b41, b42, b43, b44]
#     for _ in range(numbers):
#         i = randint(0, 3)
#         colours = [(1, 128, 181), (199, 44, 58), (255, 211, 92), (234, 62, 112)]
#         colour = colours[i]
#         i2 = randint(0, 1)
#         if i2 == 0:
#             g = PerimeterGoal(colour)
#         else:
#             g = BlobGoal(colour)
#         p1 = RandomPlayer(1, g)
#         p1._proceed = True
#         m = p1.generate_move(block1)
#         assert p1._valid_move(m[2], (m[0], m[1]))
#         assert isinstance(m, tuple)

# @given(numbers=integers(min_value=1, max_value=100))
# def test_smart_player_generate_moves(numbers) -> None:
#     block = Block((0, 0), 16, None, 0, 2)
#     b1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
#     b2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
#     b3 = Block((0, 8), 8, (1, 128, 181), 1, 2)
#     b4 = Block((8, 8), 8, (255, 211, 92), 1, 2)
#     block.children = [b1, b2, b3, b4]
#     for _ in range(numbers):
#         i = randint(0, 3)
#         colours = [(1, 128, 181), (199, 44, 58), (255, 211, 92), (234, 62, 112)]
#         colour = colours[i]
#         i2 = randint(0, 1)
#         if i2 == 0:
#             g = PerimeterGoal(colour)
#         else:
#             g = BlobGoal(colour)
#         p1 = SmartPlayer(1, g, 25)
#         p1._proceed = True
#         m = p1.generate_move(block)
#         x = [None, ('rotate', 1), ('rotate', 3), ('swap', 0), ('swap', 1),
#              ('smash', None), ('combine', None), ('paint', None), ('pass', None)]
#         assert m[:2] in x
#         assert block.children == [b1, b2, b3, b4]
#         assert b1 == Block((8, 0), 8, (1, 128, 181), 1, 2)
#         assert b2 == Block((0, 0), 8, (199, 44, 58), 1, 2)
#         assert b3 == Block((0, 8), 8, (1, 128, 181), 1, 2)
#         assert b4 == Block((8, 8), 8, (255, 211, 92), 1, 2)
#         assert m[-1] == _get_block(block, m[-1].position, m[-1].level)
#         assert p1._proceed is False
#         assert block.position == (0, 0)
#         assert block.children[0].position == (8, 0)
#         assert block.children[1].position == (0, 0)
#         assert block.children[2].position == (0, 8)
#         assert block.children[3].position == (8, 8)
#         assert block.colour == None
#         assert block.children[0].colour == (1, 128, 181)
#         assert block.children[1].colour == (199, 44, 58)
#         assert block.children[2].colour == (1, 128, 181)
#         assert block.children[3].colour == (255, 211, 92)
#         assert block.max_depth == 2
#         assert len(block.children) == 4
#         assert len(block.children[0].children) == 0
#         assert len(block.children[1].children) == 0
#         assert len(block.children[2].children) == 0
#         assert len(block.children[3].children) == 0


# def test_smart_player_generate_moves2() -> None:
#     block1 = Block((0, 0), 16, None, 0, 2)
#     c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
#     c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
#     c3 = Block((0, 8), 8, None, 1, 2)
#     c4 = Block((8, 8), 8, None, 1, 2)
#     block1.children = [c1, c2, c3, c4]
#     b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
#     b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
#     b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
#     b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
#     c3.children = [b31, b32, b33, b34]
#     b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
#     b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
#     b43 = Block((8, 12), 4, (255, 211, 92), 2, 2)
#     b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
#     c4.children = [b41, b42, b43, b44]
#     i = randint(0, 3)
#     colours = [(1, 128, 181), (199, 44, 58), (255, 211, 92), (234, 62, 112)]
#     colour = colours[i]
#     i2 = randint(0, 1)
#     if i2 == 0:
#         g = PerimeterGoal(colour)
#     else:
#         g = BlobGoal(colour)
#     p1 = SmartPlayer(1, g, 25)
#     p1._proceed = True
#     m = p1.generate_move(block1)
#     assert (p1._valid_move(m[2], (m[0], m[1]))) or (m[0] == 'pass')
#     assert isinstance(m, tuple)


# @given(numbers=integers(min_value=1, max_value=50))
# def test_smart_player_generate_moves3(numbers: int) -> None:
#     for _ in range(numbers):
#         block1 = Block((0, 0), 16, None, 0, 2)
#         c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
#         c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
#         c3 = Block((0, 8), 8, None, 1, 2)
#         c4 = Block((8, 8), 8, None, 1, 2)
#         block1.children = [c1, c2, c3, c4]
#         b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
#         b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
#         b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
#         b34 = Block((4, 12), 4, (234, 62, 112), 2, 2)
#         c3.children = [b31, b32, b33, b34]
#         b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
#         b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
#         b43 = Block((8, 12), 4, (234, 62, 112), 2, 2)
#         b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
#         c4.children = [b41, b42, b43, b44]
#         i = randint(0, 3)
#         colours = [(1, 128, 181), (199, 44, 58), (255, 211, 92), (234, 62, 112)]
#         colour = colours[i]
#         i2 = randint(0, 1)
#         if i2 == 0:
#             g = PerimeterGoal(colour)
#         else:
#             g = BlobGoal(colour)
#         p1 = SmartPlayer(1, g, 25)
#         before = g.score(block1)
#         p1._proceed = True
#         item = p1.generate_move(block1)
#         if item[0] == 'rotate':
#             item[2].rotate(item[1])
#             after = g.score(block1)
#             assert after > before
#         elif item[0] == 'swap':
#             item[2].swap(item[1])
#             after = g.score(block1)
#             assert after > before
#         elif item[0] == 'smash':
#             item[2].smash()
#             after = g.score(block1)
#             assert after >= before
#         elif item[0] == 'combine':
#             item[2].combine()
#             after = g.score(block1)
#             assert after > before
#         elif item[0] == 'paint':
#             item[2].paint(g.colour)
#             after = g.score(block1)
#             assert after > before
#         else:
#             assert item[0] == 'pass'
#             assert before == g.score(block1)


# @given(numbers=integers(min_value=1, max_value=1000))
# def test_choose_random_block(numbers) -> None:
#     block1 = Block((0, 0), 16, None, 0, 2)
#     c1 = Block((8, 0), 8, (1, 128, 181), 1, 2)
#     c2 = Block((0, 0), 8, (199, 44, 58), 1, 2)
#     c3 = Block((0, 8), 8, None, 1, 2)
#     c4 = Block((8, 8), 8, None, 1, 2)
#     block1.children = [c1, c2, c3, c4]
#     b31 = Block((4, 8), 4, (1, 128, 181), 2, 2)
#     b32 = Block((0, 8), 4, (199, 44, 58), 2, 2)
#     b33 = Block((0, 12), 4, (255, 211, 92), 2, 2)
#     b34 = Block((4, 12), 4, (199, 44, 58), 2, 2)
#     c3.children = [b31, b32, b33, b34]
#     b41 = Block((12, 8), 4, (255, 211, 92), 2, 2)
#     b42 = Block((8, 8), 4, (199, 44, 58), 2, 2)
#     b43 = Block((8, 12), 4, (255, 211, 92), 2, 2)
#     b44 = Block((12, 12), 4, (199, 44, 58), 2, 2)
#     c4.children = [b41, b42, b43, b44]
#     for _ in range(numbers):
#         a = _choose_random_block(block1)
#         assert (a[0] in block1.children) or (a[0] is block1) or (a[0] in c3.children) or (a[0] in c4.children)
#     for _ in range(numbers):
#         b = _choose_random_block(block1)
#         assert (b[2] in b[1].children) or (b[2] is b[1]) or\
#                (b[2] in b[1].children[2].children) or (b[2] in b[1].children[3].children)


if __name__ == '__main__':
    import pytest
    pytest.main(['a2_test.py'])
