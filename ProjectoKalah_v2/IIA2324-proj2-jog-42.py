'''
Pebbles "The Reaper" Snatcher 
     [____]   
     ]()()[                  _________
   ___\__/___               /         \
  |__|    |__|             / ♥ R.I.P ♥ \ 
   |_|_/\_|_|              |           |
   | | __ | |              | Chapiteau |
   |_|[::]|_|              | 2023-2023 |
   \_|_||_|_/              |           |
     |_||_|          ______|___________|______    
    _|_||_| jro
   |___||___| 

Yichen Cao "Mimi" fc58165
Gonçalo Fernandes fc58194
Github repo: https://github.com/enderesting/IIA-Projects
'''

# from jogos import *
# from testing import *
from kalah import KalahState
# from jogos import alphabeta_cutoff_search_new
# class Jogador():
#     def __init__(self, nome, fun):
#         self.nome = nome
#         self.fun = fun
#     def display(self):
#         print(self.nome+" ")
        
# class JogadorAlfaBeta(Jogador):
#     def __init__(self, nome, depth,fun_eval):
#         self.nome = nome
#         self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)


# PebblePlayer = JogadorAlfaBeta("PebbleReaper",2,)

# # O primeiro é o 0 e o segundo é o 1 (para jogos de dois jogadores).
# def linearPond(estado,jogador,pesos,funcoes,win):
#     """Função que pega no estado e no jogador e se fim do jogo devolve win*utilidade (* 1 ou -1, dependendo do jogador)
#     senão devolve a combinação linear de pesos e features."""
#     if estado.is_game_over():
#         aux = estado.result()
#         return aux*win if jogador == 0 else aux*-win
#     # print("pit_total:",pit_total(estado,proxjog))
#     # print("side_total: ", side_total(estado,proxjog))
#     # print("chance_to_clear_right_most:",chance_to_clear_right_most(estado,proxjog))
#     # print("congregate_seeds: ", congregate_seeds(estado,proxjog))
#     return sum([p*f(estado,jogador) for (p,f) in zip(pesos,funcoes)])


# class JogadorLinearPond(JogadorAlfaBeta):
#     """SubClasse dos jogadores alfabeta que usa o combinador linear como função de avaliação.
#     Recebe para além do nome e da profundidade, a lista de pesos e das funções-features, criando fun_eval"""
#     def __init__(self, nome, depth,weights,features,win_value):
#         self.nome = nome
#         fun_eval=lambda estado,jogador: linearPond(estado,jogador,weights,features,win_value)
#         self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)

def func_42(estado,jogador):
    if estado.is_game_over():
        aux = estado.result()
        return aux*100 if jogador == 0 else aux*-100
    
    # # Ideally, we would switch between strategies
    # if random.randrange(0,10) <= 3:
    ###defense strat###
    weights = [0.4132746969431487, 0.004000018652774955, 0.09436108536199529, 0.0566795623905725, 0.029663753065053162, 0.4020208835864555]
    functions = [pit_total_42,side_total_42,chance_to_clear_right_most_42,congregate_seeds_42,capture_available_42,chaining_42]
    # else:
    ###base###
        # weights = [0.51, 0.01, 0.34, 0.1]
        # functions = [pit_total_42,side_total_42,chance_to_clear_right_most_42,congregate_seeds_42]    

    return sum([p*f(estado,jogador) for (p,f) in zip(weights,functions)])


'''
REF: https://www.mdpi.com/2227-9709/7/3/34
ok    H1: Collect as many seeds in one pit as possible. Prioritize Left pits over right pits
ok    H2: Collect as many seeds on the player’s side.
n/a    H3: Reach as many moves as possible to select.
ok    H4: Maximize the number of seeds in the player’s kalaha.
ok    H5: Clear the rightmost pit (i.e., that with number 1).
ok    H6: Minimize the number of seeds in the opponent’s kalaha. Prevent seeds in opposition's kalaha.
'''
# satisfies H4: Maximize the number of seeds in the player’s kalaha.
def pit_total_42(state:KalahState,player):
    player_pit = state.state[6] if player == state.SOUTH else state.state[13]
    opponent_pit = state.state[13] if player == state.SOUTH else state.state[6] 
    return player_pit-opponent_pit

