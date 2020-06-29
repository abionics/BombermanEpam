bomberman
=========

websocket client app for Codenjoy Bomberman

Designed to be run with python3
Depends on websocket-client from https://github.com/liris/websocket-client/blob/py3/websocket.py

To connect to the game server:
1. Sign up. If you did everything right, you'll get to the main game board.
2. Click on your name on the right hand side panel
3. Copy the whole link from the browser, go to main.py and paste it to the main() method, now you're good to go!

The bomberman actions logic should be implemented in dds.py file. DirectionSolver get() method should return the action
for your bomberman to perform. You can use generic Board API methods in your DirectionSolver. 

**Моя тактика:**
Смотрю все комбинации на 5 ходов вперед и оставляю только те комбинации где я выживаю. Потом для каждой комбинации делаю оценку поля (кол-во очков которые можно заработать минус риски) и выбираю максимальное значение
Дальше смотрю, есть ли смысл ставить бомбу до хода и после хода, если есть смысл - проверяю опять на 5 ходов вперед что есть хотя бы одна комбинация где я выживаю и тогда ставлю бомбу
И параллельно трескаю свои перки которые влияют на это поведение (например скипаю проверку бомб если иммунитет, а RC взрываю если прошло много времени либо рядом чопер/соперник)
Так же есть модуль *graphics* для онлайн графического отображения поля и коэффициентов
