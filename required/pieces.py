import time

import required.chesserrors as ce
from required.board import Chessboard


class ChessPiece:

    def __init__(self, pos, color, num, piece, show):
        self.x = int(Chessboard.tile_convert(pos[0]))
        self.y = Chessboard.board_size - int(pos[1])
        self.color = color
        self.piece = piece
        self.pieceid = num
        self.moves = 0
        self.captured = []
        self.erased = False
        self.set_id()
        self.create()

        if show:
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
        try:
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
                raise ce.CannotMoveError(f'Unable to move {self.pieceid} to {pos}')
        except TypeError:
            raise ce.CannotMoveError(f'{self.pieceid} has no possible moves!')

    def info(self):
        print(f'\n{self.__class__.__name__}:\n')
        print('ID: ', self.pieceid)
        print('Position: ', Chessboard.coord_to_tile(self.x, self.y), sep='')
        print('Color: ', self.color)

    def erase(self):  # Doesn't delete the piece. It can be brought back by moving it to a square
        Chessboard.board[self.y][self.x] = '___'
        self.erased = True

    def demo(self, rec=True):  # default board
        for pos in self.demo_moves:
            self.teleport(pos, rec)
            time.sleep(Chessboard.DEMO_INTERVAL)

        if self.__class__ == Pawn:
            self.promote2(Queen)

    @staticmethod
    def castle(king, rook):
        if not king.moves and not rook.moves:
            if not king.in_check:
                pass


class Pawn(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_', show=True):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__, show)
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
                    color = Chessboard.c_convert(self.color)

                    if Chessboard.board[y + 1][x + 1].startswith(color):
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
                    color = Chessboard.c_convert(self.color)

                    if Chessboard.board[y - 1][x - 1].startswith(color):
                        pos_moves.append(Chessboard.coord_to_tile(x - 1, y - 1))
                except IndexError: pass
            else:
                try:
                    if Chessboard.board[y + 1][x + 1] != '___':
                        pos_moves.append(Chessboard.coord_to_tile(x - 1, y - 1))
                except IndexError: pass

        # En Passant

        return sorted(pos_moves) or None

    def promote(self, piece):  # oringal_piece = original_piece.promote(new_piece)
        pos = Chessboard.coord_to_tile(self.x, self.y)

        return piece(pos, color=self.color, num='p')

    def promote2(self, piece):
        pos = Chessboard.coord_to_tile(self.x, self.y)

        self.__class__ = piece
        self.__init__(pos, self.color, 'p')


class Knight(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_', show=True):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__, show)
        self.demo_moves = ('e1', 'f3', 'g5', 'h7', 'f8', 'e6', 'c5', 'd3', 'e1')

    def possible_moves(self):
        pos_moves = []
        for x_off, y_off in ( (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1) ):
            new_x = self.x + x_off
            new_y = self.y + y_off
            if 0 <= new_x < Chessboard.board_size and 0 <= new_y < Chessboard.board_size:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))

        return sorted(pos_moves) or None


class Bishop(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_', show=True):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__, show)
        self.demo_moves = ('a1', 'e5', 'b8', 'h2', 'e5', 'a1')

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        right_up = zip(range(x + 1, Chessboard.board_size), range(y - 1, -1, -1))
        right_down = zip(range(x + 1, Chessboard.board_size), range(y + 1, Chessboard.board_size))

        left_up = zip(range(x - 1, -1, -1), range(y - 1, -1, -1))
        left_down = zip(range(x - 1, -1, -1), range(y + 1, Chessboard.board_size))

        for r in (right_up, right_down, left_up, left_down):
            for new_x, new_y in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))
                        if Chessboard.board[new_y][new_x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))

        return sorted(pos_moves) or None


class Rook(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_', show=True):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__, show)
        self.demo_moves = ('a1', 'a8', 'h8', 'h1', 'a1')

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        # Horizontal
        for r in (range(x+1, Chessboard.board_size), reversed(range(x))):
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
        for r in (range(y+1, Chessboard.board_size), reversed(range(y))):
            for new_y in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][x]:
                        pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                        if Chessboard.board[new_y][x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                    if Chessboard.board[new_y][new_x] != '___': break

        return sorted(pos_moves) or None


class Queen(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_', show=True):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__, show)
        self.demo_moves = ('a1', 'h8', 'a8', 'h1', 'a1')

    def possible_moves(self):
        pos_moves = []

        x, y = self.x, self.y

        # Horizontal
        for r in (range(x+1, Chessboard.board_size), reversed(range(x))):
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
        for r in (range(y+1, Chessboard.board_size), reversed(range(y))):
            for new_y in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][x]:
                        pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                        if Chessboard.board[new_y][x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(x, new_y))
                    if Chessboard.board[new_y][new_x] != '___': break

        # Diagonal
        right_up = zip(range(x + 1, Chessboard.board_size), range(y - 1, -1, -1))
        right_down = zip(range(x + 1, Chessboard.board_size), range(y + 1, Chessboard.board_size))

        left_up = zip(range(x - 1, -1, -1), range(y - 1, -1, -1))
        left_down = zip(range(x - 1, -1, -1), range(y + 1, Chessboard.board_size))

        for r in (right_up, right_down, left_up, left_down):
            for new_x, new_y in r:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))
                        if Chessboard.board[new_y][new_x] != '___': break
                    else: break
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))

        return sorted(pos_moves) or None


class King(ChessPiece):
    def __init__(self, pos='a1', color=None, num='_', show=True):
        ChessPiece.__init__(self, pos, color, num, self.__class__.__name__, show)
        self.demo_moves = ('e4', 'd5', 'c4', 'c5', 'd6', 'e5', 'e4')
        self.in_check = False

    def possible_moves(self):
        pos_moves = []

        for x_off, y_off in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)):
            new_x = self.x + x_off
            new_y = self.y + y_off
            if 0 <= new_x < Chessboard.board_size and 0 <= new_y < Chessboard.board_size:
                if self.color is not None:
                    if self.color[0].lower() not in Chessboard.board[new_y][new_x]:
                        pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))
                else:
                    pos_moves.append(Chessboard.coord_to_tile(new_x, new_y))

        return sorted(pos_moves) or None
