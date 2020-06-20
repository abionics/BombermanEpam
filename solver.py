#!/usr/bin/env python3

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
from typing import Optional

import keyboard

from algorithm.heatmap.heatmap import Heatmap
from core.board import Board
from core.direction import Direction
from graphic.graphic import Graphic


class DirectionSolver:
    def __init__(self):
        self.board: Optional[Board] = None
        self.graphic: Optional[Graphic] = None
        self.last = Direction('UP')
        self.tick = 0

    def get(self, board_string):
        self.board = Board(board_string)
        self.graphic = Graphic(self.board)

        direction = self.logic()
        self.last = direction
        self.tick += 1

        self.graphic.save()
        command = direction.to_string()
        print(f'Sending Command {command}')
        return command

    def logic(self) -> Direction:
        heatmap = Heatmap(self.board)
        heatmap.run()
        print(heatmap.heatmap)
        for deep, (x, y) in heatmap.heatmap:
            if deep != 0:
                self.graphic.mark(x, y, 'orange', text=deep)
        try:
            if keyboard.is_pressed('up'):
                return Direction('UP')
            elif keyboard.is_pressed('down'):
                return Direction('DOWN')
            elif keyboard.is_pressed('left'):
                return Direction('LEFT')
            elif keyboard.is_pressed('right'):
                return Direction('RIGHT')
            elif keyboard.is_pressed('space'):
                return Direction('ACT')
        except:
            pass
        print('TIMING')
        return Direction('NULL')


if __name__ == '__main__':
    raise RuntimeError("This module is not intended to be ran from CLI")
