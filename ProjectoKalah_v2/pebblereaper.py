'''
Pebbles "The Reaper" Snatcher 
     [____]   
     ]()()[   
   ___\__/___ 
  |__|    |__|
   |_|_/\_|_| 
   | | __ | | 
   |_|[::]|_| 
   \_|_||_|_/ 
     |_||_| 
    _|_||_| jro
   |___||___| 
'''
from kalah import *
from fairKalahs import *
from jogos import *
from utils import *

def Jogador_42(state:KalahState,player):
    res = 1*pit_total(state,player)+1*chance_to_clear_right_most(state,player)
    return res

    
def pit_total(state:KalahState,player):
    # opponent_pit = state.board[6] if player == state.SOUTH else state.board[13]
    player_pit = state.state[13] if player == state.SOUTH else state.state[6] 
    return player_pit # biggest pit increase?

def chance_to_clear_right_most(state:KalahState,player):
    score_pit = state.SOUTH_SCORE_PIT if state.to_move == state.SOUTH else state.NORTH_SCORE_PIT
    if score_pit-1 == 1:
        return 10
    # for i in range(score_pit - state.PLAY_PITS, score_pit):
    #     pass
    return 0

def enemy_pit_total(state:KalahState,player):
    enemy_score_pit = state.SOUTH_SCORE_PIT if state.to_move == state.NORTH else state.NORTH_SCORE_PIT
    
    pass

'''
point distribution
    calculating chains - n of seeds that you can get in this chain
    capture - number of seeds you can capture
    disrupting others chain - n of seeds you can prevent from losing
    prevent capture (note for opposite empty) - n of seeds you can prevent from losing
    base case calculation - number of stone captured (normall 0-1)
'''