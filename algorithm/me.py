from act import Act
from algorithm.utils import add_empties_around
from config import DEFAULT_EXPLOSION_RADIUS, PERK_TIME, RADIUS_PERK_INCREASE, REMOTE_PERK_COUNT
from core.board import Board
from core.direction import Direction
from core.element import Element


class Me:
    def __init__(self):
        self.ticks = 0
        self.x = 0
        self.y = 0
        self.radius_value = 0
        self.radius_time = 0
        self.count_time = 0
        self.immune_time = 0
        self.remote_value = 0
        self.remote_act = False
        self.last_direction = Direction('NULL')
        self.last_act = None
        self.last_act_time = 100

    def tick(self, x, y):
        self.ticks += 1
        self.x = x
        self.y = y
        self.last_act_time += 1
        if self.last_act_time >= 5 and self.remote_act is False:
            self.last_act = None
        self.perk_tick()

    def perk_tick(self):
        if self.radius_time > 0:
            self.radius_time -= 1
            if self.radius_time == 0:
                self.radius_value = 0
        if self.count_time > 0:
            self.count_time -= 1
        if self.immune_time > 0:
            self.immune_time -= 1

    def move(self, direction: Direction, board: Board):
        self.last_direction = direction
        _, dx, dy = direction._dir
        nx = self.x + dx
        ny = self.y + dy
        next_element = board.get_at((nx, ny))
        self.set_perk(next_element)

    def set_perk(self, element: Element):
        if element == Element('BOMB_BLAST_RADIUS_INCREASE'):
            self.radius_value += RADIUS_PERK_INCREASE
            self.radius_time += PERK_TIME
        if element == Element('BOMB_COUNT_INCREASE'):
            self.count_time = PERK_TIME
        if element == Element('BOMB_IMMUNE'):
            self.immune_time = PERK_TIME
        if element == Element('BOMB_REMOTE_CONTROL'):
            self.remote_value = REMOTE_PERK_COUNT

    def act_analyzer(self, act: Act, next_point: tuple, board: Board) -> Act:
        if self.remote_act:
            d = self.explosion_radius
            points = {self.last_act}
            add_empties_around(board, self.last_act, points, dx=d, dy=d)
            if self.immune_time <= 1 and self.point in points:
                return Act.none
            for point in points:
                if board.get_at(point) in [Element('OTHER_BOMBERMAN'), Element('MEAT_CHOPPER'),
                                          Element('OTHER_BOMB_BOMBERMAN')]:
                    self.act_of_remove_act()
                    return Act.before
            if self.last_act_time > 5:
                self.act_of_remove_act()
                return Act.before
            return Act.none
        if act != Act.none:
            # can place bomb
            if self.count_time == 0:
                if self.last_act is not None:
                    return Act.none
            # remote
            if self.remote_value > 0:
                self.remote_value -= 1
                self.remote_act = True
            # setup last_act
            if act == Act.before:
                self.last_act = self.point
            if act == Act.after:
                self.last_act = next_point
            self.last_act_time = 0
            return act
        else:
            return Act.none

    def act_of_remove_act(self):
        self.remote_act = False
        self.last_act = None

    @property
    def point(self) -> tuple:
        return self.x, self.y

    @property
    def explosion_radius(self):
        return DEFAULT_EXPLOSION_RADIUS + self.radius_value

    def str(self) -> str:
        return f'radius: {self.radius_time}s, {self.radius_value}\n' \
               f'count: {self.count_time}s\n' \
               f'immune: {self.immune_time}\n' \
               f'remote: {self.remote_value} | {self.remote_act}\n' \
               f'-- last bomb: {self.last_act} {self.last_act_time}s {self.remote_act}'
