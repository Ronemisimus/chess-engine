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
                piece_index = Piece(ch)
                board[letter,index]=piece_index
                lst= pieces.get(ch,[])
                lst.append((letter,index))
                pieces[ch]=lst
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

        self.print_lists=False
    
    def do_move(self,move:Move):
        # update board``
        captured_piece = None
        capture_location = None
        moved_piece = None
        moved_rook = None
        rook_move = None
        king_moved =False
        # check if pawn move
        if self.board[move.src].tool == PAWN:
            """pawn moves"""
            # option 1 - enpassant
            if validLocation(*self.enpassant) and move.dest == self.enpassant:
                capture_location = (self.enpassant[0],5 if self.enpassant[1]==6 else 4)
            # option 2 - move pawn normally
            if move.dest[0] != move.src[0]:# capture move
                capture_location = move.dest if capture_location==None else capture_location
                captured_piece = str(self.board[capture_location])
            moved_piece = str(self.board[move.src])
            if abs(move.src[1]-move.dest[1])==2:
                """pawn first move needs to update enpassant"""
                self.enpassant = (move.src[0],(move.src[1]+move.dest[1])//2)
        # check if king move
        elif self.board[move.src].tool == KING:
            """king moves"""
            king_moved = True
            # option 1 - casteling
            if abs(ord(move.src[0]) - ord(move.dest[0]))==2:
                queen_side = ord(move.src[0])>ord(move.dest[0])
                rook_src = ('a' if queen_side else 'h', move.src[1])
                rook_dest = (addLetter(move.dest[0],1 if queen_side else -1),move.dest[1])
                rook_move = Move(rook_src,rook_dest,"")
                moved_rook = str(self.board[rook_src])
            if self.board[move.dest].tool!=EMPTY:
                capture_location = move.dest
                captured_piece = str(self.board[capture_location])
            # option 2 - move king normally
            moved_piece = str(self.board[move.src])
        else:
            """move any other piece normally"""
            if self.board[move.dest].tool!=EMPTY:
                capture_location = move.dest
                captured_piece = str(self.board[capture_location])
            moved_piece = str(self.board[move.src])
        
        if self.board[move.src].tool == ROOK:
            """rook move needs to update casteling rights"""
            rook_owner = self.board[move.src].owner
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
            self.board[capture_location] = Piece(" ")
        if moved_piece is not None:
            self.pieces[moved_piece].remove(move.src)
            self.pieces[moved_piece].append(move.dest)
            self.board[move.src] = Piece(" ")
            self.board[move.dest] = Piece(moved_piece)
        if moved_rook is not None:
            self.pieces[moved_rook].remove(rook_move.src)
            self.pieces[moved_rook].append(rook_move.dest)
            self.board[rook_move.src] = Piece(" ")
            self.board[rook_move.dest] = Piece(moved_rook)
        if self.board[move.dest].tool == PAWN and move.promotion != "":
            self.pieces[moved_piece].remove(move.dest)
            promoted_piece = Piece(move.promotion)
            promoted_piece.owner = self.to_move
            self.board[move.dest] = promoted_piece
            self.pieces[str(promoted_piece)].append(move.dest)

        # update casteling
        if king_moved:
            self.castling[self.to_move] = [False,False]

        # update half-turn
        self.half_move_clock +=1

        # update full moves
        self.full_move_number += 1 if self.to_move == BLACK else 0

        # update turn owner
        self.to_move = (1-(self.to_move -1))+1

    def __str__(self) -> str:
        block_len = 48
        res = "   |  " + "  |  ".join([chr(i) for i in range(ord('A'),ord('I'))]) + "  |\n"
        res += "   " + "-"*block_len+'\n'
        for index in range(8,0,-1):
            res += " " + str(index) + " |"
            for key in self.board.physical_board:
                cell = self.board.physical_board[key][index-1]
                res += ("  " + str(cell)+"  |")
            res += '\n'
            res += "   " + "-"*block_len+'\n'

        if self.print_lists:
            res+= "\n"
            for key in self.pieces:
                res += str(key) + " : "
                for location in self.pieces[key]:
                    res += "("+location[0]+","+str(location[1])+") "
                res += "\n"
        return res


cs = ChessState()

cs.print_lists = True

print(cs)

print("\n\ndoing e2e4\n\n")

cs.do_move(Move(('e',2),('e',4),""))

print(cs)

print("\n\ndoing e7e5\n\n")

cs.do_move(Move(('e',7),('e',5),""))

print(cs)

print("\n\ndoing g1f3\n\n")

cs.do_move(Move(('g',1),('f',3),""))

print(cs)

print("\n\ndoing g8f6\n\n")

cs.do_move(Move(('g',8),('f',6),""))

print(cs)

print("\n\ndoing f1d3\n\n")

cs.do_move(Move(('f',1),('d',3),""))

print(cs)

print("\n\ndoing f8d6\n\n")

cs.do_move(Move(('f',8),('d',6),""))

print(cs)

print("\n\ndoing e1g1\n\n")

cs.do_move(Move(('e',1),('g',1),""))

print(cs)

print("\n\ndoing e8g8\n\n")

cs.do_move(Move(('e',8),('g',8),""))

print(cs)

print("\n\ndoing c2c4\n\n")

cs.do_move(Move(('c',2),('c',4),""))

print(cs)

print("\n\ndoing c7c6\n\n")

cs.do_move(Move(('c',7),('c',6),""))

print(cs)

print("\n\ndoing c4c5\n\n")

cs.do_move(Move(('c',4),('c',5),""))

print(cs)

print("\n\ndoing b7b5\n\n")

cs.do_move(Move(('b',7),('b',5),""))

print(cs)

print("\n\ndoing c5b6\n\n")

cs.do_move(Move(('c',5),('b',6),""))

print(cs)

print("\n\ndoing b8a6\n\n")

cs.do_move(Move(('b',8),('a',6),""))

print(cs)

print("\n\ndoing b6b7\n\n")

cs.do_move(Move(('b',6),('b',7),""))

print(cs)

print("\n\ndoing d8a5\n\n")

cs.do_move(Move(('d',8),('a',5),""))

print(cs)

print("\n\ndoing b7b8q\n\n")

cs.do_move(Move(('b',7),('a',8),"q"))

print(cs)
