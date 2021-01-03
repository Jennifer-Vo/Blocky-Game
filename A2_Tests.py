from blocky import _block_to_squares
from block import Block
from settings import COLOUR_LIST
from goal import generate_goals, PerimeterGoal, BlobGoal, _flatten
from player import _get_block, create_players, HumanPlayer, RandomPlayer, \
    SmartPlayer
from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE

def test__block_to_squares() -> None:
    """ Test the _block_to_squares function. """
    b1 = Block((0, 0), 500, (255, 0, 0), 0, 3)

    assert _block_to_squares(b1) == [((255, 0, 0), (0, 0), 500)]

    b2 = Block((500, 0), 1000, None, 0, 2)
    b2.children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, (255, 255, 0), 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    squares2 = _block_to_squares(b2)

    assert len(squares2) == 4

    assert ((255, 0, 0), (500, 0), 500) in squares2

    assert ((255, 255, 0), (0, 0), 500) in squares2

    assert ((255, 0, 255), (0, 500), 500) in squares2

    assert ((0, 0, 255), (500, 500), 500) in squares2

    b2.children[1].colour = None
    b2.children[1].children = [Block((250, 0), 250, (0, 0, 0), 1, 2),
                               Block((0, 0), 250, (0, 255, 0), 1, 2),
                               Block((0, 250), 250, (255, 255, 255), 1, 2),
                               Block((250, 250), 250, (0, 255, 255), 1, 2)]

    squares3 = _block_to_squares(b2)

    assert len(squares3) == 7

    assert ((255, 0, 0), (500, 0), 500) in squares3

    assert ((0, 0, 0), (250, 0), 250) in squares3

    assert ((0, 255, 0), (0, 0), 250) in squares3

    assert ((255, 255, 255), (0, 250), 250) in squares3

    assert ((0, 255, 255), (250, 250), 250) in squares3

    assert ((255, 0, 255), (0, 500), 500) in squares3

    assert ((0, 0, 255), (500, 500), 500) in squares3


def test_smash() -> None:
    """ Test the smash method of BLock. """
    b1 = Block((0, 0), 500, (255, 0, 0), 0, 3)

    assert not b1.children

    assert b1.smash()

    assert len(b1.children) == 4

    assert b1.colour is None

    for child in b1.children:
        assert len(child.children) == 4 or not child.children

        assert child.colour in COLOUR_LIST or child.colour is None

    assert not b1.smash()


def test_generate_goals() -> None:
    """ Test the generate_goals function. """
    goals1 = generate_goals(1)

    assert len(goals1) == 1

    assert goals1[0].colour in COLOUR_LIST

    assert isinstance(goals1[0], PerimeterGoal) or isinstance(goals1[0],
                                                              BlobGoal)

    goals2 = generate_goals(4)

    assert len(goals2) == 4

    colours = []

    for goal in range(len(goals2)):
        assert goals2[goal].colour not in colours
        assert goals2[goal].colour in COLOUR_LIST
        assert isinstance(goals2[goal], type(goals2[goal - 1]))

        colours.append(goals2[goal].colour)


def test_perimeter_goal_description() -> None:
    """ Test the PerimeterGoal class' description method. """
    g1 = PerimeterGoal((1, 128, 181))

    assert isinstance(g1.description(), str)


def test_blob_goal_description() -> None:
    """ Test the PerimeterGoal class' description method. """
    g1 = BlobGoal((1, 128, 181))

    assert isinstance(g1.description(), str)


