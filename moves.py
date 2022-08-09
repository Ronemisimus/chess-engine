from board import Move
from constants import BISHOP, EMPTY, KING_CASTLING, KNIGHT, KNIGHT_MOVE_CHANGES, PAWN, QUEEN, QUEEN_CASTLING, ROOK, WHITE, validLocation,addLetter, BLACK

# pawn_location, enpassant_square - (letter,number)
# enpassant - (is the enpassant possible, pawns that can eat)
def pawn_moves(state,pawn_location):
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
        enpassantable = slot_left == state.enpassant
        if capturable or enpassantable:
            moves.append(Move(pawn_location,slot_left,""))
    if validLocation(*slot_right):
        capturable = state.board[slot_right].owner!=state.board[pawn_location].owner and \
            state.board[slot_right].owner != EMPTY
        enpassantable = slot_right == state.enpassant
        if capturable or enpassantable:
            moves.append(Move(pawn_location,slot_right,""))
    # promotions
    owner = state.board[pawn_location].owner
    promotion_rank = 7 if owner==WHITE else 1
    if pawn_location[1] == promotion_rank:
        moves = [Move(move.src,move.dest,prom) for move in moves for prom in ['q','r','b','n']]
    return moves


moveInDir = lambda location, dir: (addLetter(location[0],dir[0]),location[1]+dir[1])


def unchecked(state, square):
    valid = validLocation(*square)
    enemy = WHITE if state.board[square].owner == BLACK else BLACK
    if valid:
        knight_check = False
        for dir in KNIGHT_MOVE_CHANGES:
            slot = moveInDir(square,dir)
            if validLocation(*slot) and state.board[slot].owner==enemy and \
                state.board[slot].tool == KNIGHT:
                knight_check = True
        pawn_check = False
        direction = 1 if enemy == BLACK else -1
        pawn_dirs = [ (-1,direction) , (1,direction) ]
        for dir in pawn_dirs:
            slot = moveInDir(square,dir)
            if validLocation(*slot) and state.board[slot].owner==enemy and \
                state.board[slot].tool == PAWN:
                pawn_check = True
        rook_check = False
        bishop_check=False
        rook_dirs = [(0,1),(1,0),(0,-1),(-1,0)]
        bishop_dirs = [(1,1),(1,-1),(-1,-1),(-1,1)]
        for dir in rook_dirs:
            slot = moveInDir(square,dir)
            while validLocation(*slot) and state.board[slot].owner == EMPTY:
                slot = moveInDir(slot,dir)
            if validLocation(*slot) and state.board[slot].owner == enemy:
                rook_check = rook_check or state.board[slot].tool == ROOK or \
                    state.board[slot].tool == QUEEN
        for dir in bishop_dirs:
            slot = moveInDir(square,dir)
            while validLocation(*slot) and state.board[slot].owner == EMPTY:
                slot = moveInDir(slot,dir)
            if validLocation(*slot) and state.board[slot].owner == enemy:
                bishop_check = bishop_check or state.board[slot].tool == BISHOP or \
                    state.board[slot].tool == QUEEN
        if knight_check or pawn_check or rook_check or bishop_check:
            return False
        else:
            return True
    return False


def clear(state,square):
    valid = validLocation(square)
    return valid and state.board[square].owner == EMPTY


def king_moves(state,king_loc):
    moves=[]
    # castling
    back_rank = 1 if state.board[king_loc].owner==WHITE else 8
    if state.castling[state.to_move][KING_CASTLING]:
        slots = [('f',back_rank),('g',back_rank)]
        clear_slots = True
        for slot in slots:
            clear_slots = clear_slots and state.board[slot].owner==EMPTY
        if clear_slots:
            moves.append(Move(king_loc,slots[1],""))
    if state.castling[state.to_move][QUEEN_CASTLING]:
        slots = [('b',back_rank),('c',back_rank),('d',back_rank)]
        clear_slots = True
        for slot in slots:
            clear_slots = clear_slots and state.board[slot].owner==EMPTY
        if clear_slots:
            moves.append(Move(king_loc,slots[1],""))
    # normal moves
    king_dirs = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
    for dir in king_dirs:
        slot = moveInDir(king_loc,dir)
        if validLocation(*slot) and state.board[slot].owner!=state.board[king_loc].owner:
            moves.append(Move(king_loc,slot,""))
    return moves



def knight_moves(state,knight_pos):
    moves=[]
    for dir in KNIGHT_MOVE_CHANGES:
        slot = moveInDir(knight_pos,dir)
        if validLocation(*slot) and state.board[slot].owner!=state.board[knight_pos].owner:
            moves.append(Move(knight_pos,slot,""))
    return moves



def rook_moves(state,rook_loc):
    moves=[]
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for dir in directions:
        # walk in dir while dest is empty
        dest = moveInDir(rook_loc,dir)
        blocked = False
        while validLocation(*dest) and state.board[dest].owner!=state.board[rook_loc].owner and not blocked:
            moves.append(Move(rook_loc,dest,""))
            blocked = state.board[dest].owner!=EMPTY
            dest = moveInDir(dest,dir)    
    return moves

def bishop_moves(state,bishop_loc):
    moves=[]
    directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
    for dir in directions:
        # walk in dir while dest is empty
        dest = moveInDir(bishop_loc,dir)
        blocked = False 
        while validLocation(*dest) and state.board[dest].owner!=state.board[bishop_loc].owner and not blocked:
            moves.append(Move(bishop_loc,dest,""))
            blocked = state.board[dest].owner!=EMPTY
            dest = moveInDir(dest,dir)    
    return moves

def queen_moves(state,queen_loc):
    moves=[]
    moves.extend(bishop_moves(state,queen_loc))
    moves.extend(rook_moves(state,queen_loc))
    return moves