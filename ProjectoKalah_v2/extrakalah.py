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
    return sum([p*f(estado,jogador) for (p,f) in zip(pesos,funcoes)])


class JogadorLinearPond(JogadorAlfaBeta):
    """SubClasse dos jogadores alfabeta que usa o combinador linear como função de avaliação.
    Recebe para além do nome e da profundidade, a lista de pesos e das funções-features, criando fun_eval"""
    def __init__(self, nome, depth,weights,features,win_value):
        self.nome = nome
        fun_eval=lambda estado,jogador: linearPond(estado,jogador,weights,features,win_value)
        self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)

# se tivermos:

def fi(estado,jogador):
    pass  # a definir

def f2(estado,jogador):
    pass  # a definir

# Supondo f1 e f2 já desenvolvidas, podemos criar um jogador que usa alfabeta, à profundidade 5 por exemplo, 
# com a combinação linear 0.1*f1+0.9*f2, e +100000 na vitória, assim:

# j_10f1_90f2_5=JogadorLinearPond('10f1_90f2_depth1',5,[0.1,0.9],[f1,f2],100)

# Os pesos não têm que estar normalizados, especialmente se tiverem funções (fis) com outputs em diferentes escalas 
# Será fácil até criarem um torneio automaticamente para um conjunto de jogadores com diferentes pesos de modo a seleccionarem os melhores
# pesos para várias funções fis ...