def test_get_block() -> None:
    """ Test the _get_block function. """
    b1 = Block((0, 0), 500, (255, 0, 0), 0, 3)

    assert _get_block(b1, (55, 75), 0) is b1

    assert _get_block(b1, (0, 0), 0) is b1

    assert _get_block(b1, (500, 425), 0) is None

    assert _get_block(b1, (55, 75), 5) is b1

    b2 = Block((0, 0), 1000, None, 0, 2)
    b2.children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, (255, 255, 0), 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    b2.children[1].colour = None

    b2.children[1].children = [Block((250, 0), 250, (0, 0, 0), 2, 2),
                               Block((0, 0), 250, (0, 255, 0), 2, 2),
                               Block((0, 250), 250, (255, 255, 255), 2, 2),
                               Block((250, 250), 250, (0, 255, 255), 2, 2)]

    assert _get_block(b2, (288, 22), 0) is b2

    assert _get_block(b2, (51, 155), 2) is b2.children[1].children[1]

    assert _get_block(b2, (51, 243), 1) is b2.children[1]

    assert _get_block(b2, (1, 1000), 1) is None

    assert _get_block(b2, (250, 1000), 1) is None

    assert _get_block(b2, (250, 16), 2) is b2.children[1].children[0]

    assert _get_block(b2, (550, 670), 2) is b2.children[3]


def test_create_players() -> None:
    """ Test the create_players function. """
    players = create_players(1, 1, [1, 3])

    assert isinstance(players[0], HumanPlayer)

    assert isinstance(players[1], RandomPlayer)

    assert isinstance(players[2], SmartPlayer)

    assert players[2]._difficulty == 1

    assert isinstance(players[3], SmartPlayer)

    assert players[3]._difficulty == 3

    for player in range(1, len(players)):
        assert players[player - 1].id < players[player].id

    players2 = create_players(1, 0, [])

    assert isinstance(players2[0], HumanPlayer)

    assert players2[0].id == 0

    players3 = create_players(0, 1, [])

    assert isinstance(players3[0], RandomPlayer)

    assert players3[0].id == 0

    players4 = create_players(0, 0, [1])

    assert isinstance(players4[0], SmartPlayer)

    assert players4[0].id == 0

    assert players4[0]._difficulty == 1

    players5 = create_players(0, 0, [])

    assert not players5


def test__update_children_positions() -> None:
    """ Test the Block class' _update_children_positions method"""
    b1 = Block((0, 0), 500, (255, 0, 0), 0, 3)

    b1._update_children_positions((50, 50))

    assert b1.position == (50, 50)

    assert not b1.children

    b2 = Block((0, 0), 1000, None, 0, 2)
    b2.children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, (255, 255, 0), 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    b2.children[0].colour = None

    b2.children[1].children = [Block((250, 0), 250, (0, 0, 0), 2, 2),
                               Block((0, 0), 250, (0, 255, 0), 2, 2),
                               Block((0, 250), 250, (255, 255, 255), 2, 2),
                               Block((250, 250), 250, (0, 255, 255), 2, 2)]

    b2._update_children_positions((500, 500))

    assert b2.position == (500, 500)

    assert b2.children[0].position == (1000, 500)

    assert b2.children[1].position == (500, 500)

    assert b2.children[1].children[0].position == (750, 500)

    assert b2.children[1].children[1].position == (500, 500)

    assert b2.children[1].children[2].position == (500, 750)

    assert b2.children[1].children[3].position == (750, 750)

    assert b2.children[2].position == (500, 1000)

    assert b2.children[3].position == (1000, 1000)


def test_swap() -> None:
    """ Test the Block class' swap method. """
    b1 = Block((0, 0), 1000, (255, 255, 255), 0, 5)

    assert not b1.swap(0)

    assert not b1.swap(1)

    b2 = Block((0, 0), 1000, None, 0, 2)
    b2.children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, None, 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    b2.children[1].children = [Block((250, 0), 250, (0, 0, 0), 2, 2),
                               Block((0, 0), 250, (0, 255, 0), 2, 2),
                               Block((0, 250), 250, (255, 255, 255), 2, 2),
                               Block((250, 250), 250, (0, 255, 255), 2, 2)]

    b2_old = Block((0, 0), 1000, None, 0, 2)

    b2_old.children = b2.children[:]

    b2_old_child_children = b2.children[1].children[:]

    assert b2.swap(1)

    assert b2.children[0] is b2_old.children[3]

    assert b2.children[0].position == (500, 0)

    assert b2.children[1] is b2_old.children[2]

    assert b2.children[1].position == (0, 0)

    assert b2.children[2] is b2_old.children[1]

    assert b2.children[2].position == (0, 500)

    assert b2.children[3] is b2_old.children[0]

    assert b2.children[3].position == (500, 500)

    assert b2.children[2].children == b2_old_child_children


