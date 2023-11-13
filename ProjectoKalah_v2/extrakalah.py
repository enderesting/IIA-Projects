from jogos import *
from testing import *
# Eis a definição da classe dos jogadores alfabeta que executam uma combinação linear de características do jogo nos casos não terminais 
# e devolve +valor_vitoria no caso de ganhar, -valor_vitoria no caso de perder e 0 no caso de empate.

# Cada característica fi é uma função fi(estado,jogador) e devolve um valor numérico

# 	p1*f1(estado,jogador)+p2*f2(estado,jogador)...+pn*fn(estado,jogador)




# O primeiro é o 0 e o segundo é o 1 (para jogos de dois jogadores).
def linearPond(estado,jogador,pesos,funcoes,win):
    """Função que pega no estado e no jogador e se fim do jogo devolve win*utilidade (* 1 ou -1, dependendo do jogador)
    senão devolve a combinação linear de pesos e features."""
    if estado.is_game_over():
        aux = estado.result()
        return aux*win if jogador == 0 else aux*-win
    # print("pit_total:",pit_total(estado,proxjog))
    # print("side_total: ", side_total(estado,proxjog))
    # print("chance_to_clear_right_most:",chance_to_clear_right_most(estado,proxjog))
    # print("congregate_seeds: ", congregate_seeds(estado,proxjog))
    return sum([p*f(estado,jogador) for (p,f) in zip(pesos,funcoes)])


class JogadorLinearPond(JogadorAlfaBeta):
    """SubClasse dos jogadores alfabeta que usa o combinador linear como função de avaliação.
    Recebe para além do nome e da profundidade, a lista de pesos e das funções-features, criando fun_eval"""
    def __init__(self, nome, depth,weights,features,win_value):
        self.nome = nome
        fun_eval=lambda estado,jogador: linearPond(estado,jogador,weights,features,win_value)
        self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)

'''
ok    H1: Collect as many seeds in one pit as possible. 
ok    H2: Collect as many seeds on the player’s side.
n/a    H3: Reach as many moves as possible to select.
ok    H4: Maximize the number of seeds in the player’s kalaha.
ok    H5: Clear the rightmost pit (i.e., that with number 1).
wip    H6: Minimize the number of seeds in the opponent’s kalaha.
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
    north_right_empty = 1 if state.state[12] == 0 else 0
    south_right_empty = 1 if state.state[5] == 0 else 0
    return south_right_empty - north_right_empty if player == state.SOUTH else north_right_empty - south_right_empty

# satsifies H1: Collect as many seeds in one pit as possible
# encourages having more seeds on the pits closer to the left hand side
def congregate_seeds(state:KalahState,player):
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

# def capture_available(state:KalahState,player):
#     board = state.state
#     if player == state.SOUTH:
#         empties = [i for i in range(6) if board[i]==0]
#         move_final_index = [i+board[i] if i+board[i]<13 else 13%i+board[i] for i in range(6)]
#         possible_captures = [value for value in empties if value in move_final_index]

#         if len(possible_captures) == 0:
#             return 0
#         else:
#             max_capture = 0
#             for i in possible_captures:
#                 if 1+board[i+7] > max_capture:
#                     max_capture = 1+board[i+7]
#             return max_capture
#     else:
#         empties = [i for i in range(7,13) if board[i]==0]
#         move_final_index = [i+board[i] if i+board[i]-7<13 else 13%i+board[i] for i in range(7,13)]
#         possible_captures = [value for value in empties if value in move_final_index]

#         if len(possible_captures) == 0:
#             return 0
#         else:
#             max_capture = 0
#             for i in possible_captures:
#                 if 1+board[i-7] > max_capture:
#                     max_capture = 1+board[i-7]
#             return max_capture

# detect possible captures from oppositions
# heuristics are taken away for every weak link
def capture_defense(state:KalahState,player):
    # for every capture blocked, the value is like, the number of seed they dont win
    board = state.state
    
    south_max_capture = 0
    south_empties = [i for i in range(6) if board[i]==0]
    south_move_final_index = [i+board[i] if i+board[i]<13 else (i+board[i])%13 for i in range(6)]
    south_possible_captures = [value for value in south_empties if value in south_move_final_index]

    if len(south_possible_captures) != 0:
        for i in south_possible_captures:
            if 1+board[i+7] > south_max_capture:
                south_max_capture = 1+board[i+7] #figure out the best capture you could do
    
    north_max_capture = 0
    north_empties = [i for i in range(7,13) if board[i]==0]
    north_move_final_index = [i+board[i] if i+board[i]-7<13 else (i+board[i])%13 for i in range(7,13)]
    north_possible_captures = [value for value in north_empties if value in north_move_final_index]

    if len(north_possible_captures) != 0:
        for i in north_possible_captures:
            if 1+board[i-7] > north_max_capture:
                north_max_capture = 1+board[i-7]

    if player == state.SOUTH:
        return pit_total(state,player) - north_max_capture*(-1) # or north_max_capture?
    else:
        return pit_total(state,player) - south_max_capture*(-1)

    # return south_max_capture - north_max_capture if player == state.SOUTH else north_max_capture - south_max_capture

    # pass

# return a 32 bit hash, 5 bit
def hash(state:KalahState):
    pass
# Supondo f1 e f2 já desenvolvidas, podemos criar um jogador que usa alfabeta, à profundidade 5 por exemplo, 
# com a combinação linear 0.1*f1+0.9*f2, e +100000 na vitória, assim:

# j_10f1_90f2_5=JogadorLinearPond('10f1_90f2_depth1',5,[0.1,0.9],[f1,f2],100)

# Os pesos não têm que estar normalizados, especialmente se tiverem funções (fis) com outputs em diferentes escalas 
# Será fácil até criarem um torneio automaticamente para um conjunto de jogadores com diferentes pesos de modo a seleccionarem os melhores
# pesos para várias funções fis ...