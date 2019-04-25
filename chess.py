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
                if len(str(cls.b_len)) == 2:
                    print(' ', end='')
                for x in range(cls.b_len):
                    print(' '*6 + f'{cls.letters[x]}', end='')
                print('\n')

            print('\n'*2)
            printl()
            for x in range(cls.b_len):
                print(f'{cls.b_len-x:0{len(str(cls.b_len))}}  {cls.board[x]}  {cls.b_len-x:0{len(str(cls.b_len))}}\n')
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
        else:  # disp converts the letter in {letter}{number} to a number
            return cls.b_len - int(x)

    @classmethod
    def l_num_to_coord(cls, pos):
        return Config.b_len - int(pos[1]), int(Config.tile_convert(pos[0]))

    @classmethod
    def c_convert(cls, color):
        if color == 'White':
            return 'b'
        if color == "Black":
            return 'w'

class ChessPiece:
    def __init__(self, pos, color, num, piece):
        self.x = int(Config.tile_convert(pos[0]))
        self.y = Config.b_len - int(pos[1])
        self.color = color
        self.piece = piece
        self.pieceid = num
        self.moves = 0
        self.captured = []
        self.set_id()
        self.create()
        Config.print_board()

    def __str__(self):
        return self.piece

    def __repr__(self):
        return self.pieceid

    def set_id(self):
        if self.__class__.__name__ != "Knight":
            self.pieceid = f'{self.piece[0]}{self.pieceid}'
        else:
            self.pieceid = f'N{self.pieceid}'

        if self.color is not None:
            if self.color.lower() in ('black', 'white', 'b', 'w'):
                self.pieceid = self.color.lower()[0] + self.pieceid
                if self.color.lower() == 'b':
                    self.color = 'Black'
                elif self.color.lower() == 'w':
                    self.color = 'White'
            else:
                self.color = None
                print("Invalid color input. Color not set.")
                self.set_id()
        else:
             self.pieceid = '_' + self.pieceid


    def create(self):
        if Config.board[self.y][self.x] != '___':
            po = Config.board[self.y][self.x]
            print(f'Piece {po} erased to make room for {self.pieceid}')

        Config.board[self.y][self.x] = self.pieceid

    def teleport(self, pos, record=False):
        Config.board[self.y][self.x] = '___'

        if record:
            self.moves += 1
            coord = Config.l_num_to_coord(pos)
            if Config.board[coord[0]][coord[1]] != '___':
                self.captured.append(Config.board[coord[0]][coord[1]])
                print(f'{self.pieceid} has captured {Config.board[coord[0]][coord[1]]}!')

        self.x = Config.tile_convert(pos[0])
        self.y = Config.tile_convert(pos[1], True)

        Config.board[self.y][self.x] = self.pieceid

        Config.print_board()

    def move(self, pos):
        if pos in self.possible_moves():
            coord = Config.l_num_to_coord(pos)
            if Config.board[coord[0]][coord[1]] != '___':
                self.captured.append(Config.board[coord[0]][coord[1]])
                print(f'{self.pieceid} has captured {Config.board[coord[0]][coord[1]]}!')

            self.teleport(pos)
            self.moves += 1
        else:
            print(f'Unable to move to {pos}')


    def get_info(self):
        print(f'{self.__class__.__name__}:\n')
        print('ID: ', self.pieceid)
        print('Position: ', Config.tile_convert(self.x), Config.tile_convert(self.y, True), sep='')
        print('Color: ', self.color)

    def erase(self):  # Doesn't delete the piece. It can be brought back by moving it to a square
        Config.board[self.y][self.x] = '___'