def test_rotate() -> None:
    """ Test the Block class' rotate method. """
    b1 = Block((0, 0), 1000, (255, 255, 255), 0, 5)

    assert not b1.rotate(1)

    assert not b1.rotate(3)

    b2 = Block((0, 0), 1000, None, 0, 2)
    b2.children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, None, 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    b2.children[1].children = [Block((250, 0), 250, (0, 0, 0), 2, 2),
                               Block((0, 0), 250, (0, 255, 0), 2, 2),
                               Block((0, 250), 250, (255, 255, 255), 2, 2),
                               Block((250, 250), 250, (0, 255, 255), 2, 2)]

    b2_old = Block((0, 0), 1000, None, 0, 2)

    b2_old.children = b2.children[:]

    b2_old_child_children = b2.children[1].children[:]

    assert b2.rotate(3)

    assert b2.position == (0, 0)

    assert b2.children[0] is b2_old.children[3]

    assert b2.children[1] is b2_old.children[0]

    assert b2.children[2] is b2_old.children[1]

    assert b2.children[2].children[0] is b2_old_child_children[3]

    assert b2.children[2].children[1] is b2_old_child_children[0]

    assert b2.children[2].children[2] is b2_old_child_children[1]

    assert b2.children[2].children[3] is b2_old_child_children[2]

    assert b2.children[3] is b2_old.children[2]


def test_paint() -> None:
    """ Test the Block class' paint method. """
    b1 = Block((0, 0), 1000, (255, 255, 255), 0, 5)

    assert not b1.paint((0, 125, 15))

    assert b1.colour == (255, 255, 255)

    b2 = Block((0, 0), 1000, (255, 255, 255), 0, 0)

    assert b2.paint((0, 125, 15))

    assert b2.colour == (0, 125, 15)

    b3 = Block((0, 0), 1000, None, 0, 2)
    b3.children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, None, 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    b3.children[1].children = [Block((250, 0), 250, (0, 0, 0), 2, 2),
                               Block((0, 0), 250, (0, 255, 0), 2, 2),
                               Block((0, 250), 250, (255, 255, 255), 2, 2),
                               Block((250, 250), 250, (0, 255, 255), 2, 2)]

    assert not b3.paint((15, 16, 17))

    assert not b3.children[0].paint((4, 8, 12))

    assert not b3.children[1].paint((3, 9, 27))

    assert b3.children[1].children[1].paint((55, 66, 77))

    assert b3.children[1].children[1].colour == (55, 66, 77)


def test_combine() -> None:
    """ Test the Block class' combine method."""
    b1 = Block((0, 0), 1000, (255, 255, 255), 0, 5)

    assert not b1.combine()

    b2 = Block((0, 0), 1000, None, 0, 2)
    b2.children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, None, 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    b2.children[1].children = [Block((250, 0), 250, (0, 0, 0), 2, 2),
                               Block((0, 0), 250, (0, 255, 0), 2, 2),
                               Block((0, 250), 250, (0, 0, 0), 2, 2),
                               Block((250, 250), 250, (0, 0, 255), 2, 2)]

    assert b2.children[1].combine()

    assert b2.children[1].colour == (0, 0, 0)

    assert not b2.children[1].children

    assert not b2.combine()


