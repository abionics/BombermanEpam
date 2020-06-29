from core.board import Board
from core.element import Element

ALL_EMPTY = [Element('BOMBERMAN'), Element('BOMB_BOMBERMAN'),
             Element('OTHER_BOMBERMAN'), Element('OTHER_DEAD_BOMBERMAN'), Element('OTHER_BOMB_BOMBERMAN'),
             Element('DESTROYED_WALL'), Element('MEAT_CHOPPER'), Element('DEAD_MEAT_CHOPPER'),
             Element('BOMB_BLAST_RADIUS_INCREASE'), Element('BOMB_COUNT_INCREASE'),
             Element('BOMB_IMMUNE'), Element('BOMB_REMOTE_CONTROL'),
             Element('BOOM'), Element('NONE')]


def add_empties_around(board: Board, point: tuple, points: set, *, dx=1, dy=1):
    x, y = point
    forward = backward = True
    for xi in range(1, dx + 1):
        if forward:
            forward = _add_if_empty(board, x + xi, y, points)
        if backward:
            backward = _add_if_empty(board, x - xi, y, points)
    forward = backward = True
    for yi in range(1, dy + 1):
        if forward:
            forward = _add_if_empty(board, x, y + yi, points)
        if backward:
            backward = _add_if_empty(board, x, y - yi, points)


def _add_if_empty(board: Board, x: int, y: int, points: set) -> bool:
    if is_empty(board, x, y):
        points.add((x, y))
        return True
    return False


def is_empty(board: Board, x: int, y: int) -> bool:
    return board.get_at((x, y)) in ALL_EMPTY
