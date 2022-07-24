from board import Move
from chessState import ChessState
from constants import EMPTY, KING_CASTLING, QUEEN_CASTLING, WHITE, validLocation,addLetter, BLACK

# pawn_location, enpassant_square - (letter,number)
# enpassant - (is the enpassant possible, pawns that can eat)
def pawn_moves(state:ChessState,pawn_location,enpassant_square):
    moves = []
    direction = 1 if state.to_move == WHITE else -1
    # forward
    slot1 = (pawn_location[0],pawn_location[1]+direction)
    slot2 = (pawn_location[0],pawn_location[1]+2*direction)
    if validLocation(*slot1) and state.board[slot1].owner==EMPTY:
        moves.append(Move(pawn_location,slot1,""))
        start_pawn = pawn_location[1] == 2 or pawn_location[1] == 7
        # double forward
        if validLocation(*slot2) and start_pawn and state.board[slot2].owner==EMPTY:
            moves.append(Move(pawn_location,slot2,""))
    # eat sideways - can be enpassant
    slot_left = (addLetter(pawn_location[0],-1),pawn_location[1]+direction)
    slot_right = (addLetter(pawn_location[0],1),pawn_location[1]+direction)
    if validLocation(*slot_left):
        capturable = state.board[slot_left].owner!=state.board[pawn_location].owner and \
            state.board[slot_left].owner != EMPTY
        enpassantable = slot_left == enpassant_square
        if capturable or enpassantable:
            moves.append(Move(pawn_location,slot_left,""))
    if validLocation(*slot_right):
        capturable = state.board[slot_right].owner!=state.board[pawn_location].owner and \
            state.board[slot_right].owner != EMPTY
        enpassantable = slot_right == enpassant_square
        if capturable or enpassantable:
            moves.append(Move(pawn_location,slot_right,""))
    # promotions
    owner = state.board[pawn_location].owner
    promotion_rank = 7 if owner==WHITE else 1
    if pawn_location[1] == promotion_rank:
        moves = [Move(move.src,move.dest,prom) for move in moves for prom in ['q','r','b','n']]
    return moves


moveInDir = lambda location, dir: (addLetter(location[0],dir[0]),location[1]+dir[1])


def unchecked(state:ChessState, square):
    valid = validLocation(*square)
    enemy = WHITE if state.to_move == BLACK else BLACK
    if valid:
        return True
    return False


def clear(state:ChessState,square):
    valid = validLocation(square)
    return valid and state.board[square].owner == EMPTY


def king_moves(state:ChessState,king_loc):
    moves=[]
    # castling
    if state.castling[state.to_move][KING_CASTLING]:
        slots = [('f',1),('g',1)]
        clear_slots = True
        for slot in slots:
            clear_slots = clear_slots and state.board[slot].owner==EMPTY
        if clear_slots:
            moves.append(Move(king_loc,slots[1],""))
    if state.castling[state.to_move][QUEEN_CASTLING]:
        slots = [('b',1),('c',1),('d',1)]
        clear_slots = True
        for slot in slots:
            clear_slots = clear_slots and state.board[slot].owner==EMPTY
        if clear_slots:
            moves.append(Move(king_loc,slots[1],""))
    # normal moves
    king_dirs = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
    for dir in king_dirs:
        slot = moveInDir(king_loc,dir)
        if validLocation(*slot) and state.board[slot].owner==EMPTY:
            moves.append(Move(king_loc,slot,""))
    return moves



def knight_moves(state:ChessState,knight_pos):
    moves=[]
    return moves



def rook_moves(state:ChessState,rook_loc):
    moves=[]
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for dir in directions:
        # walk in dir while dest is empty
        dest = moveInDir(rook_loc,dir)
    
    return moves

def bishop_moves(state:ChessState,bishop_loc):
    moves=[]
    directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
    for dir in directions:
        # walk in dir while dest is empty
        dest = moveInDir(bishop_loc,dir)
    return moves

def queen_moves(state:ChessState,queen_loc):
    moves=[]
    moves.extend(bishop_moves(state,queen_loc))
    moves.extend(rook_moves(state,queen_loc))
    return moves