import chess
import random as rd
import Board

squares = {
    chess.A8:(0,0), chess.B8:(0,1), chess.C8:(0,2), chess.D8:(0,3), chess.E8:(0,4), chess.F8:(0,5), chess.G8:(0,6), chess.H8:(0,7),
    chess.A7:(1,0), chess.B7:(1,1), chess.C7:(1,2), chess.D7:(1,3), chess.E7:(1,4), chess.F7:(1,5), chess.G7:(1,6), chess.H7:(1,7),
    chess.A6:(2,0), chess.B6:(2,1), chess.C6:(2,2), chess.D6:(2,3), chess.E6:(2,4), chess.F6:(2,5), chess.G6:(2,6), chess.H6:(2,7),
    chess.A5:(3,0), chess.B5:(3,1), chess.C5:(3,2), chess.D5:(3,3), chess.E5:(3,4), chess.F5:(3,5), chess.G5:(3,6), chess.H5:(3,7),
    chess.A4:(4,0), chess.B4:(4,1), chess.C4:(4,2), chess.D4:(4,3), chess.E4:(4,4), chess.F4:(4,5), chess.G4:(4,6), chess.H4:(4,7),
    chess.A3:(5,0), chess.B3:(5,1), chess.C3:(5,2), chess.D3:(5,3), chess.E3:(5,4), chess.F3:(5,5), chess.G3:(5,6), chess.H3:(5,7),
    chess.A2:(6,0), chess.B2:(6,1), chess.C2:(6,2), chess.D2:(6,3), chess.E2:(6,4), chess.F2:(6,5), chess.G2:(6,6), chess.H2:(6,7),
    chess.A1:(7,0), chess.B1:(7,1), chess.C1:(7,2), chess.D1:(7,3), chess.E1:(7,4), chess.F1:(7,5), chess.G1:(7,6), chess.H1:(7,7)
    } # Mapping of board squares to positions for accessing board values

piece_values = {chess.PAWN:100, chess.KNIGHT:320, chess.BISHOP:330, chess.ROOK:350, chess.QUEEN:900, chess.KING:20000}

board_values = {chess.PAWN:  [[  0,   0,   0,   0,   0,   0,   0,   0],
                              [ 50,  50,  50,  50,  50,  50,  50,  50],
                              [ 10,  10,  20,  30,  30,  20,  10,  10],
                              [  5,   5,  10,  25,  25,  10,   5,   5],
                              [  0,   0,   0,  20,  20,   0,   0,   0],
                              [  5,  -5, -10,   0,   0, -10,  -5,   5],
                              [  5,  10,  10, -20, -20,  10,  10,   5],
                              [  0,   0,   0,   0,   0,   0,   0,   0]],

                chess.KNIGHT:[[-50, -40, -30, -30, -30, -30, -40, -50],
                              [-40, -20,   0,   0,   0,   0, -20, -40],
                              [-30,   0,  10,  15,  15,  10,   0, -30],
                              [-30,   5,  15,  20,  20,  15,   5, -30],
                              [-30,   0,  15,  20,  20,  15,   0, -30],
                              [-30,   5,   5,  15,  15,   5,   5, -30],
                              [-40, -20,   0,   5,   5,   0, -20, -40],
                              [-50, -40, -30, -30, -30, -30, -40, -50]],

                chess.BISHOP:[[-20, -10, -10, -10, -10, -10, -10, -20],
                              [-10,   0,   0,   0,   0,   0,   0, -10],
                              [-10,   0,   5,  10,  10,   5,   0, -10],
                              [-10,   5,   5,  10,  10,   5,   5, -10],
                              [-10,   0,  10,  10,  10,  10,   0, -10],
                              [-10,  10,  10,  10,  10,  10,  10, -10],
                              [-10,   5,   0,   0,   0,   0,   5, -10],
                              [-20, -10, -10, -10, -10, -10, -10, -20]],

                chess.ROOK:  [[  0,   0,   0,   0,   0,   0,   0,   0],
                              [  5,  10,  10,  10,  10,  10,  10,   5],
                              [ -5,   0,   0,   0,   0,   0,   0,  -5],
                              [ -5,   0,   0,   0,   0,   0,   0,  -5],
                              [ -5,   0,   0,   0,   0,   0,   0,  -5],
                              [ -5,   0,   0,   0,   0,   0,   0,  -5],
                              [ -5,   0,   0,   0,   0,   0,   0,  -5],
                              [  0,   0,   0,  10,   5,  10,   0,   0]],

                chess.QUEEN: [[-20, -10, -10,  -5,  -5, -10, -10, -20],
                              [-10,   0,   0,   0,   0,   0,   0, -10],
                              [-10,   0,   5,   5,   5,   5,   0, -10],
                              [ -5,   0,   5,   5,   5,   5,   0,  -5],
                              [  0,   0,   5,   5,   5,   5,   0,  -5],
                              [-10,   5,   5,   5,   5,   5,   0, -10],
                              [-10,   0,   5,   0,   0,   0,   0, -10],
                              [-20, -10, -10,  -5,  -5, -10, -10, -20]],

                chess.KING:  [[-30, -40, -40, -50, -50, -40, -40, -30],
                              [-30, -40, -40, -50, -50, -40, -40, -30],
                              [-30, -40, -40, -50, -50, -40, -40, -30],
                              [-30, -40, -40, -50, -50, -40, -40, -30],
                              [-20, -30, -30, -40, -40, -30, -30, -20],
                              [-10, -20, -20, -20, -20, -20, -20, -10],
                              [ 20,  20,   0,   0,   0,   0,  20,  20],
                              [ 20,  30,  10,   0,   0,  10,  30,  20]]
                }

