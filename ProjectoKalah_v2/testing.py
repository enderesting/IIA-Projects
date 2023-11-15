# from kalah import *
from pebblereaper import *
from tqdm import tqdm

for i in tqdm(range(10000)):
    pass

class Jogador():
    def __init__(self, nome, fun):
        self.nome = nome
        self.fun = fun
    def display(self):
        print(self.nome+" ")
        
class JogadorAlfaBeta(Jogador):
    def __init__(self, nome, depth,fun_eval):
        self.nome = nome
        self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)

#to pitch two bad bitches together
def joga11(game, jog1, jog2,verbose=False):
    ### jog1 e jog2 são jogadores com funções que dado um estado do jogo devolvem a jogada que escolheram
    ### devolve o par de jogadores, a lista de jogadas e o resultado
    estado=game.initial
    proxjog = jog1
    lista_jogadas=[]
    lance = 0
    while not game.terminal_test(estado):
        if verbose:
            print('----------   LANCE:',lance)
            game.display(estado)
        jogada = proxjog.fun(game, estado)
        if verbose:
            print('JOGADA=',jogada)
        estado=game.result(estado,jogada)
        lista_jogadas.append(jogada)
        proxjog = jog2 if proxjog == jog1 else jog1
        lance+=1
    #p jogou e ganhou
    util=game.utility(estado,0)
    if util == 1:
        resultado=jog1.nome
    elif util== -1:
        resultado = jog2.nome
    else:
        resultado='Empate'
    return ((jog1.nome,jog2.nome),lista_jogadas,resultado)

###CHAPITEAU###
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

toe1 = JogadorAlfaBeta("chapiteau",6,toes)
# toe2 = JogadorAlfaBeta("heehoo",6,toes)

###RANDOM###
def f_caos_intel(estado,jogador):
    """Quando é terminal: +100 para vitória, -100 para a derrota e 0 para o empate.
       Quando o tabuleiro é não terminal devolve 0, o que quer dizer que como o minimax baralha as acções, será random"""
    if estado.is_game_over():
        aux = estado.result()
        return aux*100 if jogador == estado.SOUTH else aux*-100
    return 0

el_caos_int6=JogadorAlfaBeta("El Caos Inteligente 6",6,f_caos_intel)

###PEBBLES###
pebs = JogadorAlfaBeta('Pebbles',6,Jogador_42)

###N_MATCHING###
scores={'Vitoria': 3, 'Empate': 1}

def traduzPontos(tabela):
    tabelaScore={}
    empates=tabela['Empate']
    for x in tabela:
        if x != 'Empate':
            tabelaScore[x]=scores['Vitoria']*tabela[x]+empates
    return tabelaScore

def jogaNpares(jogo,n,jog1,jog2):
    tabelaPrim={jog1.nome:0, jog2.nome:0, 'Empate':0}
    tabelaSeg={jog1.nome:0, jog2.nome:0, 'Empate':0}
    tabela={}
    for _ in range(n):
        _,_,vencedor=joga11(jogo,jog1,jog2)
        tabelaPrim[vencedor]+=1
        _,_,vencedor=joga11(jogo,jog2,jog1)
        tabelaSeg[vencedor]+=1
    for x in tabelaPrim:
        tabela[x]=tabelaPrim[x]+tabelaSeg[x]
    return tabelaPrim,tabelaSeg,tabela,traduzPontos(tabela)

# jogaNpares()

jogo=Kalah(10)
#n jogaNpares(jogo,300,el_caos,el_caos_int6)
# jogo.result()

# _,_,res=joga11(jogo,toe1,pebs,True)
jogaNpares(jogo,30,toe1,pebs)