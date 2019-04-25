from time import sleep

class Config:
    types = {'min': 1, 'miniature': 3, 'small': 5, 'default': 8, 'extended': 11, 'large': 15, 'massive': 20, 'max': 26}
    letters = tuple('abcdefghijklmnopqrstuvwxyz')
    board = 'UNINITIALIZED'
    b_len = 'UNINITIALIZED'

    @classmethod
    def new_board(cls, btype):
        def size(x):
            return [['___' for _ in range(x)] for _ in range(x)], x

        if btype is not None:
            btype = btype.lower()

            if 'custom' in btype and 1:
                btype = int(btype.replace('custom', '').strip())
                if 1 <= btype <= 26:
                    cls.board, cls.b_len = size(btype)
                else:
                    btype = None
                    cls.new_board(btype)
            elif btype in cls.types:
                cls.board, cls.b_len = size(cls.types[btype])
            else:
                print(f'Unable to initialize board of unknown type {btype}')

        else:
            print('Unable to initalize board with a size lower than 1 or greater than 26')

    @classmethod
    def print_board(cls):
        if Config.b_len != 'UNINITIALIZED':
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
        else:
            print('Unable to print board of uninitialized type')

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
        self.y = Config.b_len - int(pos[1])
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
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)


    def possible_moves(self):
        pos_moves = []
        for xoff, yoff in ( (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1) ):
            newx = self.x + xoff
            newy = self.y + yoff
            if 0 <= newx < Config.b_len and 0 <= newy < Config.b_len and Config.board[newx][newy] == '___':
                pos_moves.append(f'{Config.tile_convert(newx)}{Config.tile_convert(newy, True)}')

        return pos_moves

    def demo(self):  # default board
        for pos in ('e1', 'f3', 'g5', 'h7', 'f8', 'e6', 'c5', 'd3', 'e1'):
            self.teleport(pos)
            sleep(1)

class Rook(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        for x in range(Config.b_len): pass

Config.new_board('default')

# knight1 = Knight('c1', color='w', num=1)

Config.print_board()

# knight1.demo()

# knight1.get_info()

# knight1.demo()
