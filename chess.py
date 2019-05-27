import string
from time import sleep
from itertools import count
from gc import get_objects


class Chessboard:
    """The chessboard.

    The board can have different sizes, but is 8x8 by default. There
    is a list of predefined sizes in Chessboard.TYPES, but custom sizes are
    available by passing "custom<n>" to the constructor, where <n> is an
    integer between 1 and 26.
    """

    DEMTIME = .8  # seconds
    board = 'UNINITIALIZED'
    b_len = 'UNINITIALIZED'

    TYPES = {
        'min': 1, 'miniature': 3, 'small': 5, 'default': 8,
        'extended': 11, 'large': 15, 'massive': 20, 'max': 26
    }

    WHITE_PIECES = {
        'Pawn': "♙", 'Rook': "♖", 'Knight': "♘",
        'Bishop': "♗", 'King': "♔", 'Queen': "♕"
    }

    BLACK_PIECES = {
        'Pawn': "♟", 'Rook': "♜", 'Knight': "♞",
        'Bishop': "♝", 'King': "♚", 'Queen': "♛"
    }

    _LETTERS = string.ascii_lowercase

    @classmethod
    def new_board(cls, btype='default'):
        def size(x):
            return [['___' for _ in range(x)] for _ in range(x)], x

        can_print = False

        if btype is not None:
            btype = btype.lower()

            if btype.startswith('custom'):
                try:
                    btype = int(btype.replace('custom', '').strip())

                except ValueError: pass

                if 1 <= btype <= 26:
                    cls.board, cls.b_len = size(btype)
                    can_print = True
                else:
                    btype = None
                    cls.new_board(btype)
            elif btype in cls.TYPES:
                cls.board, cls.b_len = size(cls.TYPES[btype])
                can_print = True
            else:
                raise ValueError(f'Unable to initialize board of unknown type {btype}')

        else:
            raise ValueError('Unable to initialize board with a size lower than 1 or greater than 26')

        if can_print:
            cls.print_board()

    @classmethod
    def print_board(cls, leading=2, trailing=4):
        """Print the board to the console

        The number of leading and trailing newlines can be configured.
        Their respective values are 2 and 4 by default.
        """
        def print_letters(n=True):
            print(" " + "".join(f"{letter:>7}" for letter in cls._LETTERS[:cls.b_len]))
            if n: print()

        print("\n"*leading, end="")

        print_letters()

        for i in range(cls.b_len):
            print(f'{cls.b_len-i:>2}  {cls.board[i]}  {cls.b_len-i:>2}\n')

        print_letters(False)

        print("\n"*trailing, end="")

    @classmethod
    def tile_convert(cls, x, display_tile=False):
        if not display_tile:
            if isinstance(x, str):
                return cls._LETTERS.index(x)
            else:
                return cls._LETTERS[x]
        else:  # display_tile converts the letter in {letter}{number} to a number
            return cls.b_len - int(x)

    @classmethod
    def l_num_to_coord(cls, pos):
        return Chessboard.b_len - int(pos[1]), int(Chessboard.tile_convert(pos[0]))

    @classmethod
    def coord_to_tile(cls, x, y):
        return f'{Chessboard.tile_convert(x)}{Chessboard.tile_convert(y, True)}'

    @classmethod
    def c_convert(cls, color):
        if color == 'White':
            return 'b'
        if color == "Black":
            return 'w'

