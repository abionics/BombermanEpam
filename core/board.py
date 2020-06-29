#! /usr/bin/env python3

###
# #%L
# Codenjoy - it's a dojo-like platform from developers to developers.
# %%
# Copyright (C) 2018 Codenjoy
# %%
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/gpl-3.0.html>.
# #L%
###

from math import sqrt
from typing import Dict, List

from core.element import Element, ELEMENTS

DEFAULT_ELEMENT = Element('WALL')


class Board:
    def __init__(self, board_string: str):
        board_string = board_string.replace('\n', '')
        self.size = int(sqrt(len(board_string)))
        self.field: List[List[Element]] = self.create_2d_array(self.size, self.size, DEFAULT_ELEMENT)
        self.grouped: Dict[Element, list] = {}
        self.init(board_string)

    def init(self, board_string: str):
        for element in ELEMENTS:
            self.grouped[element] = []
        x = y = 0
        for char in board_string:
            element = Element(char)
            self.field[x][y] = element
            self.grouped[element].append((x, y))
            x += 1
            if x == self.size:
                x = 0
                y += 1

    def get_at(self, point: tuple, default: Element = DEFAULT_ELEMENT) -> Element:
        if not self.is_into(point):
            return default
        x, y = point
        return self.field[x][y]

    def set_at(self, point: tuple, value: Element):
        if not self.is_into(point):
            return
        x, y = point
        old_value = self.field[x][y]
        self.grouped[old_value].remove((x, y))
        self.field[x][y] = value
        self.grouped[value].append((x, y))

    def is_into(self, point: tuple) -> bool:
        x, y = point
        return 0 <= x < self.size and 0 <= y < self.size

    def find(self, *elements) -> list:
        points = set()
        for element in elements:
            p = self.grouped[element]
            points.update(p)
        return list(points)

    def find_bomberman(self) -> tuple:
        points = self.find(Element('BOMBERMAN'), Element('BOMB_BOMBERMAN'), Element('DEAD_BOMBERMAN'))
        return points[0]

    def copy(self) -> 'Board':
        return Board(self.to_board_string())

    def to_board_string(self) -> str:
        board_string = ''
        for x in range(self.size):
            for y in range(self.size):
                board_string += self.field[y][x].char
        return board_string

    @staticmethod
    def create_2d_array(width: int, height: int, value):
        return [[value for _ in range(width)] for _ in range(height)]

