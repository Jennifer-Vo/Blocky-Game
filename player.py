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

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    goals = generate_goals(num_human + num_random + len(smart_players))
    player_id = 0
    goal_number = 0
    difficulty_level = 0
    lst_players = []
    for _ in range(num_human):
        lst_players.append(HumanPlayer(player_id, goals[goal_number]))
        player_id += 1
        goal_number += 1
    for _ in range(num_random):
        lst_players.append(RandomPlayer(player_id, goals[goal_number]))
        player_id += 1
        goal_number += 1
    for _ in range(len(smart_players)):
        lst_players.append(SmartPlayer(player_id, goals[goal_number],
                                       smart_players[difficulty_level]))
        player_id += 1
        goal_number += 1
        difficulty_level += 1
    return lst_players


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    temp = None
    if block.position[0] <= location[0] < block.position[0] + block.size and \
            block.position[1] <= location[1] < block.position[1] + block.size:
        if block.level == level or block.colour is not None:
            return block

        for i in block.children:
            temp = _get_block(i, location, level)
            if temp:
                break

    return temp


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    """Return a tuple of actions that can be performed.
    """
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    """
    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    """ A non-human player in the game of Blocky. The player chooses random
    moves.
    """
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize RandomPlayer with player_id and goal, while setting
        self._proceed to False.
        """
        super().__init__(player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """No block is selected by the player, return None.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        MOUSEBUTTONDOWN, and the user clicking once.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def _create_move_all(self, board: Block) -> List[Tuple[str, Optional[int],
                                                           Block]]:
        """Return a list of all actions that can be performed next.
        """
        move_action = []

        if board.level == board.max_depth:
            move_action.append(_create_move(PAINT, board))

        if len(board.children) == 4:
            move_action.append(_create_move(SWAP_HORIZONTAL, board))
            move_action.append(_create_move(SWAP_VERTICAL, board))
            move_action.append(_create_move(ROTATE_CLOCKWISE, board))
            move_action.append(_create_move(ROTATE_COUNTER_CLOCKWISE, board))

        if board.combine():
            move_action.append(_create_move(COMBINE, board))

        if board.smashable():
            move_action.append(_create_move(SMASH, board))

        for child in board.children:
            child_moves = self._create_move_all(child)
            if child_moves.__len__() > 0:
                move_action += child_moves

        return move_action

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        move_action = self._create_move_all(board.create_copy())
        if len(move_action) == 0:
            return _create_move(PASS, board.create_copy())
        move_action = move_action[random.randint(0, len(move_action)-1)]

        self._proceed = False  # Must set to False before returning!

        return move_action


class SmartPlayer(Player):
    """A non-human player in the game of Blocky. This player chooses moves
    intelligently; it generates a set of random, valid moves and chooses the
    move which yields the best score. The number of moves generated depends on
    the assigned difficulty level.
    """
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    _proceed: bool
    _difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        """Initialize SmartPlayer with player_id and goal, a difficulty level,
        while setting self._proceed to False.
        """
        super().__init__(player_id, goal)
        self._difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """No block is selected by the player, return None.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        MOUSEBUTTONDOWN, and the user clicking once.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def _create_move_all(self, board: Block) -> List[Tuple[str, Optional[int],
                                                           Block]]:
        """Return a list of all actions that can be performed next.
        """
        move_action = list()
        if board.level == board.max_depth:
            move_action.append(_create_move(PAINT, board))

        if len(board.children) == 4:
            move_action.append(_create_move(SWAP_HORIZONTAL, board))
            move_action.append(_create_move(SWAP_VERTICAL, board))
            move_action.append(_create_move(ROTATE_CLOCKWISE, board))
            move_action.append(_create_move(ROTATE_COUNTER_CLOCKWISE, board))

        if board.combine():
            move_action.append(_create_move(COMBINE, board))

        if board.smashable():
            move_action.append(_create_move(SMASH, board))

        for child in board.children:
            child_moves = self._create_move_all(child)
            if child_moves.__len__() > 0:
                move_action += child_moves

        if move_action.__len__() <= self._difficulty:
            return move_action

        return random.sample(move_action, self._difficulty)

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        move_actions = self._create_move_all(board.create_copy())
        board_c = board.create_copy()
        score_min = self.goal.score(board_c)
        index = -1
        for k, move in enumerate(move_actions):
            board_c = board.create_copy()
            temp = (move[0], move[1])
            board_tmp = _get_block(board_c, move[2].position, move[2].level)
            if temp == SMASH:
                board_tmp.smash()
            elif temp == COMBINE:
                board_tmp.combine()
            elif temp == SWAP_HORIZONTAL:
                board_tmp.swap(0)
            elif temp == ROTATE_CLOCKWISE:
                board_tmp.rotate(1)
            elif temp == PAINT:
                board_tmp.paint(self.goal.colour)
            elif temp == ROTATE_COUNTER_CLOCKWISE:
                board_tmp.rotate(3)
            elif temp == SWAP_VERTICAL:
                board_tmp.swap(1)
            score = self.goal.score(board_c)
            if score > score_min:
                index = k
        if index == -1:
            return _create_move(PASS, board.create_copy())

        self._proceed = False  # Must set to False before returning!
        return move_actions[index]


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
