from chessState import ChessState
from board import Move
from search_ai import alpha_beta_cutoff

search_depth = 4

def alpha_beta_player(state:ChessState):
    return alpha_beta_cutoff(state)


def query_player(state:ChessState):
    move = Move.read_move()
    moves = state.actions()
    while move not in moves:
        move = Move.read_move()
    return move    

def play_game(white_player, black_player):
    game = ChessState()
    players = [white_player,black_player]
    index = 0
    while not game.final_state():
        print(game)
        move = players[index](game)
        index = 1-index
        game.do_move(move)
    print(game.winner())


def main():
    play_game(query_player,alpha_beta_player)

if __name__ == "__main__":
    main()