def test__flatten() -> None:
    """ Test the _flatten function. """
    b1 = Block((0, 0), 1000, (255, 255, 255), 0, 0)

    assert _flatten(b1) == [[(255, 255, 255)]]

    b2 = Block((0, 0), 1000, (255, 255, 255), 0, 1)

    assert _flatten(b2) == [[(255, 255, 255), (255, 255, 255)],
                            [(255, 255, 255), (255, 255, 255)]]

    b3 = Block((0, 0), 1000, (255, 255, 255), 0, 3)

    assert _flatten(b3) == [[(255, 255, 255) for w in range(8)]
                            for n in range(8)]

    b4 = Block((0, 0), 1000, None, 0, 2)
    b4.children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, None, 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    b4.children[1].children = [Block((250, 0), 250, (0, 0, 0), 2, 2),
                               Block((0, 0), 250, (0, 255, 0), 2, 2),
                               Block((0, 250), 250, (0, 0, 0), 2, 2),
                               Block((250, 250), 250, (0, 0, 255), 2, 2)]

    assert _flatten(b4.children[1]) == [[(0, 255, 0), (0, 0, 0)],
                                        [(0, 0, 0), (0, 0, 255)]]

    assert _flatten(b4) == [
        [(0, 255, 0), (0, 0, 0), (255, 0, 255), (255, 0, 255)],
        [(0, 0, 0), (0, 0, 255), (255, 0, 255), (255, 0, 255)],
        [(255, 0, 0), (255, 0, 0), (0, 0, 255), (0, 0, 255)],
        [(255, 0, 0), (255, 0, 0), (0, 0, 255), (0, 0, 255)]]

    b5 = Block((0, 0), 1000, None, 0, 2)
    b5.children = [Block((500, 0), 500, (0, 255, 0), 1, 2),
                   Block((0, 0), 500, (0, 0, 0), 1, 2),
                   Block((0, 500), 500, (255, 255, 255), 1, 2),
                   Block((500, 500), 500, (0, 255, 0), 1, 2)]

    assert _flatten(b5) == [[(0, 0, 0), (0, 0, 0),
                             (255, 255, 255), (255, 255, 255)],
                            [(0, 0, 0), (0, 0, 0),
                             (255, 255, 255), (255, 255, 255)],
                            [(0, 255, 0), (0, 255, 0),
                             (0, 255, 0), (0, 255, 0)],
                            [(0, 255, 0), (0, 255, 0),
                             (0, 255, 0), (0, 255, 0)]]


def test_perimeter_goal_score() -> None:
    """ Test the score method of the PerimeterGoal class. """
    goal = PerimeterGoal((255, 255, 255))

    assert goal.score(Block((0, 0), 1000, (255, 255, 255), 0, 0)) == 4

    assert goal.score(Block((0, 0), 1000, (0, 255, 255), 0, 0)) == 0

    goal2 = PerimeterGoal((0, 0, 0))
    b1 = Block((1000, 0), 500, None, 0, 2)
    b1.children = [Block((1250, 0), 250, (0, 0, 0), 1, 2),
                   Block((0, 0), 250, (0, 0, 0), 1, 2),
                   Block((0, 1250), 250, (55, 0, 0), 1, 2),
                   Block((1250, 1250), 250, None, 1, 2)]
    b1.children[3].children = [Block((1375, 0), 125, (0, 255, 0), 2, 2),
                               Block((1250, 0), 125, (0, 0, 0), 2, 2),
                               Block((1250, 1375), 125, (155, 0, 0), 2, 2),
                               Block((1375, 1375), 125, (0, 0, 0), 2, 2)]

    assert goal.score(b1) == 0
    assert goal2.score(b1) == 10


