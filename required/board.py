import string

import required.chesserrors as ce
from required.layouts import LAYOUTS


class Chessboard:
    """The chessboard.

    The board can have different sizes, but it is 8x8 by default. There
    is a list of predefined sizes in Chessboard.TYPES, but custom sizes are
    available by passing "custom<n>" to the constructor, where <n> is an
    integer between 1 and 26.
    """

    DEMO_INTERVAL = .8  # seconds
    board = 'UNINITIALIZED'
    board_size = 'UNINITIALIZED'

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

    _LAYOUTS = LAYOUTS

    _LETTERS = string.ascii_lowercase

    @classmethod
    def new_board(cls, board_type='default', show=True):
        def size(x):
            return [['___' for _ in range(x)] for _ in range(x)], x

        can_print = False

        if board_type is not None:
            board_type = board_type.lower()

            if board_type.startswith('custom'):
                try:
                    board_type = int(board_type.replace('custom', '').strip())

                except ValueError: pass

                if 1 <= board_type <= 26:
                    cls.board, cls.board_size = size(board_type)
                    can_print = True
                else:
                    board_type = None
                    cls.new_board(board_type)
            elif board_type in cls.TYPES:
                cls.board, cls.board_size = size(cls.TYPES[board_type])
                can_print = True
            else:
                raise ce.InitialzeError(f'Unable to initialize board of unknown type {board_type}')

        else:
            raise ce.InitializeError('Unable to initialize board with a size lower than 1 or greater than 26')

        if can_print and show:
            cls.print_board()

    @classmethod
    def print_board(cls, leading=2, trailing=4):
        """Print the board to the console

        The number of leading and trailing newlines can be configured.
        Their respective values are 2 and 4 by default.
        """
        def print_letters(n=True):
            print(" " + "".join(f"{letter:>7}" for letter in cls._LETTERS[:cls.board_size]))
            if n: print()

        print("\n"*leading, end="")

        print_letters()

        for i in range(cls.board_size):
            print(f'{cls.board_size - i:>2}  {cls.board[i]}  {cls.board_size - i:>2}\n')

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
            return cls.board_size - int(x)

    @classmethod
    def l_num_to_coord(cls, pos):
        return Chessboard.board_size - int(pos[1]), int(Chessboard.tile_convert(pos[0]))

    @classmethod
    def coord_to_tile(cls, x, y):
        return f'{Chessboard.tile_convert(x)}{Chessboard.tile_convert(y, True)}'

    @classmethod
    def c_convert(cls, color):
        if color == 'white':
            return 'b'
        if color == "black":
            return 'w'
        if color is None:
            return '_'
