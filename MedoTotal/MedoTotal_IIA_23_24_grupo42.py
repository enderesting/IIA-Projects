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

    def __init__(self, fear, pac_pos, pill_pos, path):
    # self.fear,self.pacman_pos,self.pill_pos,self.path
        self.fear, self.pacman_pos, self.pill_pos, self.path = fear, pac_pos, pill_pos, path


class MedoTotal(Problem):
    
    def __init__(self, situacaoInicial=mundoStandard):
        infoDetails = Problem.split('\n', 3)
        #params
        self.objective = infoDetails[0]
        # self.fear = infoDetails[1]
        self.power = infoDetails[2]
        #grid
        lines = infoDetails[3].split('\n')[:-1]
        self.grid = [(line.replace(" ", "")) for line in lines]
        #positions
        self.ghost_pos = self.find_symbol(self.grid,'F')[0]
        pacman_pos_ini = self.find_symbol(self.grid,'F')[0]
        pill_pos_ini = self.find_symbol(self.grid,'*')
        #state
        self.initial = EstadoFantasma(infoDetails[1],pacman_pos_ini,pill_pos_ini,{})


    def find_symbol(grid,symbol):
        """
        Returns a list of positions
            grid: 2d array
            symbol: the symbol to find 
        """
        list_of_pos = []
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (symbol == grid[i][j]):
                    list_of_pos.append((j,i))
        return list_of_pos


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
