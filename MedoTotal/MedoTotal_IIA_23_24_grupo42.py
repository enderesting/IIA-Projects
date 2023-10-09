from searchPlus import *
import copy

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

    def __init__(self, objective:int, fear:int, pac_pos:(int,int), pill_pos:[(int,int)], path:{(int,int):int}):
        self.objective, self.fear, self.pacman_pos, self.pill_pos, self.path = objective, fear, pac_pos, pill_pos, path

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, EstadoFantasma):
            return NotImplemented
        result = (self.objective == __value.objective) and (self.fear == __value.fear) and (self.pacman_pos == __value.pacman_pos) 
        result &= (self.pill_pos == __value.pill_pos) and (self.path == __value.path)
        return result

dires = {"N":(0,-1),"W":(-1,0),"E":(1,0),"S":(0,1)}
class MedoTotal(Problem):

    def __init__(self, situacaoInicial=mundoStandard):
        infoDetails = situacaoInicial.split('\n', 3)
        #params
        # self.objective = int((infoDetails[0])[2:])
        # self.fear = infoDetails[1]
        self.power = int((infoDetails[2])[2:])
        #grid
        lines = infoDetails[3].split('\n')[:-1]
        self.grid_len = len(lines)
        self.grid = [(line.replace(" ", "")) for line in lines]
        #positions
        self.ghost_pos = self.find_symbol(self.grid,'F')[0]
        pacman_pos_ini = self.find_symbol(self.grid,'@')[0]
        pill_pos_ini = self.find_symbol(self.grid,'*')
        # display
        self.display_grid = infoDetails[3]
        self.display_grid = self.replace_symbol(pacman_pos_ini,'.')
        for pos in pill_pos_ini:
            self.display_grid = self.replace_symbol(pos,'.')

        #state
        self.initial = EstadoFantasma(int((infoDetails[0])[2:]),int((infoDetails[1])[2:]),pacman_pos_ini,pill_pos_ini,{pacman_pos_ini:1})


    def replace_symbol(self,pos,new_symbol):
        index = pos[1]*(2*self.grid_len)+2*pos[0]
        new_grid = self.display_grid[:index] + new_symbol + self.display_grid[index+1:]
        return new_grid
     
    def find_symbol(self, grid, symbol):
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


    def actions(self, state : EstadoFantasma):
        # directions = {"N":(0,-1),"W":(-1,0),"E":(1,0),"S":(0,1)}
        pacman_x, pacman_y = state.pacman_pos[0], state.pacman_pos[1]
        closest_pellet_distance = self.distance_to_closest_pellet(state)
        num_pill_pos = len(state.pill_pos)

        if state.fear < state.objective and (num_pill_pos == 0 or closest_pellet_distance > state.fear or closest_pellet_distance + num_pill_pos * self.power < state.objective):
            return []

        allowed_actions = [key for key, (x, y) in dires.items() if self.grid[pacman_y + y][pacman_x + x] not in ["=", "F"]]
        return allowed_actions
    
    def distance_to_closest_pellet(self, state : EstadoFantasma):
        pacman_x, pacman_y = state.pacman_pos[0], state.pacman_pos[1]
        if (len(state.pill_pos) == 0):
            return float('inf')
        distances = [abs(pacman_x-x)+abs(pacman_y-y) for (x, y) in state.pill_pos]
        return min(distances)

    def result(self, state : EstadoFantasma, action):
        # objective, fear, pac_pos, pill_pos, path
        res = copy.deepcopy(state)
        res.objective -=1
        res.fear -= 1
        # apply action to pac_pos
        dir = dires[action]
        res.pacman_pos = (res.pacman_pos[0]+dir[0],res.pacman_pos[1]+dir[1])
        # check if it's equal to a pill_pos
        for each_pill in res.pill_pos:
            if each_pill == res.pacman_pos:
                # if yes,remove this from pill_pos list
                res.pill_pos.remove(each_pill)
                # top the fear to P
                res.fear = self.power
                break
        # add new pos to path
        if res.pacman_pos in res.path.values():
            res.path[res.pacman_pos] += 1
        else:
            res.path[res.pacman_pos] = 1
        return res
    
    def goal_test(self, state:EstadoFantasma):
        return state.objective == 0 

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
        self.display_grid = self.replace_symbol(state.pacman_pos,'@')
        for each_pill_pos in state.pill_pos:
            self.display_grid = self.replace_symbol(each_pill_pos,'*')
        return self.display_grid
