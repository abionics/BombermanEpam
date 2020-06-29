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


from sys import version_info
from urllib.parse import urlparse, parse_qs

from solver import DirectionSolver
from core.web.webclient import WebClient


def get_url_for_ws(url):
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)

    return "{}://{}/codenjoy-contest/ws?user={}&code={}".format('ws' if parsed_url.scheme == 'http' else 'wss',
                                                                parsed_url.netloc,
                                                                parsed_url.path.split('/')[-1],
                                                                query['code'][0])


def main():
    assert version_info[0] == 3, "You should run me with Python 3.x"

    # substitute following link with the one you've copied in your browser after registration
    # url = "https://botchallenge.cloud.epam.com/codenjoy-contest/board/player/4yvrb5xa2u78prdqjq6s?code=1896417313009904871"
    # url = 'http://144.91.91.85:8080/codenjoy-contest/board/player/user_id?code=12345678901234567890'
    # url = "http://bomberman.coders.in.ua:8081/codenjoy-contest/board/player/anyidofbot?code=12345678901234567890"
    # url = 'http://127.0.0.1:8080/codenjoy-contest/board/player/user_id?code=12345678901234567890'
    url = 'https://botchallenge.cloud.epam.com/codenjoy-contest/board/player/4yvrb5xa2u78prdqjq6s?code=1896417313009904871'
    direction_solver = DirectionSolver()

    wcl = WebClient(url=get_url_for_ws(url), solver=direction_solver)
    wcl.run_forever()


if __name__ == '__main__':
    main()
