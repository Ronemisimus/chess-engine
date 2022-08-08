from chessState import ChessState 
import numpy as np

from constants import BLACK, WHITE

def utility(state:ChessState,final_flag,player):
    copy_state = state.copy()
    if final_flag:
        return -100 * copy_state.winner()
    else:
        my_actions = len(copy_state.actions())
        copy_state.to_move = WHITE if copy_state.to_move==BLACK else BLACK
        enemy_actions = len(copy_state.actions())
        return (my_actions-enemy_actions)*(-1 if player == WHITE else 1)
        


def alpha_beta_cutoff(state:ChessState,d=2,cutoff_test=None,eval_fn=None):
    player = state.to_move
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d))
    eval_fn = eval_fn or (lambda state: utility(state,state.final_state(), player))
    
    # Functions used by alpha_beta
    def max_value(state:ChessState, alpha, beta,depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in state.actions():
            copy_state = state.copy()
            copy_state.do_move(a)
            v = max(v, min_value(copy_state, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state:ChessState, alpha, beta,depth):
        if cutoff_test(state, depth):
                return eval_fn(state)
        v = np.inf
        for a in state.actions():
            copy_state = state.copy()
            copy_state.do_move(a)
            v = min(v, max_value(copy_state, alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in state.actions():
        copy_state = state.copy()
        copy_state.do_move(a)
        v = min_value(copy_state, best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action
