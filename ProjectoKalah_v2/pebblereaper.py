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
    res = 1*pit_total(state,player)+side_total(state,player)+chance_to_clear_right_most(state,player)
    return res

'''
    H1: Collect as many seeds in one pit as possible. 
ok    H2: Collect as many seeds on the player’s side.
    H3: Reach as many moves as possible to select.
ok    H4: Maximize the number of seeds in the player’s kalaha.
ok    H5: Clear the rightmost pit (i.e., that with number 1).
?    H6: Minimize the number of seeds in the opponent’s kalaha.
'''
# satisfies H4: Maximize the number of seeds in the player’s kalaha.
def pit_total(state:KalahState,player):
    player_pit = state.state[6] if player == state.SOUTH else state.state[13]
    opponent_pit = state.state[13] if player == state.SOUTH else state.state[6] 
    return player_pit-opponent_pit # biggest pit increase?

# satisfies H2:  Collect as many seeds on the player’s side.
def side_total(state:KalahState,player):
    player_side_total = sum(state.state[:6]) if player == state.SOUTH else sum(state.state[7:13]) 
    opponent_side_total = sum(state.state[7:13]) if player == state.SOUTH else sum(state.state[:6])
    return player_side_total-opponent_side_total # biggest pit increase?

# satsifies H5: Clear the rightmost pit (i.e., that with number 1).
def chance_to_clear_right_most(state:KalahState,player):
    score_pit = state.SOUTH_SCORE_PIT if state.to_move == state.SOUTH else state.NORTH_SCORE_PIT
    if state.state[score_pit-1] == 0:
        return 1
    # for i in range(score_pit - state.PLAY_PITS, score_pit):
    #     pass
    return 0


def get_captured(state:KalahState,player):
    #the mroe captures someone get the more seed they have in their pit. so just compare their pit will do
    score_pit = state.SOUTH_SCORE_PIT if state.to_move == state.SOUTH else state.NORTH_SCORE_PIT
    # enemy_score_pit = state.SOUTH_SCORE_PIT if state.to_move == state.NORTH else state.NORTH_SCORE_PIT
    # 
    pass

# if there's an empty spot in the opposition and we can cover,
def capture_defense(state:KalahState,player):
    # for every capture blocked, the value is like, the number of seed they dont win
    pass

'''
point distribution
    calculating chains - n of seeds that you can get in this chain
    capture - number of seeds you can capture
    disrupting others chain - n of seeds you can prevent from losing
    prevent capture (note for opposite empty) - n of seeds you can prevent from losing
    base case calculation - number of stone captured (normall 0-1)
'''