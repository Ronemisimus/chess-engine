import constants

class Piece():
    def __init__(self,sign:str):
        piece, owner = constants.convertToInts(sign)
        self.tool = piece
        self.owner = owner
        

class Board():
    def __init__(self):
        self.physical_board={
            'a':[8*Piece(" ")],
            'b':[8*Piece(" ")],
            'c':[8*Piece(" ")],
            'e':[8*Piece(" ")],
            'f':[8*Piece(" ")],
            'g':[8*Piece(" ")],
            'h':[8*Piece(" ")]
        }

    def __setitem__(self, key:tuple, value:Piece):
        letter, index = key
        self.physical_board[letter][index-1] = value
    
    def __getitem__(self,key:tuple):
        letter, index = key
        return self.physical_board[letter][index-1]

class Move():
    def __init__(self,src:tuple,dest:tuple,promotion:str):
        self.src = src
        self.dest = dest
        self.promotion = promotion