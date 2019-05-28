from itertools import count
from gc import get_objects

from required.board import Chessboard
from required.pieces import ChessPiece, Pawn, Knight, Bishop, Rook, Queen, King


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


def setup_board(setup_type):
    layout = Chessboard._LAYOUTS[setup_type]

    for piece in layout:
        #eval(f'global {piece}')
        exec(f'{piece} = {layout[piece]}')


def test():
    """
    For bug testing. Changes often.
    """
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


if __name__ == '__main__':
    Chessboard.new_board('default', False)
    setup_board('default')
