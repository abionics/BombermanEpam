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

from act import Act
from algorithm.estimation.estimation import Estimation
from algorithm.me import Me
from algorithm.predictor.predictor import Predictor
from config import PREDICTOR_DEEP, ESTIMATION_ACK_MIN_SCORE, DIRECTION_STOP_K, DIRECTION_INVERTED_K
from core.board import Board
from core.direction import Direction
from core.element import Element
from graphic.graphic import Graphic


class DirectionSolver:
    def __init__(self):
        self.me = Me()
        self.board: Optional[Board] = None
        self.graphic: Optional[Graphic] = None
        self.estimation: Optional[Estimation] = None

        self.next_point: Optional[tuple] = None
        self.direction: Optional[Direction] = None
        self.act: Optional[Act] = None

    def get(self, board_string):
        try:
            print('\n\n')
            self.board = Board(board_string)

            self.graphic = Graphic(self.board)
            self.estimation = Estimation(self.board)

            self.act = Act.none
            self.get_me()

            self.logic()
            self.act_logic()

            self.act = self.me.act_analyzer(self.act, self.next_point, self.board)
            self.direction = self.point_to_direction(self.next_point)
            self.me.move(self.direction, self.board)
            self.die_check()

            self.graphic.global_text = self.me.str()
            self.graphic.save()

            command = self.create_answer()
            print(f'Sending Command {command}')
            return command
        except Exception as e:
            print(e)
            return 'STOP'

    def get_me(self):
        x, y = self.board.find_bomberman()
        self.me.tick(x, y)
        print(self.me.str())
        # p = (me.y + 3) * self.board._size + me.x
        # self.board._string = self.board._string[:p] + '1' + self.board._string[p + 1:]

    def make_np(self, lax, lay):
        npx, npy = self.me.point
        if lax > npx:
            npx -= 1
        elif lax < npx:
            npx += 1
        if lay > npy:
            npy -= 1
        elif lay < npy:
            npy += 1
        return npx, npy

    def logic(self):
        predictor = Predictor(self.board, self.me)
        predictor.run(self.me.point)
        print('\nPREDICTION:')
        predictor.print()

        proposal = predictor.proposal()
        print('\nPROPOSAL:')
        next_point_estimation = {}
        for next_point, points in proposal.items():
            estimation = self.estimation.estimate(points, next_point)
            direction = self.point_to_direction(next_point)
            if direction == Direction('STOP'):
                estimation *= DIRECTION_STOP_K
            if direction == self.me.last_direction.inverted():
                estimation *= DIRECTION_INVERTED_K
            next_point_estimation[next_point] = estimation
            print(f'{direction.to_string()}: {round(estimation, 5)}: {points} - {len(points)}')
        self.next_point = self.me.point
        if len(next_point_estimation) > 0:
            self.next_point = max(next_point_estimation, key=next_point_estimation.get)
        self.draw(predictor, next_point_estimation)

    def act_logic(self):
        before = self.estimation.estimate_act(self.me.point, self.me.explosion_radius)
        after = self.estimation.estimate_act(self.next_point, self.me.explosion_radius)
        if before >= after and before >= ESTIMATION_ACK_MIN_SCORE:
            self.act = Act.before
        elif after >= ESTIMATION_ACK_MIN_SCORE:
            self.act = Act.after
        # act check with predictor
        if self.act != Act.none:
            act_point = self.me.point if self.act == Act.before else self.next_point
            board = self.board.copy()
            board.set_at(act_point, Element('BOMB_TIMER_4'))
            # self.graphic = Graphic(board)
            act_predictor = Predictor(board, self.me)
            act_predictor.run(self.next_point, meat_chopper_d=2)
            if len(act_predictor.tree[PREDICTOR_DEEP]) == 0:
                self.act = Act.none
            if self.act == Act.before:
                proposal = act_predictor.proposal()
                if self.next_point not in proposal.keys():
                    self.act = Act.none
                    # nx, ny = self.next_point
                    # self.graphic.set_color(nx, ny, 'violet')
                    # self.next_point = max(proposal, key=lambda key: len(proposal.get(key)))

    def draw(self, predictor: Predictor, next_point_estimation: dict):
        for deep, tree_level in enumerate(predictor.tree):
            if deep == 0:
                continue
            color = 'red' if deep == PREDICTOR_DEEP else 'orange'
            for possibility in tree_level:
                x, y = possibility.point
                self.graphic.set_color(x, y, color)
        for possibility in predictor.tree[PREDICTOR_DEEP]:
            x, y = possibility.point
            estimation = self.estimation.estimate_one(x, y)
            text = str(round(estimation, 1))
            self.graphic.set_text(x, y, text)
        for (x, y), estimation in next_point_estimation.items():
            self.graphic.set_color(x, y, 'blue')
            self.graphic.set_text(x, y, str(round(estimation, 2)), append=False)

    def die_check(self):
        state = self.board.get_at(self.me.point)
        if state == Element('DEAD_BOMBERMAN'):
            self.me = Me()

    def point_to_direction(self, next_point: tuple) -> Direction:
        nx, ny = next_point
        x, y = self.me.point
        dx = nx - x
        dy = ny - y
        if dx + dy == 0:
            return Direction('STOP')
        elif dy == -1:
            return Direction('UP')
        elif dy == 1:
            return Direction('DOWN')
        elif dx == -1:
            return Direction('LEFT')
        elif dx == 1:
            return Direction('RIGHT')

    def create_answer(self) -> str:
        command = self.direction.to_string()
        if self.act == Act.before:
            command = 'ACT, ' + command
        if self.act == Act.after:
            command = command + ', ACT'
        return command


if __name__ == '__main__':
    raise RuntimeError("This module is not intended to be ran from CLI")

# try:
#     if keyboard.is_pressed('up'):
#         return 'UP'
#     elif keyboard.is_pressed('down'):
#         return 'DOWN'
#     elif keyboard.is_pressed('left'):
#         return 'LEFT'
#     elif keyboard.is_pressed('right'):
#         return 'RIGHT'
#     elif keyboard.is_pressed('space'):
#         return 'ACT'
# except:
#     pass
# print('TIMING')
# return 'NULL'