def test__undiscovered_blob_size() -> None:
    """ Test the BlobGoal class' _undiscovered_blob_size method. """
    goal1 = BlobGoal((0, 0, 0))
    pos1 = (0, 0)
    board1 = [[(0, 0, 0), (0, 0, 0)],
              [(0, 0, 0), (0, 0, 0)]]
    visited1 = [[-1, -1],
                [-1, -1]]

    assert goal1._undiscovered_blob_size(pos1, board1, visited1) == 4

    assert visited1 == [[1, 1], [1, 1]]

    assert goal1._undiscovered_blob_size(pos1, board1, visited1) == 0

    goal2 = BlobGoal((0, 255, 0))
    pos2 = (0, 0)
    board2 = [[(0, 255, 0), (0, 0, 0)],
              [(0, 0, 0), (0, 255, 0)]]
    visited2 = [[-1, -1],
                [-1, -1]]

    assert goal2._undiscovered_blob_size(pos2, board2, visited2) == 1

    assert visited2 == [[1, 0], [0, -1]]

    assert goal2._undiscovered_blob_size(pos2, board2, visited2) == 0

    goal3 = goal1  # (0, 0, 0)
    pos3 = (1, 1)
    board3 = [[(0, 255, 0), (0, 0, 0), (0, 255, 0)],
              [(0, 0, 0), (0, 255, 0), (0, 255, 0)],
              [(0, 255, 0), (0, 0, 0), (0, 255, 0)]]
    visited3 = [[-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1]]

    assert goal3._undiscovered_blob_size(pos3, board3, visited3) == 0

    assert visited3 == [[-1, -1, -1], [-1, 0, -1], [-1, -1, -1]]

    assert goal3._undiscovered_blob_size(pos3, board3, visited3) == 0

    goal4 = goal1  # (0, 0, 0)
    pos4 = (0, 1)
    board4 = [[(0, 0, 0), (0, 0, 0), (0, 255, 0)],
              [(0, 0, 0), (0, 255, 0), (0, 255, 0)],
              [(0, 0, 0), (0, 0, 0), (0, 255, 0)]]
    visited4 = [[1, -1, -1],
                [-1, -1, -1],
                [-1, 1, -1]]

    assert goal4._undiscovered_blob_size(pos4, board4, visited4) == 1

    assert visited4 == [[1, 1, 0], [-1, 0, -1], [-1, 1, -1]]

    assert goal4._undiscovered_blob_size(pos4, board4, visited4) == 0


def test_blob_goal_score() -> None:
    """ Test the BlobGoal class' score method. """
    goal = BlobGoal((255, 255, 255))
    assert goal.score(Block((0, 0), 250, (255, 255, 255), 0, 0)) == 1

    board = Block((0, 0), 1000, None, 0, 2)
    board.children = [Block((500, 0), 500, (0, 255, 0), 1, 2),
                      Block((0, 0), 500, (0, 0, 0), 1, 2),
                      Block((0, 500), 500, (255, 255, 255), 1, 2),
                      Block((500, 500), 500, (0, 255, 0), 1, 2)]
    assert goal.score(board) == 4

    board.children[3].children = [Block((750, 500), 250, (0, 0, 0), 2, 2),
                                  Block((500, 500), 250, (0, 0, 0), 2, 2),
                                  Block((500, 750), 250, (55, 0, 0), 2, 2),
                                  Block((750, 750), 250, (0, 0, 0), 2, 2)]
    board.children[3].colour = None

    assert goal.score(board) == 4

    goal2 = BlobGoal((0, 0, 0))

    assert goal2.score(board) == 4

    board.children[0].colour = (0, 0, 0)

    assert goal2.score(board) == 11


def test_random_player__init__() -> None:
    """ Test the __init__ method of the RandomPlayer class. """
    goal = BlobGoal((0, 0, 0))
    player = RandomPlayer(1, goal)

    assert player.id == 1

    assert player.goal is goal

    assert not player._proceed


