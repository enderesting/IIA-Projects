from searchPlus import *

parametros = "T=26\nM=6\nP=10"
linha1 = "= = = = = = = = = =\n"
linha2 = "= @ . * . . * . . =\n"
linha3 = "= . = = = = = = . =\n"
linha4 = "= . = F . . . . . =\n"
linha5 = "= . = . . . . . . =\n"
linha6 = "= . = . . . . . . =\n"
linha7 = "= . = . . . . . . =\n"
linha8 = "= * . . . . . . . =\n"
linha9 = "= . . . . . . . . =\n"
linha10 = "= = = = = = = = = =\n"
grelha = linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9+linha10
mundoStandard = parametros + "\n" + grelha


class EstadoFantasma:

    def __init__(self, info):
        infoDetails = info.split("\n", 3)
        self.objective = infoDetails[0]
        self.fear = infoDetails[1]
        self.power = infoDetails[2]
        self.map = infoDetails[3]


class MedoTotal(Problem):

    def __init__(self, situacaoInicial=mundoStandard):
        self.initial

    def actions(self, state):
        pass

    def result(self, state, action):
        pass

    def path_cost(self, c, state1, action, next_state):
        pass

    def executa(p, estado, accoes, verbose=False):
        """Executa uma sequência de acções a partir do estado devolvendo o triplo formado pelo estado, 
        pelo custo acumulado e pelo booleano que indica se o objectivo foi ou não atingido. Se o objectivo for atingido
        antes da sequência ser atingida, devolve-se o estado e o custo corrente.
        Há o modo verboso e o não verboso, por defeito."""
        custo = 0
        for a in accoes:
            seg = p.result(estado, a)
            custo = p.path_cost(custo, estado, a, seg)
            estado = seg
            objectivo = p.goal_test(estado)
            if verbose:
                p.display(estado)
                print('Custo Total:', custo)
                print('Atingido o objectivo?', objectivo)
            if objectivo:
                break
        return (estado, custo, objectivo)

    def display(self, state: EstadoFantasma):
        """Devolve a grelha em modo txt"""
        return state.map
