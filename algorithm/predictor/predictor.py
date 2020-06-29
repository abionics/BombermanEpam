from typing import List, Set, Union

from algorithm.me import Me
from algorithm.utils import add_empties_around
from config import PREDICTOR_DEEP
from core.board import Board
from core.element import Element


class Possibility:
    def __init__(self, point: tuple, previous: set):
        self.point = point
        self.previous = previous

    def next_points(self, board: Board) -> set:
        points = {self.point}
        add_empties_around(board, self.point, points)
        return points

    def like(self, point: tuple) -> bool:
        return self.point == point

    def __eq__(self, other):
        if not isinstance(other, Possibility):
            return False
        return self.point == other.point

    def __hash__(self):
        return hash(self.point)

    def __repr__(self):
        x, y = self.point
        return f'({x};{y}:{self.previous})'


class Predictor:
    def __init__(self, board: Board, me: Me):
        self.me = me
        self.board = board
        self.tree: List[List[Possibility]] = []

    def run(self, start_point: tuple, meat_chopper_d: int = 1):
        zero_level = [Possibility(start_point, set())]
        self.tree.append(zero_level)
        self.first(meat_chopper_d)
        for deep in range(1, PREDICTOR_DEEP):
            allow_possibilities = self.get_allow_possibilities(deep)
            self.tree.append(allow_possibilities)

    def first(self, meat_chopper_d: int = 1):
        allow_possibilities = self.get_allow_possibilities(0)
        banned_points = set()
        for point in self.board.find(Element('MEAT_CHOPPER'), Element('DEAD_MEAT_CHOPPER')):
            banned_points.add(point)
            add_empties_around(self.board, point, banned_points, dx=meat_chopper_d, dy=meat_chopper_d)
        if self.me.immune_time <= 1:
            for point in self.board.find(Element('BOMB_BOMBERMAN'),
                                         Element('OTHER_BOMBERMAN'), Element('OTHER_BOMB_BOMBERMAN')):
                banned_points.add(point)
        self.remove_from_possibilities(allow_possibilities, banned_points)
        self.tree.append(allow_possibilities)

    def get_allow_possibilities(self, deep: int) -> List[Possibility]:
        next_possibilities = self.get_next_possibilities(deep)
        banned_points = self.get_banned_points(deep)
        self.remove_from_possibilities(next_possibilities, banned_points)
        return list(next_possibilities)

    def get_next_possibilities(self, deep: int) -> Set[Possibility]:
        current_points = self.get_current_points(deep)
        next_possibilities: Set[Possibility] = set()
        for i, possibility in enumerate(current_points):
            next_points = possibility.next_points(self.board)
            for point in next_points:
                exists = list(filter(lambda p: p.like(point), next_possibilities))
                if exists:
                    exist = exists[0]
                    exist.previous.add(i)
                else:
                    next_possibility = Possibility(point, {i})
                    next_possibilities.add(next_possibility)
        return next_possibilities

    def get_current_points(self, deep: int) -> List[Possibility]:
        return self.tree[deep]

    def get_banned_points(self, deep: int) -> set:
        banned_points = set()
        if self.me.immune_time > deep:
            return set()
        if deep + 1 <= 4:
            bomb_points = self.board.find(Element(f'BOMB_TIMER_{deep + 1}'))
            if self.me.last_act and not self.me.remote_act and (deep + self.me.last_act_time == 5):
                bomb_points.append(self.me.last_act)
            for point in bomb_points:
                banned_points.add(point)
                if self.me.last_act:
                    if point == self.me.last_act:
                        d = self.me.explosion_radius
                        add_empties_around(self.board, point, banned_points, dx=d, dy=d)
                        continue
                add_empties_around(self.board, point, banned_points, dx=3, dy=3)
        if not self.me.remote_act:  # todo fix!
            other_banned = self.board.find(Element('OTHER_BOMB_BOMBERMAN'), Element('BOMB_TIMER_5'))
            if self.me.last_act and self.me.remote_act:
                while self.me.last_act in other_banned:
                    other_banned.pop(self.me.last_act)
            for point in other_banned:
                banned_points.add(point)
                add_empties_around(self.board, point, banned_points, dx=3, dy=3)
        return banned_points

    @staticmethod
    def remove_from_possibilities(source: Union[List[Possibility], Set[Possibility]], remove_points: set):
        for point in remove_points:
            remove_possibilities = list(filter(lambda p: p.like(point), source))
            for remove_possibility in remove_possibilities:
                source.remove(remove_possibility)

    def print(self):
        for i, tree_level in enumerate(self.tree):
            print(f'{i}: {tree_level} - {len(tree_level)}')

    def proposal(self) -> dict:
        last_level = self.tree[PREDICTOR_DEEP]
        proposal = {}
        for possibility in last_level:
            base_possibilities = self._get_base_possibilities({possibility}, PREDICTOR_DEEP)
            for base_possibility in base_possibilities:
                base = base_possibility.point
                if base not in proposal:
                    proposal[base] = []
                proposal[base].append(possibility.point)
        return proposal

    def _get_base_possibilities(self, possibilities: Set[Possibility],
                                deep: int, base_deep: int = 1) -> Set[Possibility]:
        if deep == base_deep:
            return possibilities
        deep -= 1
        indexes = set()
        for possibility in possibilities:
            indexes.update(possibility.previous)
        base_possibilities = set(map(lambda i: self.tree[deep][i], indexes))
        return self._get_base_possibilities(base_possibilities, deep, base_deep)