def test_create_copy() -> None:
    """ Test the Block class' create_copy method. """
    b1 = Block((0, 0), 1000, (0, 0, 0), 0, 2)

    b1_copy = b1.create_copy()

    assert b1_copy is not b1

    assert b1_copy == b1

    assert b1.position == (0, 0) and b1.size == 1000 and b1.colour == (0, 0, 0) \
           and b1.level == 0 and b1.max_depth == 2 and not b1.children

    b2 = Block((0, 0), 1000, None, 0, 2)
    b2_children = [Block((500, 0), 500, (255, 0, 0), 1, 2),
                   Block((0, 0), 500, None, 1, 2),
                   Block((0, 500), 500, (255, 0, 255), 1, 2),
                   Block((500, 500), 500, (0, 0, 255), 1, 2)]

    b2.children = b2_children[:]

    b2.children[1].children = [Block((250, 0), 250, (0, 0, 0), 2, 2),
                               Block((0, 0), 250, (0, 255, 0), 2, 2),
                               Block((0, 250), 250, (0, 0, 0), 2, 2),
                               Block((250, 250), 250, (0, 0, 255), 2, 2)]

    b2_copy = b2.create_copy()

    assert b2_copy is not b2

    assert b2_copy == b2

    assert b2.position == (0, 0) and b2.size == 1000 and b2.colour is None \
           and b2.level == 0 and b2.max_depth == 2 and b2.children == b2_children

    assert b2_copy.children is not b2.children

    for n in range(4):
        assert b2_copy.children[n] is not b2.children[n]

        assert b2_copy.children[1].children[n] is not b2.children[1].children[n]


def test_random_player_generate_move() -> None:
    """ Test the RandomPlayer class' generate_move method. """
    goal = BlobGoal((0, 0, 0))
    player1 = RandomPlayer(1, goal)
    player1._proceed = True
    b1 = Block((0, 0), 1000, (0, 0, 0), 0, 2)

    move1 = player1.generate_move(b1)

    assert isinstance(move1, tuple) and isinstance(move1[0], str) and \
           (isinstance(move1[1], int) or move1[1] is None) and \
           isinstance(move1[2], Block)

    if move1[0:2] == ('rotate', 1):
        assert move1[2].rotate(1)
    elif move1[0:2] == ('rotate', 3):
        assert move1[2].rotate(3)
    elif move1[0:2] == ('swap', 0):
        assert move1[2].swap(0)
    elif move1[0:2] == ('swap', 1):
        assert move1[2].swap(1)
    elif move1[0:2] == ('smash', None):
        assert move1[2].smash()
    elif move1[0:2] == ('paint', None):
        assert move1[2].paint(self.goal.colour)
    elif move1[0:2] == ('combine', None):
        assert move1[2].combine()
    else:
        assert False


def test_smart_player_generate_move() -> None:
    """ Test the SmartPlayer class' generate_move method. """
    goal = BlobGoal((0, 0, 0))
    player1 = SmartPlayer(1, goal, 4)
    player1._proceed = True
    b1 = Block((0, 0), 1000, (0, 0, 0), 0, 2)

    b1_score = goal.score(b1)

    move1 = player1.generate_move(b1)

    assert isinstance(move1, tuple) and isinstance(move1[0], str) and \
           (isinstance(move1[1], int) or move1[1] is None) and \
           isinstance(move1[2], Block)

    if move1[0:2] == ('rotate', 1):
        assert move1[2].rotate(1)
        assert goal.score(b1) > b1_score
    elif move1[0:2] == ('rotate', 3):
        assert move1[2].rotate(3)
        assert goal.score(b1) > b1_score
    elif move1[0:2] == ('swap', 0):
        assert move1[2].swap(0)
        assert goal.score(b1) > b1_score
    elif move1[0:2] == ('swap', 1):
        assert move1[2].swap(1)
        assert goal.score(b1) > b1_score
    elif move1[0:2] == ('paint', None):
        assert move1[2].paint(self.goal.colour)
        assert goal.score(b1) > b1_score
    elif move1[0:2] == ('combine', None):
        assert move1[2].combine()
        assert goal.score(b1) > b1_score
    else:
        assert move1[0:2] == ('pass', None)
        assert goal.score(b1) == b1_score


if __name__ == '__main__':
    import pytest

    pytest.main(['-vv', 'A2_Tests.py'])
