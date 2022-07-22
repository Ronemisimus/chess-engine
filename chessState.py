from constants import addLetter, WHITE, BLACK
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
    def __init__(self,fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
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
    
    def do_move(move:Move):
        pass


