
def toes(state,player):
    board = state.state
    if state.is_game_over():
        result = state.result()
        if result == 0:
            result = 0
        return 100 if result == player else -100
    
    own_seeds = sum(board[:6]) if player == 0 else sum(board[7:13])
    opponent_seeds = sum(board[7:13]) if player == 0 else sum(board[:6])
    score = own_seeds - opponent_seeds
    return score

# toe1 = JogadorAlfaBeta("teehee",6,toes)
# toe2 = JogadorAlfaBeta("heehoo",6,toes)