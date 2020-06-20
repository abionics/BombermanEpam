from core.board import Board

FOLDER = 'graphic'
FILENAME = 'field.html'
SPRITES_FOLDER = '../sprites'
DEFAULT_OPACITY = 0.3


class Graphic:
    def __init__(self, board: Board):
        self.board = board
        self.size = self.board._size
        self.field = []
        self.create_board()

    def create_board(self):
        for x in range(self.size):
            row = []
            for y in range(self.size):
                element = self.board.get_at(x, y)
                name = element._name.lower()
                cell = Cell(name)
                row.append(cell)
            self.field.append(row)

    def mark(self, x: int, y: int, color: str, text: str = ""):
        self.field[x][y].mark(color, text)

    def save(self):
        html = ''
        style = ''
        _id = 0
        for y in range(self.size):
            html += '<tr>'
            for x in range(self.size):
                cell = self.field[x][y]
                html += f'<td>{cell.to_html(_id)}</td>'
                style += cell.to_css(_id)
                _id += 1
            html += '</tr>'

        style = open(f'{FOLDER}/style.css').read() + style
        content = open(f'{FOLDER}/template.html').read().format(FILENAME, style, html)
        with open(f'{FOLDER}/{FILENAME}', 'w') as f:
            f.write(content)


class Cell:
    def __init__(self, name: str):
        self.name = name
        self.image = f'{SPRITES_FOLDER}/{name}.png'
        self.styles = {}

    def mark(self, color: str, text: str = ""):
        self.styles['background'] = color
        self.styles['opacity'] = DEFAULT_OPACITY
        self.styles['content'] = f'\"{text}\"'

    def to_html(self, _id):
        return f'<div class="cell c{_id}"><img src="{self.image}" alt={self.name} width="30"></div>\n'

    def to_css(self, _id):
        if len(self.styles) == 0:
            return ''
        css = ';\n'.join(f'{k}: {v};' for k, v in self.styles.items())
        return f'.c{_id}::before {{ {css} }}\n'
