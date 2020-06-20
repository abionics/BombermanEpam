from typing import List

from core.board import Board
from core.element import Element

ALL_EMPTY = [Element('BOMBERMAN'), Element('BOMB_BOMBERMAN'),
             Element('OTHER_BOMBERMAN'), Element('OTHER_DEAD_BOMBERMAN'), Element('OTHER_BOMB_BOMBERMAN'),
             Element('DESTROYED_WALL'), Element('MEAT_CHOPPER'), Element('DEAD_MEAT_CHOPPER'),
             Element('BOMB_BLAST_RADIUS_INCREASE'), Element('BOMB_COUNT_INCREASE'),
             Element('BOMB_IMMUNE'), Element('BOMB_REMOTE_CONTROL'),
             Element('BOOM'), Element('NONE')]


class Heatmap:
    def __init__(self, board: Board):
        self.board = board
        self.heatmap = []

    def run(self):
        me = self.board.get_bomberman()
        self.heatmap = [(0, (me.x, me.y))]
        self.first()
        for deep in range(1, 5):
            allow_points = self.get_allow_points(deep)
            for x, y in allow_points:
                self.heatmap.append((deep + 1, (x, y)))

    def first(self):
        allow_points = self.get_allow_points(0)
        banned_points = set()
        for point in self.board.get_meat_choppers():
            x, y = point.x, point.y
            banned_points.add((x, y))
            self._add_empties_around(x, y, banned_points)
        allow_points.difference_update(banned_points)
        for x, y in allow_points:
            self.heatmap.append((1, (x, y)))

    def get_allow_points(self, deep: int) -> set:
        next_points = self.get_next_points(deep)
        banned_points = self.get_banned_points(deep)
        return next_points.difference(banned_points)

    def get_next_points(self, deep: int) -> set:
        current_points = self.get_current_points(deep)
        next_points = set()
        for x, y in current_points:
            self._add_empties_around(x, y, next_points)
        for deep, point in self.heatmap:
            next_points.discard(point)
        return next_points

    def get_current_points(self, deep: int) -> list:
        return list(map(
            lambda val: val[1],
            filter(
                lambda val: val[0] == deep,
                self.heatmap
            )
        ))

    def get_banned_points(self, deep: int) -> set:
        banned_points = set()
        if deep + 1 <= 4:
            for point in self.board.find_all(Element(f'BOMB_TIMER_{deep + 1}')):
                x, y = point.x, point.y
                banned_points.add((x, y))
                self._add_empties_around(x, y, banned_points, dx=3, dy=3)
        for point in self.board.find_all(Element('OTHER_BOMB_BOMBERMAN'), Element('BOMB_TIMER_5')):
            x, y = point.x, point.y
            banned_points.add((x, y))
            self._add_empties_around(x, y, banned_points, dx=3, dy=3)
        for point in self.board.find_all(Element('BOOM')):
            x, y = point.x, point.y
            banned_points.add((x, y))
        return banned_points

    def _add_empties_around(self, x, y, points: set, *, dx=1, dy=1):
        add = lambda _x, _y: points.add((_x, _y)) \
            if self._is_empty(_x, _y) else None
        for xi in range(1, dx + 1):
            add(x + xi, y)
            add(x - xi, y)
        for yi in range(1, dy + 1):
            add(x, y + dy)
            add(x, y - dy)

    def _is_empty(self, x, y) -> bool:
        if not self.board.is_into(x, y):
            return False
        return self.board.get_at(x, y) in ALL_EMPTY

    @staticmethod
    def _all_bombs() -> List[Element]:
        elements = []
        for i in range(5):
            elements.append(Element(f'BOMB_TIMER_{i + 1}'))
        return elements
