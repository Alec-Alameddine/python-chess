from time import sleep

class Config:
    letters = tuple('abcdefghijklmnopqrstuvwxyz')

    @classmethod
    def new_board(cls, btype):
        def size(x):
            return [['___' for _ in range(x)] for _ in range(x)]

        if 'custom' in btype.lower():
            btype = int(btype.replace('custom', '').strip())
            cls.board = size(btype)
        elif btype.lower() == 'default':
            cls.board = size(8)
        elif btype.lower() == 'extended':
            cls.board = size(10)
        elif btype.lower() == 'small':
            cls.board = size(5)
        elif btype.lower() == 'max':
            cls.board = size(26)
        elif btype.lower() == 'min':
            cls.board = size(1)

    @classmethod
    def print_board(cls):
        def printl():
            if len(str(len(cls.board))) == 2:
                print(' ', end='')
            for x in range(len(cls.board)):
                print(' '*6 + f'{cls.letters[x]}', end='')
            print('\n')

        print('\n'*2)
        printl()
        for x in range(len(cls.board)):
            print(f'{len(cls.board)-x:0{len(str(len(cls.board)))}}  {cls.board[x]}  {len(cls.board)-x:0{len(str(len(cls.board)))}}\n')
        printl()
        print('\n'*4)

    @classmethod
    def tile_convert(cls, x, disp=False):
        if not disp:
            if isinstance(x, str):
                return cls.letters.index(x)
            else:
                return cls.letters[x]
        else:
            return len(cls.board) - int(x)

class ChessPiece:
    def __init__(self, pos, color, num, piece):
        self.x = int(Config.tile_convert(pos[0]))
        self.y = len(Config.board) - int(pos[1])
        self.color = color
        self.piece = piece
        self.pieceid = num
        self.set_id()
        self.create()
        Config.print_board()

    def __str__(self):
        return self.piece

    def set_id(self):
        if self.__class__.__name__ != "Knight":
            self.pieceid = f'{piece[0]}{self.pieceid}'
        else:
            self.pieceid = f'N{self.pieceid}'

        if self.color is not None:
            if self.color.lower() in ('black', 'white', 'b', 'w'):
                self.pieceid = self.color.lower()[0] + self.pieceid
                if self.color.lower() == 'b':
                    self.color = 'black'
                elif self.color.lower() == 'w':
                    self.color = 'white'
            else:
                self.color = None
                print("Invalid color input. Color not set.")
                self.set_id()
        else:
             self.pieceid = '_' + self.pieceid


    def create(self):
        Config.board[self.y][self.x] = self.pieceid

    def teleport(self, pos):
        Config.board[self.y][self.x] = '___'

        self.x = Config.tile_convert(pos[0])
        self.y = Config.tile_convert(pos[1], True)

        Config.board[self.y][self.x] = self.pieceid

        Config.print_board()

    def move(self, pos):
        if pos in self.possible_moves():
            self.teleport(pos)
        else:
            print(f'Unable to move to {pos}')


    def get_info(self):
        print(f'{self.__class__.__name__}:\n')
        print('ID: ', self.pieceid)
        print('Position: ', Config.tile_convert(self.x), Config.tile_convert(self.y, True), sep='')
        print('Color: ', self.color)

    def erase(self):  # Doesn't delete the piece. It can be brought back by moving it to a square
        Config.board[self.y][self.x] = '___'


class Knight(ChessPiece):
    def __init__(self, pos, color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)


    def possible_moves(self):
        pos_moves = []
        for xoff, yoff in ( (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1) ):
            newx = self.x + xoff
            newy = self.y + yoff
            if 0 <= newx < len(Config.board) and 0 <= newy < len(Config.board) and Config.board[newx][newy] == '___':
                pos_moves.append(f'{Config.tile_convert(newx)}{Config.tile_convert(newy, True)}')

        return pos_moves

    def demo(self):  # default board
        for pos in ('e1', 'f3', 'g5', 'h7', 'f8', 'e6', 'c5', 'd3', 'e1'):
            self.teleport(pos)
            sleep(1)

class Rook(ChessPiece):
    def __init__(self, pos, color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)

Config.new_board('default')

# knight1 = Knight('c1', color='w', num=1)

Config.print_board()

# knight1.demo()

# knight1.get_info()

# knight1.demo()