class ChessPiece:
    def __init__(self, pos, color, num, piece):
        self.x = int(Chessboard.tile_convert(pos[0]))
        self.y = Chessboard.b_len - int(pos[1])
        self.color = color
        self.piece = piece
        self.pieceid = num
        self.moves = 0
        self.captured = []
        self.erased = False
        self.set_id()
        self.create()
        Chessboard.print_board()

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
        if Chessboard.board[self.y][self.x] != '___':
            po = Chessboard.board[self.y][self.x]
            print(f'Piece {po} erased to make room for {self.pieceid}')

        Chessboard.board[self.y][self.x] = self.pieceid

    def teleport(self, pos, record=False):
        Chessboard.board[self.y][self.x] = '___'

        if record:
            self.moves += 1
            coord = Chessboard.l_num_to_coord(pos)
            if Chessboard.board[coord[0]][coord[1]] != '___':
                self.captured.append(Chessboard.board[coord[0]][coord[1]])
                print(f'{self.pieceid} has captured {Chessboard.board[coord[0]][coord[1]]}!')

        self.x = Chessboard.tile_convert(pos[0])
        self.y = Chessboard.tile_convert(pos[1], True)

        Chessboard.board[self.y][self.x] = self.pieceid

        Chessboard.print_board()

    def move(self, pos):
        if pos in self.possible_moves():
            coord = Chessboard.l_num_to_coord(pos)
            if Chessboard.board[coord[0]][coord[1]] != '___':
                self.captured.append(Chessboard.board[coord[0]][coord[1]])
                print(f'{self.pieceid} has captured {Chessboard.board[coord[0]][coord[1]]}!')
                # Erase piece

            if self.__class__ == Pawn:
                if abs(int(pos[1]) - Chessboard.tile_convert(self.y, True)) == 2:
                    self.two_move = True

            self.teleport(pos)
            self.moves += 1

        else:
            print(f'Unable to move to {pos}')


    def get_info(self):
        print(f'{self.__class__.__name__}:\n')
        print('ID: ', self.pieceid)
        print('Position: ', Chessboard.tile_convert(self.x), Chessboard.tile_convert(self.y, True), sep='')
        print('Color: ', self.color)

    def erase(self):  # Doesn't delete the piece. It can be brought back by moving it to a square
        Chessboard.board[self.y][self.x] = '___'
        self.erased = True

    def demo(self, rec=True):  # default board
        for pos in self.demo_moves:
            self.teleport(pos, rec)
            sleep(Chessboard.DEMTIME)

        if self.__class__ == Pawn:
            self.promote2(Queen)

    @staticmethod
    def castle(king, rook):
        if not king.moves and not rook.moves:
            if not king.in_check:
                pass


class Pawn(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)
        self.demo_moves = ('e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8')
        self.two_move = False

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        # Forward
        if not self.moves: # Starting Position
            if self.color != 'White':
                for new_y in (y+1, y+2):
                    try:
                        if Chessboard.board[new_y][x] == '___':
                            pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                        else: break
                    except IndexError: pass

            if self.color != 'Black':
                for new_y in (y-1, y-2):
                    try:
                        if Chessboard.board[new_y][x] == '___':
                            pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                        else: break
                    except IndexError: pass

        else:  # Post-Start
            if self.color != 'White':
                try:
                    if Chessboard.board[y + 1][x] == '___':
                        pos_moves.append(Chessboard.coord_to_tile(x, y + 1))
                except IndexError: pass

            if self.color != 'Black':
                try:
                    if Chessboard.board[y - 1][x] == '___':
                        pos_moves.append(Chessboard.coord_to_tile(x, y - 1))
                except IndexError: pass

        # Capturing
        if self.color != 'White':
            if self.color is not None:
                try:
                    if Chessboard.c_convert(self.color) in Chessboard.board[y + 1][x + 1]:
                        pos_moves.append(Chessboard.coord_to_tile(x + 1, y + 1))
                except IndexError: pass
            else:
                try:
                    if Chessboard.board[y + 1][x + 1] != '___':
                        pos_moves.append(Chessboard.coord_to_tile(x + 1, y + 1))
                except IndexError: pass

        if self.color != 'Black':
            if self.color is not None:
                try:
                    if Chessboard.c_convert(self.color) in Chessboard.board[y - 1][x - 1]:
                        pos_moves.append(Chessboard.coord_to_tile(x - 1, y - 1))
                except IndexError: pass
            else:
                try:
                    if Chessboard.board[y + 1][x + 1] != '___':
                        pos_moves.append(Chessboard.coord_to_tile(x - 1, y - 1))
                except IndexError: pass

        # En Passant


        return sorted(pos_moves)

    def promote(self, piece):  # oringal_piece = original_piece.promote(new_piece)
        pos = f'{Chessboard.tile_convert(self.x)}{Chessboard.tile_convert(self.y, True)}'

        return piece(pos, color=self.color, num='p')

    def promote2(self, piece):
        pos = f'{Chessboard.tile_convert(self.x)}{Chessboard.tile_convert(self.y, True)}'

        self.__class__ = piece
        self.__init__(pos, self.color, 'p')


class Knight(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)
        self.demo_moves = ('e1', 'f3', 'g5', 'h7', 'f8', 'e6', 'c5', 'd3', 'e1')

    def possible_moves(self):
        pos_moves = []
        for x_off, y_off in ( (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1) ):
            new_x = self.x + x_off
            new_y = self.y + y_off
            if 0 <= new_x < Chessboard.b_len and 0 <= new_y < Chessboard.b_len:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))

        return sorted(pos_moves)