def get_board_val(board:chess.Board):
    if is_draw(board):
        return 0
    if board.is_checkmate():
        return 99999 if board.outcome().winner == chess.WHITE else -99999
    val = 0
    for square in squares:
        tmp_piece = board.piece_at(square)
        if tmp_piece is not None:
            tmp_color = tmp_piece.color
            tmp_type = tmp_piece.piece_type
            tmp_pos = squares[square]
            if tmp_color == chess.WHITE:
                val = val + piece_values[tmp_type] + board_values[tmp_type][tmp_pos[0]][tmp_pos[1]]
            else:
                #Flip the value board vertically and multiply by (-1)
                val = val + (piece_values[tmp_type] + board_values[tmp_type][7-tmp_pos[0]][tmp_pos[1]]) * (-1)
    return val

def is_draw(board:chess.Board):
    return board.is_stalemate() or board.is_seventyfive_moves() or board.is_fivefold_repetition() or board.is_insufficient_material()

#######################################################################
# Global variables/constant
d = 0               # Maximum depth (assign value later)
best_moves = []     # List of the best moves found
nodes_count = 0     # To count the number of nodes visited after calculation
openings = []       # Collection of opening sequences
INFINITY = 960240   # Any huge number

def minimax_search(board: Board.GUI_Board, depth = 5, maximizing = False):
    global d
    global best_moves
    global nodes_count
    d = depth
    best_moves.clear()
    nodes_count = 0

    if board.chess_board.is_game_over():
        return None 
        #Unable to make a move since the game is over

    tmp_board = board.chess_board.fen()
    best_value = alpha_beta(tmp_board, depth, -INFINITY, INFINITY, maximizing)
    chosen_move = best_moves[rd.randint(0, len(best_moves) - 1)]  #Randomly choose one of the best moves found

    #Make the move
    best_piece = board.get_piece_from_pos(Board.get_pos_from_coord(chosen_move[0:2]))
    dst_sq = board.get_square_from_pos(Board.get_pos_from_coord(chosen_move[2:4]))
    best_piece.move(dst_sq)

    #Print information
    print("Nodes visited:", nodes_count)
    print("Best move value found:", best_value)
    print("Best moves found:", *best_moves)
    print("Chosen move:", chosen_move)
    return chosen_move

def get_move_value(move, board_fen):
    tmp_board = chess.Board(board_fen)
    tmp_board.push_san(move)
    return get_board_val(tmp_board)

def alpha_beta(board_fen, depth, a, b, maximizing):
    global best_moves
    global nodes_count
    global d

    tmp_board = chess.Board(board_fen)
    if (depth <= 0) or (tmp_board.is_game_over()):
        return get_board_val(tmp_board)

    moves = [move.uci() for move in tmp_board.generate_legal_moves()]
    
    if maximizing:
        # Sort the moves by board value in ascending order
        if depth >= 2:
            moves.sort(key = lambda x: get_move_value(x, board_fen), reverse=True)
        
        value_max = -INFINITY
        for move in moves:
            nodes_count += 1
            tmp_board.push_san(move)
            value = alpha_beta(tmp_board.fen(), depth - 1, a, b, False)
            tmp_board.pop()
            if depth == d: #Record the best moves
                if value > value_max:
                    value_max = value
                    best_moves.clear()
                    best_moves.append(move)
                elif value == value_max:
                    best_moves.append(move)
            else:
                value_max = max(value, value_max)
            a = max(a, value_max)
            if a >= b:
                break
        return value_max
    
    else:
        # Sort the moves by board value in descending order
        if depth >= 2:
            moves.sort(key = lambda x: get_move_value(x, board_fen))
        
        value_min = INFINITY
        for move in moves:
            nodes_count += 1
            tmp_board.push_san(move)
            value = alpha_beta(tmp_board.fen(), depth - 1, a, b, True)
            tmp_board.pop()
            if depth == d: #Record the best moves
                if value < value_min:
                    value_min = value
                    best_moves.clear()
                    best_moves.append(move)
                elif value == value_min:
                    best_moves.append(move)
            else:
                value_min = min(value, value_min)
            b = min(b, value_min)
            if b <= a:
                break
        return value_min

def initialize_openings():
    global openings
    with open('data/openings.txt') as open_sequences:
        while True:
            sequence = open_sequences.readline().split()
            if len(sequence) == 0:
                break
            openings.append(sequence)
    return

def opening_search(board: Board.GUI_Board, sequence: list):
    global best_moves
    global openings
    best_moves.clear()

    for line in openings:
        if sequence == line[0:len(sequence)] and line[len(sequence)] != 'None':
            best_moves.append(line[len(sequence)])
        else:
            openings.remove(line)

    # Make the move
    if len(best_moves) > 0:
        chosen_move = best_moves[rd.randint(0, len(best_moves) - 1)]  # Randomly choose one of the best moves found
        best_piece = board.get_piece_from_pos(Board.get_pos_from_coord(chosen_move[0:2]))
        dst_sq = board.get_square_from_pos(Board.get_pos_from_coord(chosen_move[2:4]))
        best_piece.move(dst_sq)

        # Print information
        print("Book moves found:", best_moves)
        print("Chosen move:", chosen_move)
        return chosen_move

    #No book move found
    else:
        return None
