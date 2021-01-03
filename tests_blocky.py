import pytest
from block import Block



def test_swap_horizontal():
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
    assert board.children[1].colour == None
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


def test_swap_vertical():
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
    assert board.children[3].colour == None
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


def test_rotate_1():
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
    assert board.children[3].colour == None
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


if __name__ == '__main__':
    pytest.main(['tests_blocky.py'])
