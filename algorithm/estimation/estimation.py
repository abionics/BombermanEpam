from config import ESTIMATION_AROUND_K
from core.board import Board
from core.element import Element


class Estimation:
    def __init__(self, board: Board):
        self.board = board

    def estimate(self, points: list, me) -> float:
        x_me, y_me = me
        estimate = 0
        for x, y in points:
            estimate_one = self.estimate_one(x, y)
            dist = abs(x - x_me) + abs(y - y_me)
            k = (1 - 0.1 * dist)
            if dist == 0:
                k = 1.5
            estimate += estimate_one * k
        # count = len(points)
        # return (20 * estimate + count ** 2.2) / (20 * len(points))
        # return estimate ** 1.25 / count
        return estimate

    def estimate_one(self, x: int, y: int, *, dx=1, dy=1) -> float:
        current = self._estimate_cell(x, y)
        around = 0
        for xi in range(1, dx + 1):
            around += self._estimate_cell(x + xi, y) + self._estimate_cell(x - xi, y)
        for yi in range(1, dy + 1):
            around += self._estimate_cell(x, y + yi) + self._estimate_cell(x, y - yi)
        around *= ESTIMATION_AROUND_K
        return current + around

    def _estimate_cell(self, x: int, y: int) -> float:
        element = self.board.get_at((x, y))
        # todo estimate players (static bots ++)
        return COSTS.get(element.name, 0)

    def estimate_act(self, point: tuple, radius: int) -> float:
        x, y = point
        estimate = 0
        forward = backward = True
        for xi in range(1, radius + 1):
            if forward:
                forward = self.board.get_at((x + xi, y)) != Element('WALL')
                estimate += self._estimate_act(x + xi, y)
            if backward:
                backward = self.board.get_at((x + xi, y)) != Element('WALL')
                estimate += self._estimate_act(x - xi, y)
        for yi in range(1, 4):
            if forward:
                forward = self.board.get_at((x, y + yi)) != Element('WALL')
                estimate += self._estimate_act(x, y + yi)
            if backward:
                backward = self.board.get_at((x, y - yi)) != Element('WALL')
                estimate += self._estimate_act(x, y - yi)
        return estimate

    def _estimate_act(self, x: int, y: int) -> float:
        element = self.board.get_at((x, y))
        return ACT_COSTS.get(element.name, 0)


COSTS = {
    # The Bomberman
    'BOMBERMAN': -0.01,
    'BOMB_BOMBERMAN': -1,
    'DEAD_BOMBERMAN': 0,
    # The Enemies
    'OTHER_BOMBERMAN': 0.75,
    'OTHER_BOMB_BOMBERMAN': -1,
    'OTHER_DEAD_BOMBERMAN': 0.1,
    # The Bombs
    'BOMB_TIMER_5': -1,
    'BOMB_TIMER_4': -1,
    'BOMB_TIMER_3': -1,
    'BOMB_TIMER_2': -1,
    'BOMB_TIMER_1': -1,
    'BOOM': 0.05,
    # Walls
    'WALL': -0.1,
    'DESTROY_WALL': 0.25,
    'DESTROYED_WALL': 0.2,
    # Meatchoopers
    'MEAT_CHOPPER': 0.9,
    'DEAD_MEAT_CHOPPER': 0.9,
    # Perks
    'BOMB_BLAST_RADIUS_INCREASE': 1.2,
    'BOMB_COUNT_INCREASE': 1.2,
    'BOMB_IMMUNE': 1.25,
    'BOMB_REMOTE_CONTROL': 1.25,
    # Space
    'NONE': 0.1,
}

ACT_COSTS = {
    # The Enemies
    'OTHER_BOMBERMAN': 1,
    'OTHER_BOMB_BOMBERMAN': 1,
    'OTHER_DEAD_BOMBERMAN': 0.2,
    # The Bombs
    'BOMB_TIMER_5': 0.2,
    'BOMB_TIMER_4': 0.2,
    'BOMB_TIMER_3': 0.2,
    'BOMB_TIMER_2': 0.2,
    'BOMB_TIMER_1': 0.2,
    'BOOM': 0.01,
    # Walls
    'DESTROY_WALL': 1,
    'DESTROYED_WALL': 0.2,
    # Meatchoopers
    'MEAT_CHOPPER': 1,
    'DEAD_MEAT_CHOPPER': 0.9,
    # Perks
    'BOMB_BLAST_RADIUS_INCREASE': 0.5,
    'BOMB_COUNT_INCREASE': 0.5,
    'BOMB_IMMUNE': 0.5,
    'BOMB_REMOTE_CONTROL': 0.5,
}
