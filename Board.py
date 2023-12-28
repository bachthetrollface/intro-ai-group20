import pygame
import chess
from Square import Square

columns = 'abcdefgh'

def get_pos_from_coord(coord:str):
    for i in range(8):
        if columns[i] == coord[0]:
            res = (i, 8 - int(coord[1]))
            break
    return res

def get_coord_from_pos(x, y):
    return columns[x] + str(8-y)

class GUI_Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = chess.WHITE
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.chess_board = chess.Board()
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        output = set()
        for y in range(8):
            for x in range(8):
                output.add(Square(x, y, self.tile_width, self.tile_height))
        return output

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece
    
    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))
                    # Set occupying piece in square based on config
                    if piece[1] == 'R':
                        square.occupying_piece = Piece((x,y), chess.ROOK, chess.WHITE if piece[0] == 'w' else chess.BLACK, self)
                    elif piece[1] == 'N':
                        square.occupying_piece = Piece((x,y), chess.KNIGHT, chess.WHITE if piece[0] == 'w' else chess.BLACK, self)
                    elif piece[1] == 'B':
                        square.occupying_piece = Piece((x,y), chess.BISHOP, chess.WHITE if piece[0] == 'w' else chess.BLACK, self)
                    elif piece[1] == 'Q':
                        square.occupying_piece = Piece((x,y), chess.QUEEN, chess.WHITE if piece[0] == 'w' else chess.BLACK, self)
                    elif piece[1] == 'K':
                        square.occupying_piece = Piece((x,y), chess.KING, chess.WHITE if piece[0] == 'w' else chess.BLACK, self)
                    elif piece[1] == 'P':
                        square.occupying_piece = Piece((x,y), chess.PAWN, chess.WHITE if piece[0] == 'w' else chess.BLACK, self)
    
    def get_possible_moves(self):
        res = set()
        for square in self.squares:
            if square.occupying_piece is not None:
                for valid_move in square.occupying_piece.get_moves():
                    res.add(valid_move)
        return res
    
    def is_checkmate(self):
        return self.chess_board.is_checkmate()
    def is_draw(self):
        return self.chess_board.is_stalemate() or self.chess_board.is_seventyfive_moves() or self.chess_board.is_fivefold_repetition() or self.chess_board.is_insufficient_material()
    
    def is_end_game(self):
        res = ''
        if self.is_checkmate():
            side = 'White' if self.turn == chess.BLACK else 'Black'
            res = side + ' wins!'
        elif self.is_draw():
            res = 'Draw!'
        if res != '':
            return res
        return False
    
    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        try:
            move_made = self.selected_piece.move(clicked_square)
        except AttributeError:
            move_made = None

        if move_made is not None:
            return move_made

        elif self.selected_piece is None:
            # Select a piece
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    # 1. Currently not selecting any piece; 2. Clicking on a piece; 3. Clicking on self's side's piece
                    self.selected_piece = clicked_square.occupying_piece

        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                # Change selected piece
                self.selected_piece = clicked_square.occupying_piece
    
    def draw(self, display):
        cur_turn = self.turn
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves():
                square.highlight = True
        for square in self.squares:
            if square.occupying_piece is not None:
                if square.occupying_piece.piece_type == chess.KING and square.occupying_piece.color == cur_turn:
                    if self.is_checkmate():
                        square.checkmate = True
                    elif self.chess_board.is_check():
                        square.check = True
                    else:
                        square.check = False
                        square.checkmate = False
                elif square.occupying_piece.piece_type != chess.KING:
                    square.check = square.checkmate = False
            else:
                square.check = square.checkmate = False
            square.draw(display)



class Piece(chess.Piece):
    def __init__(self, pos, type:chess.PieceType, color:chess.Color, board:GUI_Board):
        super().__init__(type, color)
        self.pos = pos # position on 8x8 board with indices from 0 to 7
        self.coord = get_coord_from_pos(*self.pos) # coordinate by chess rule
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.gui_board = board
        self.img = self.get_img()
    
    def get_img(self):
        img_path = 'data/imgs/'
        pieces = ['_pawn.png', '_knight.png', '_bishop.png', '_rook.png', '_queen.png', '_king.png']
        if self.color == chess.WHITE:
            img_path += 'w'
        else:
            img_path += 'b'
        img_path += pieces[self.piece_type - 1]
        res = pygame.image.load(img_path)
        res = pygame.transform.scale(res, (self.gui_board.tile_width - 35, self.gui_board.tile_height - 35))
        return res
    
    def get_moves(self):
        output = set()
        available_moves = {move.uci() for move in self.gui_board.chess_board.generate_legal_moves()}
        
        for move in available_moves:
            if move[0:2] == self.coord:
                output.add(move)
        return output
    
    def get_valid_moves(self):
        output = set()
        for move in self.get_moves():
            sq_pos = get_pos_from_coord(move[2:4])
            square = self.gui_board.get_square_from_pos(sq_pos)
            output.add(square)
        return output


    def move(self, square:Square, force=False):
        for i in self.gui_board.squares:
            i.highlight = False
        
        mark_castling = False
        mark_en_passant = False
        if self.piece_type == chess.KING and abs(square.x - self.x) == 2 and self.gui_board.chess_board.has_castling_rights(self.gui_board.turn):
            mark_castling = True
            side = 'KING_SIDE' if square.x > self.x else 'QUEEN_SIDE'
        if self.piece_type == chess.PAWN and abs(self.x - square.x) == 1 and abs(self.y - square.y) == 1 and square.occupying_piece == None:
            mark_en_passant = True
        
        if square in self.get_valid_moves() or force:           
            prev_square = self.gui_board.get_square_from_pos(self.pos)
            move_cur = self.coord
            self.pos, self.x, self.y = square.pos, square.x, square.y
            self.coord = get_coord_from_pos(*self.pos)
            prev_square.occupying_piece = None
            square.occupying_piece = self
            self.gui_board.selected_piece = None
            move_new = self.coord
            if self.piece_type == chess.PAWN:
                if (self.color == chess.WHITE and move_new[1] == '8') or (self.color == chess.BLACK and move_new[1] == '1'):
                    move_new += 'q'
                    self.piece_type = chess.QUEEN
                    self.img = self.get_img()
            if not force:
                self.gui_board.chess_board.push_san(move_cur + move_new)
            
            if mark_en_passant:
                captured_pawn_at = self.gui_board.get_square_from_pos((square.x, prev_square.y))
                captured_pawn_at.occupying_piece = None
            
            if mark_castling:
                if self.gui_board.turn == chess.WHITE:
                    rook_cur_pos = (7, 7) if side == 'KING_SIDE' else (0, 7)
                    rook_new_pos = (5, 7) if side == 'KING_SIDE' else (3, 7)
                elif self.gui_board.turn == chess.BLACK:
                    rook_cur_pos = (7, 0) if side == 'KING_SIDE' else (0, 0)
                    rook_new_pos = (5, 0) if side == 'KING_SIDE' else (3, 0)
                rook = self.gui_board.get_piece_from_pos(rook_cur_pos)
                rook.move(self.gui_board.get_square_from_pos(rook_new_pos), force=True)
            if not force:
                self.gui_board.turn = chess.WHITE if self.gui_board.turn == chess.BLACK else chess.BLACK
            return move_cur + move_new
        
        else:
            self.gui_board.selected_piece = None
            return None