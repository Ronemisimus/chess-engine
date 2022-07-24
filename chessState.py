from constants import EMPTY, KING, KING_CASTLING, PAWN, QUEEN_CASTLING, ROOK, addLetter, WHITE, BLACK, validLocation
from board import Board, Move,Piece

def get_board(fen:str):
    board = Board()
    pieces = {}
    fen = fen.split(" ")
    board_str = fen[0]
    fen = " ".join(fen[1:])
    board_str = board_str.split("/")
    index = 8
    for line in board_str:
        letter = 'a'
        for ch in line:
            if ord(ch)<ord('0') or ord(ch)>ord('9'):
                board[letter,index]=Piece(ch)
                pieces.get(Piece(ch),[]).append((letter,index))
                letter=addLetter(letter,1)
            else:
                for i in range(int(ch)):
                    temp_letter = addLetter(letter,i)
                    board[temp_letter,index]=Piece(" ") 
                letter = addLetter(letter,int(ch))
        index-=1
    return board, pieces, fen


class ChessState():
    def __init__(self,fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board, self.pieces, fen = get_board(fen)
        turn, castling, enpassant, half_moves, full_moves = fen.split(" ")
        #2. next player to move
        self.to_move = WHITE if turn == "w" else BLACK
    
        #3. castling
        self.castling = {WHITE:['K' in castling, 'Q' in castling],
                        BLACK:['k' in castling, 'q' in castling]}

        #4. enpassant
        if enpassant != '-':
            self.enpassant = (enpassant[0],int(enpassant[1]))
        else:
            self.enpassant = (addLetter('a',-1),-1)

        self.half_move_clock = int(half_moves)
        self.full_move_number = int(full_moves)
    
    def do_move(self,move:Move):
        # update board``
        captured_piece = None
        capture_location = None
        moved_piece = None
        moved_rook = None
        rook_move = None
        king_moved =False
        # check if pawn move
        if self.board[move.src][0] == PAWN:
            """pawn moves"""
            # option 1 - enpassant
            if validLocation(*self.enpassant) and move.dest == self.enpassant:
                capture_location = (self.enpassant[0],5 if self.enpassant[1]==6 else 4)
            # option 2 - move pawn normally
            if move.dest[0] != move.src[0]:# capture move
                capture_location = move.dest if capture_location==None else capture_location
                captured_piece = self.board[capture_location]
            moved_piece = self.board[move.src]
            if abs(move.src[1]-move.dest[1])==2:
                """pawn first move needs to update enpassant"""
                self.enpassant = (move.src[0],(move.src[1]+move.dest[1])//2)
        # check if king move
        elif self.board[move.src][0] == KING:
            """king moves"""
            king_moved = True
            # option 1 - casteling
            if abs(ord(move.src[0]) - ord(move.dest[0]))==2:
                queen_side = ord(move.src[0])>ord(move.dest[0])
                rook_src = ('a' if queen_side else 'h', move.src[1])
                rook_dest = (addLetter(move.dest[0],1 if queen_side else -1),move.dest[1])
                rook_move = Move(rook_src,rook_dest,"")
                moved_rook = self.board[rook_src]
            if self.board[move.dest][0]!=EMPTY:
                capture_location = move.dest
                captured_piece = self.board[capture_location]
            # option 2 - move king normally
            moved_piece = self.board[move.src]
        else:
            """move any other piece normally"""
            if self.board[move.dest][0]!=EMPTY:
                capture_location = move.dest
                captured_piece = self.board[capture_location]
            moved_piece = self.board[move.src]
        
        if self.board[move.src][0] == ROOK:
            """rook move needs to update casteling rights"""
            rook_owner = self.board[move.src][1]
            first_rank = 1 if rook_owner == WHITE else 8
            queen_rook = ('a',first_rank)
            king_rook = ('h',first_rank)
            if move.src == queen_rook and self.castling[rook_owner][QUEEN_CASTLING]:
                self.castling[rook_owner][QUEEN_CASTLING] = False
            elif move.src == king_rook and self.castling[rook_owner][KING_CASTLING]:
                self.castling[rook_owner][KING_CASTLING] = False
        
        # update pieces lists
        if captured_piece is not None:
            self.pieces[captured_piece].remove(capture_location)
        if moved_piece is not None:
            self.pieces[moved_piece].remove(move.src)
            self.pieces[moved_piece].append(move.dest)
        if moved_rook is not None:
            self.pieces[moved_rook].remove(rook_move.src)
            self.pieces[moved_rook].append(rook_move.dest)

        # update casteling
        if king_moved:
            self.castling[self.to_move] = [False,False]

        # update half-turn
        self.half_move_clock +=1

        # update full moves
        self.full_move_number += 1 if self.turn_owner == BLACK else 0

        # update turn owner
        self.to_move = (1-(self.to_move -1))+1