class Bishop(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)
        self.demo_moves = ('a1', 'e5', 'b8', 'h2', 'e5', 'a1')

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        right_up = zip(range(x + 1, Chessboard.b_len), range(y - 1, -1, -1))
        right_down = zip(range(x + 1, Chessboard.b_len), range(y + 1, Chessboard.b_len))

        left_up = zip(range(x - 1, -1, -1), range(y - 1, -1, -1))
        left_down = zip(range(x - 1, -1, -1), range(y + 1, Chessboard.b_len))

        for r in (right_up, right_down, left_up, left_down):
            for new_x, new_y in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))
                        if Chessboard.board[new_y][new_x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))

        return sorted(pos_moves)


class Rook(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)
        self.demo_moves = ('a1', 'a8', 'h8', 'h1', 'a1')

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        # Horizontal
        for r in (range(x+1, Chessboard.b_len), reversed(range(x))):
            for new_x in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, y))
                        if Chessboard.board[y][new_x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, y))
                    if Chessboard.board[y][new_x] != '___': break

        # Vertical
        for r in (range(y+1, Chessboard.b_len), reversed(range(y))):
            for new_y in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][x]:
                        pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                        if Chessboard.board[new_y][x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                    if Chessboard.board[new_y][new_x] != '___': break

        return sorted(pos_moves)


class Queen(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)
        self.demo_moves = ('a1', 'h8', 'a8', 'h1', 'a1')

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        # Horizontal
        for r in (range(x+1, Chessboard.b_len), reversed(range(x))):
            for new_x in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, y))
                        if Chessboard.board[y][new_x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, y))
                    if Chessboard.board[y][new_x] != '___': break

        # Vertical
        for r in (range(y+1, Chessboard.b_len), reversed(range(y))):
            for new_y in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][x]:
                        pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                        if Chessboard.board[new_y][x] != '___': break
                    else: break
                else:
                    pos_moves.append(f'{Chessboard.tile_convert(x)}{Chessboard.tile_convert(new_y, True)}')
                    if Chessboard.board[new_y][new_x] != '___': break

        #Diagonal
        right_up = zip(range(x + 1, Chessboard.b_len), range(y - 1, -1, -1))
        right_down = zip(range(x + 1, Chessboard.b_len), range(y + 1, Chessboard.b_len))

        left_up = zip(range(x - 1, -1, -1), range(y - 1, -1, -1))
        left_down = zip(range(x - 1, -1, -1), range(y + 1, Chessboard.b_len))

        for r in (right_up, right_down, left_up, left_down):
            for new_x, new_y in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))
                        if Chessboard.board[new_y][new_x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))

        return sorted(pos_moves)


class King(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_'):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__)
        self.demo_moves = ('e4', 'd5', 'c4', 'c5', 'd6', 'e5', 'e4')
        self.in_check = False

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        for x_off, y_off in ( (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1) ):
            new_x = self.x + x_off
            new_y = self.y + y_off
            if 0 <= new_x < Chessboard.b_len and 0 <= new_y < Chessboard.b_len:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))


        return sorted(pos_moves)


class Game:
    game = count(1)

    def __init__(self):
        self.id = next(self.game)
        self.turn = 0
        self.end = False
        self.start()


    def start(self):
        if not self.end:
            self.proceed()
        else: pass

    @staticmethod
    def attacks_on(piece):
        pos = Chessboard.coord_to_tile(piece.x, piece.y)

        for instance in get_objects():
            if isinstance(instance, ChessPiece) and instance is not piece:
                if instance.color != piece.color or instance.color is None:
                    if pos in instance.possible_moves():
                        print(f'{piece.pieceid} is threatened by {instance.pieceid} on {pos}')

    def proceed(self):
        self.turn += 1


g = Game()
Chessboard.new_board('default')

r1 = Rook(color='w')
n1 = Knight('a5', color='b')
p1 = Pawn('e1', color='w')
p2 = Pawn('e8', color='b')
p3 = Pawn('f7', color='w')
r1.teleport('b3')

# p1.teleport('f4')
# p1 = p1.promote(Bishop)
# print(Config.white_pieces['Pawn'], Config.black_pieces['Pawn'])