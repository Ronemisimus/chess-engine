def addLetter(letter:str,num:int):
    return chr(ord(letter)+num)

def letterToNumber(letter:str):
    return ord(letter) - ord('a')

def validLetter(letter:str):
    return ord(letter) in range(ord('a'),ord('i'))

def validNumber(num:int):
    return num>0 and num<9

def validLocation(letter:str,number:int):
    return validLetter(letter) and validNumber(number)


#notation
EMPTY = 0


# types
KING = 1
QUEEN = 2
ROOK = 3
KNIGHT = 4
BISHOP = 5
PAWN = 6


# ownership
WHITE = 1
BLACK = 2


# castling
KING_CASTLING = 0
QUEEN_CASTLING = 1

KNIGHT_MOVE_CHANGES = [
    (1,2),
    (2,1),
    (2,-1),
    (1,-2),
    (-1,-2),
    (-2,-1),
    (-2,1),
    (-1,2)
]


# notation conversion
convertToChars = {
    EMPTY:{
        EMPTY:" "
    },
    WHITE:{
        KING:"K",
        QUEEN:"Q",
        ROOK:"R",
        KNIGHT:"N",
        BISHOP:"B",
        PAWN:"P"
    },
    BLACK:{
        KING:"k",
        QUEEN:"q",
        ROOK:"r",
        KNIGHT:"n",
        BISHOP:"b",
        PAWN:"p"
    }
}


convertToInts = {
    " ":(EMPTY,EMPTY),
    "K":(KING,WHITE),
    "Q":(QUEEN,WHITE),
    "R":(ROOK,WHITE),
    "N":(KNIGHT,WHITE),
    "B":(BISHOP,WHITE),
    "P":(PAWN,WHITE),
    "k":(KING,BLACK),
    "q":(QUEEN,BLACK),
    "r":(ROOK,BLACK),
    "n":(KNIGHT,BLACK),
    "b":(BISHOP,BLACK),
    "p":(PAWN,BLACK)
}