class Pawn(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        # Forward
        if not self.moves: # Starting Position
            if self.color != 'White':
                for new_y in (y+1, y+2):
                    try:
                        if Config.board[new_y][x] == '___':
                            pos_moves.append(f'{Config.tile_convert(x)}{Config.tile_convert(new_y, True)}')
                        else: break
                    except IndexError: pass

            if self.color != 'Black':
                for new_y in (y-1, y-2):
                    try:
                        if Config.board[new_y][x] == '___':
                            pos_moves.append(f'{Config.tile_convert(x)}{Config.tile_convert(new_y, True)}')
                        else: break
                    except IndexError: pass

        else:  # Post-Start
            if self.color != 'White':
                try:
                    if Config.board[y+1][x] == '___':
                        pos_moves.append(f'{Config.tile_convert(x)}{Config.tile_convert(y+1, True)}')
                except IndexError: pass

            if self.color != 'Black':
                try:
                    if Config.board[y-1][x] == '___':
                        pos_moves.append(f'{Config.tile_convert(x)}{Config.tile_convert(y-1, True)}')
                except IndexError: pass

        # Capturing
        if self.color != 'White':
            if self.color is not None:
                try:
                    if Config.c_convert(self.color) in Config.board[y+1][x+1]:
                        pos_moves.append(f'{Config.tile_convert(x+1)}{Config.tile_convert(y+1, True)}')
                except IndexError: pass
            else:
                try:
                    if Config.board[y+1][x+1] != '___':
                        pos_moves.append(f'{Config.tile_convert(x+1)}{Config.tile_convert(y+1, True)}')
                except IndexError: pass

        # En Passant


        return sorted(pos_moves)

    def promote(): pass

class Knight(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)

    def possible_moves(self):
        pos_moves = []
        for x_off, y_off in ( (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1) ):
            new_x = self.x + x_off
            new_y = self.y + y_off
            if 0 <= new_x < Config.b_len and 0 <= new_y < Config.b_len:
                if self.color is not None:
                    if self.color[0].lower() not in Config.board[new_y][new_x]:
                        pos_moves.append(f'{Config.tile_convert(new_x)}{Config.tile_convert(new_y, True)}')
                else:
                    pos_moves.append(f'{Config.tile_convert(new_x)}{Config.tile_convert(new_y, True)}')

        return sorted(pos_moves)

    def demo(self, rec=True):  # default board
        for pos in ('e1', 'f3', 'g5', 'h7', 'f8', 'e6', 'c5', 'd3', 'e1'):
            self.teleport(pos, rec)
            sleep(1)

class Rook(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        # Left
        for new_x in range(x+1, Config.b_len):
            if self.color is not None:
                if self.color[0].lower() not in Config.board[y][new_x]:
                    pos_moves.append(f'{Config.tile_convert(new_x)}{Config.tile_convert(y, True)}')
                    if Config.board[y][new_x] != '___': break
                else: break
            else:
                pos_moves.append(f'{Config.tile_convert(new_x)}{Config.tile_convert(y, True)}')

        # Right
        for new_x in reversed(range(x)):
            if self.color is not None:
                if self.color[0].lower() not in Config.board[y][new_x]:
                    pos_moves.append(f'{Config.tile_convert(new_x)}{Config.tile_convert(y, True)}')
                    if Config.board[y][new_x] != '___': break
                else: break
            else:
                pos_moves.append(f'{Config.tile_convert(new_x)}{Config.tile_convert(y, True)}')
        # Up
        for new_y in reversed(range(y)):
            if self.color is not None:
                if self.color[0].lower() not in Config.board[new_y][x]:
                    pos_moves.append(f'{Config.tile_convert(x)}{Config.tile_convert(new_y, True)}')
                    if Config.board[new_y][x] != '___': break
                else: break
            else:
                pos_moves.append(f'{Config.tile_convert(x)}{Config.tile_convert(new_y, True)}')

        # Down
        for new_y in range(y+1, Config.b_len):
            if self.color is not None:
                if self.color[0].lower() not in Config.board[new_y][x]:
                    pos_moves.append(f'{Config.tile_convert(x)}{Config.tile_convert(new_y, True)}')
                    if Config.board[new_y][x] != '___': break
                else: break
            else:
                pos_moves.append(f'{Config.tile_convert(x)}{Config.tile_convert(new_y, True)}')

        return sorted(pos_moves)

    def castle(): pass

    def demo(self, rec=True):  # default board
        for pos in ('a1', 'a8', 'h8', 'h1', 'a1'):
            self.teleport(pos, rec)
            sleep(1)

Config.new_board('default')

r1 = Rook(color='w')
n1 = Knight('a5', color='b')
p1 = Pawn('e1', color='w')
p2 = Pawn('e8', color='b')