# satisfies H2:  Collect as many seeds on the player’s side.
def side_total_42(state:KalahState,player):
    player_side_total = sum(state.state[:6]) if player == state.SOUTH else sum(state.state[7:13]) 
    opponent_side_total = sum(state.state[7:13]) if player == state.SOUTH else sum(state.state[:6])
    return player_side_total-opponent_side_total

# satsifies H5: Clear the rightmost pit (i.e., that with number 1).
def chance_to_clear_right_most_42(state:KalahState,player):
    north_right_empty = 1 if state.state[12] == 0 else 0
    south_right_empty = 1 if state.state[5] == 0 else 0
    return south_right_empty - north_right_empty if player == state.SOUTH else north_right_empty - south_right_empty

# satsifies H1: Collect as many seeds in one pit as possible
# encourages having more seeds on the pits closer to the left hand side
def congregate_seeds_42(state:KalahState,player):
    weights = {0:1,
               1:0.8,
               2:0.6,
               3:0.4,
               4:0.2}
    
    south_result = 0
    for i in range(5):
        pit_weight = state.state[i]*weights[i]
        if  pit_weight > south_result:
            south_result = pit_weight
    north_result = 0
    for i in range(7,12):
        pit_weight = state.state[i]*weights[i-7]
        if  pit_weight > north_result:
            north_result = pit_weight
    return south_result - north_result if player == state.SOUTH else north_result - south_result


# Not used.
# This supposes a given state isn't played and could have potential captures
def capture_available_42(state:KalahState,player):
    board = state.state

    south_max_capture = 0
    south_empties = [i for i in range(6) if board[i]==0]
    south_move_final_index = [(i+board[i])%14 if i+board[i]<13 else (i+board[i])%13 for i in range(6) if board[i] != 0 and board[i]<=13]
    south_possible_captures = [value for value in south_empties if value in south_move_final_index]

    if len(south_possible_captures) != 0:
        for i in south_possible_captures:
            if 1+board[i+7] > south_max_capture:
                south_max_capture = 1+board[i+7]
    
    north_max_capture = 0
    north_empties = [i for i in range(7,13) if board[i]==0]
    north_move_final_index = [(i+board[i])%14 if i+board[i]-7<13 else ((i+board[i])%14)+1 for i in range(7,13) if board[i] != 0 and board[i]<=13]
    north_possible_captures = [value for value in north_empties if value in north_move_final_index]

    if len(north_possible_captures) != 0:
        for i in north_possible_captures:
            if 1+board[i-7] > north_max_capture:
                north_max_capture = 1+board[i-7]

    return south_max_capture - north_max_capture if player == state.SOUTH else north_max_capture - south_max_capture

# Check if any chaining can be used.
def chaining_42(state:KalahState,player):
    if(state.pass_turn == True):
        return 1
    return 0

# Detect possible captures from oppositions on the next move.
# Heuristics are taken away for every weak link
def capture_defense_42(state:KalahState,player):
    # for every capture blocked, the value is like, the number of seed they dont win
    board = state.state
    
    south_max_capture = 0
    south_empties = [i for i in range(6) if board[i]==0]
    south_move_final_index = [(i+board[i])%14 if i+board[i]<13 else (i+board[i])%13 for i in range(6) if board[i] != 0 and board[i]<=13]
    south_possible_captures = [value for value in south_empties if value in south_move_final_index]

    if len(south_possible_captures) != 0:
        for i in south_possible_captures:
            if 1+board[i+7] > south_max_capture:
                south_max_capture = 1+board[i+7] #figure out the best capture they could do
    
    north_max_capture = 0
    north_empties = [i for i in range(7,13) if board[i]==0]
    north_move_final_index = [(i+board[i])%14 if i+board[i]-7<13 else ((i+board[i])%14)+1 for i in range(7,13) if board[i] != 0 and board[i]<=13]
    north_possible_captures = [value for value in north_empties if value in north_move_final_index]

    if len(north_possible_captures) != 0:
        for i in north_possible_captures:
            if 1+board[i-7] > north_max_capture:
                north_max_capture = 1+board[i-7]

    if player == state.SOUTH:
        return pit_total_42(state,player) - north_max_capture*(-1)
    else:
        return pit_total_42(state,player) - south_max_capture*(-1)