# class Board:
#     BLAST_RANGE = 3
#
#     """ Class describes the Board field for Bomberman game."""
#
#     def __init__(self, board_string):
#         self._string = board_string.replace('\n', '')
#         self._len = len(self._string)  # the length of the string
#         self._size = int(sqrt(self._len))  # size of the board
#         # print("Board size is sqrt", self._len, self._size)
#
#     def find_all(self, *elements) -> list:
#         """ Returns the list of points for the given element type."""
#         _points = set()
#         for element in elements:
#             _a_char = element.get_char()
#             for i, c in enumerate(self._string):
#                 if c == _a_char:
#                     _points.add(self._strpos2pt(i))
#         return list(_points)
#
#     def get_at(self, x, y):
#         """ Return an Element object at coordinates x,y."""
#         return Element(self._string[self._xy2strpos(x, y)])
#
#     def set_at(self, x, y, element: Element):
#         p = y * self._size + x
#         self._string = self._string[:p] + element._char + self._string[p + 1:]
#
#     def is_at(self, x, y, element_object):
#         """ Return True if Element is at x,y coordinates."""
#         return element_object == self.get_at(x, y)
#
#     def is_barrier_at(self, x, y):
#         """ Return true if barrier is at x,y."""
#         return Point(x, y) in self.get_barriers()
#
#     def is_my_bomberman_dead(self):
#         """ Returns False if your bomberman still alive."""
#         return Element('DEAD_BOMBERMAN').get_char() in self._string
#
#     def get_bomberman(self):
#         """ Return the point where your bombermain is."""
#         points = set()
#         points.update(self.find_all(Element('BOMBERMAN')))
#         points.update(self.find_all(Element('BOMB_BOMBERMAN')))
#         points.update(self.find_all(Element('DEAD_BOMBERMAN')))
#         assert len(points) <= 1, "There should be only one bomberman"
#         return list(points)[0]
#
#     def get_other_bombermans(self):
#         """ Return the list of points for other bombermans."""
#         points = set()
#         points.update(self.find_all(Element('OTHER_BOMBERMAN')))
#         points.update(self.find_all(Element('OTHER_BOMB_BOMBERMAN')))
#         points.update(self.find_all(Element('OTHER_DEAD_BOMBERMAN')))
#         return list(points)
#
#     def get_meat_choppers(self):
#         return self.find_all(Element('MEAT_CHOPPER'))
#
#     def get_barriers(self):
#         """ Return the list of barriers Points."""
#         points = set()
#         points.update(self.get_walls())
#         points.update(self.get_bombs())
#         points.update(self.get_destroy_walls())
#         points.update(self.get_meat_choppers())
#         points.update(self.get_other_bombermans())
#         return list(points)
#
#     def get_walls(self):
#         """ Retuns the list of walls Element Points."""
#         return self.find_all(Element('WALL'))
#
#     def get_destroy_walls(self):
#         """ """
#         return self.find_all(Element('DESTROY_WALL'))
#
#     def get_bombs(self):
#         """ Returns the list of bombs points."""
#         points = set()
#         points.update(self.find_all(Element('BOMB_TIMER_1')))
#         points.update(self.find_all(Element('BOMB_TIMER_2')))
#         points.update(self.find_all(Element('BOMB_TIMER_3')))
#         points.update(self.find_all(Element('BOMB_TIMER_4')))
#         points.update(self.find_all(Element('BOMB_TIMER_5')))
#         points.update(self.find_all(Element('BOMB_BOMBERMAN')))
#         return list(points)
#
#     def get_blasts(self):
#         return self.find_all(Element('BOOM'))
#
#     def get_future_blasts(self):
#         _bombs = set()
#         _bombs.update(self.get_bombs())
#         _bombs.update(self.find_all(Element('OTHER_BOMB_BOMBERMAN')))
#         _points = set()
#         for _bomb in _bombs:
#             _bx, _by = _bomb.get_x(), _bomb.get_y()
#             _points.add(_bomb)
#             _points.update(self._search_blasts(_bomb))
#         return list(_points)
#
#     def get_perks(self):
#         """ Returns the list of points with Perks."""
#         points = set()
#         points.update(self.find_all(Element('BOMB_BLAST_RADIUS_INCREASE')))
#         points.update(self.find_all(Element('BOMB_COUNT_INCREASE')))
#         points.update(self.find_all(Element('BOMB_IMMUNE')))
#         points.update(self.find_all(Element('BOMB_REMOTE_CONTROL')))
#         return list(points)
#
#     def is_near(self, x, y, elem):
#         _is_near = False
#         if not Point(x, y).is_bad(self._size):
#             _is_near = (self.is_at(x + 1, y, elem) or
#                         self.is_at(x - 1, y, elem) or
#                         self.is_at(x, 1 + y, elem) or
#                         self.is_at(x, 1 - y, elem))
#         return _is_near
#
#     def count_near(self, x, y, elem):
#         """ Counts the number of occurrences of elem nearby """
#         _near_count = 0
#         if not Point(x, y).is_bad(self._size):
#             for _x, _y in ((x + 1, y), (x - 1, y), (x, 1 + y), (x, 1 - y)):
#                 if self.is_at(_x, _y, elem):
#                     _near_count += 1
#         return _near_count
#
#     def to_string(self):
#         return ("Board:\n{brd}\nBomberman at: {mbm}\nOther Bombermans "
#                 "at: {obm}\nMeat Choppers at: {mcp}\nDestroy Walls at:"
#                 " {dwl}\nBombs at: {bmb}\nBlasts at: {bls}\nExpected "
#                 "Blasts at: {ebl}".format(brd=self._line_by_line(),
#                                           mbm=self.get_bomberman(),
#                                           obm=self.get_other_bombermans(),
#                                           mcp=self.get_meat_choppers(),
#                                           dwl=self.get_destroy_walls(),
#                                           bmb=self.get_bombs(),
#                                           bls=self.get_blasts(),
#                                           ebl=self.get_future_blasts())
#                 )
#
#     def _line_by_line(self):
#         return '\n'.join([self._string[i:i + self._size]
#                           for i in range(0, self._len, self._size)])
#
#     def _strpos2pt(self, strpos):
#         return Point(*self._strpos2xy(strpos))
#
#     def _strpos2xy(self, strpos):
#         return (strpos % self._size, strpos // self._size)
#
#     def _xy2strpos(self, x, y):
#         return self._size * y + x
#
#     def _search_blasts(self, bomb_point):
#         points = set()
#         walls = self.get_walls()
#
#         for search_range, is_x in ((range(bomb_point.get_x(), bomb_point.get_x() + self.BLAST_RANGE), True),
#                                    (range(bomb_point.get_x(), bomb_point.get_x() - self.BLAST_RANGE), True),
#                                    (range(bomb_point.get_y(), bomb_point.get_y() + self.BLAST_RANGE), False),
#                                    (range(bomb_point.get_y(), bomb_point.get_y() - self.BLAST_RANGE), False)):
#             for i in search_range:
#                 current_point = Point(i, bomb_point.get_y()) if is_x else Point(bomb_point.get_x(), i)
#                 if (current_point.is_bad(self._size) or
#                         current_point in walls):
#                     break
#                 else:
#                     points.add(current_point)
#
#         return points
#
#     def is_into(self, x, y):
#         return 0 <= x < self._size and 0 <= y < self._size
#
#
# if __name__ == '__main__':
#     raise RuntimeError("This module is not designed to be ran from CLI")
