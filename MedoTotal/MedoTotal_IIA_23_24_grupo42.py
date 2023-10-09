"""
Yichen Cao "Mimi" fc58165
Gonçalo Fernandes fc58194
Github repo: https://github.com/enderesting/IIA-Projects
"""
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

    def __init__(self, objective, fear, pac_pos, pill_pos, path):
        """
        Initiates EstadoFantasma, which is the state object that carries all
        changing states within the MedoTotal problem.
            objective:int - counts down to success
            fear:int - counts down to failure
            pac_pos:(int,int) - position of pacman
            pill_pos:[(int,int)] - list of positions of pills
            path:{(int,int):int} - counts pacman position and its frequency
        """
        self.objective, self.fear, self.pacman_pos, self.pill_pos, self.path = objective, fear, pac_pos, pill_pos, path

    def __eq__(self, __value: object) -> bool:
        """
        Check if two states are equal or not.
            __value:object - the other state to compare
        """
        if not isinstance(__value, EstadoFantasma):
            return NotImplemented
        result = (self.objective == __value.objective) and (self.fear == __value.fear) and (self.pacman_pos == __value.pacman_pos) 
        result &= (self.pill_pos == __value.pill_pos) and (self.path == __value.path)
        return result

dires = {"N":(0,-1),"W":(-1,0),"E":(1,0),"S":(0,1)}
class MedoTotal(Problem):

    def __init__(self, situacaoInicial=mundoStandard):
        """
        Initiates MedoTotal problem.
            situacaoInicial:String - String including params and grid. If empty, use mundoStandard
        """
        infoDetails = situacaoInicial.split('\n', 3)
        #params
        self.power = int((infoDetails[2])[2:])
        #grid
        lines = infoDetails[3].split('\n')[:-1]
        self.grid_len = len(lines)
        self.grid = [(line.replace(" ", "")) for line in lines]
        #positions
        self.ghost_pos = self.find_symbol(self.grid,'F')[0]
        pacman_pos_ini = self.find_symbol(self.grid,'@')[0]
        pill_pos_ini = self.find_symbol(self.grid,'*')
        #display
        self.display_grid = infoDetails[3]
        self.display_grid = self.replace_symbol(pacman_pos_ini,'.')
        for pos in pill_pos_ini:
            self.display_grid = self.replace_symbol(pos,'.')
        #state
        self.initial = EstadoFantasma(int((infoDetails[0])[2:]),int((infoDetails[1])[2:]),pacman_pos_ini,pill_pos_ini,{pacman_pos_ini:1})


    def replace_symbol(self,pos,new_symbol):
        """
        Replaces a position in the display grid with a different symbol
            pos:(int,int) - the position tuple to change
            new_Symbol:char - the symbol to change to
        """
        index = pos[1]*(2*self.grid_len)+2*pos[0]
        new_grid = self.display_grid[:index] + new_symbol + self.display_grid[index+1:]
        return new_grid
     
    def find_symbol(self, grid, symbol):
        """
        Returns a list of positions of a symbol that exists in a grid.
            grid: 2d array (not display grid)
            symbol: the symbol to find 
        """
        list_of_pos = []
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (symbol == grid[i][j]):
                    list_of_pos.append((j,i))
        return list_of_pos


    def actions(self, state : EstadoFantasma):
        """
        Return the actions that is possible to be executed in the given state.
        In this case, a list of directions that is possible to go ('N','W','E','S')
            state:EstadoFantasma - the state to search actions for
        """
        pacman_x, pacman_y = state.pacman_pos[0], state.pacman_pos[1]
        closest_pellet_distance = self.distance_to_closest_pellet(state)
        num_pill_pos = len(state.pill_pos)

        if state.fear < state.objective and (num_pill_pos == 0 or closest_pellet_distance > state.fear or closest_pellet_distance + num_pill_pos * self.power < state.objective):
            return []

        allowed_actions = [key for key, (x, y) in dires.items() if self.grid[pacman_y + y][pacman_x + x] not in ["=", "F"]]
        return allowed_actions
    
    def distance_to_closest_pellet(self, state : EstadoFantasma):
        """
        Find the Manhattan Distance from pacman's current position to the closest pill.
            state:EstadoFantasma - the state to search closest pellets/pill for
        """
        pacman_x, pacman_y = state.pacman_pos[0], state.pacman_pos[1]
        if (len(state.pill_pos) == 0):
            return float('inf')
        distances = [abs(pacman_x-x)+abs(pacman_y-y) for (x, y) in state.pill_pos]
        return min(distances)

    def result(self, state : EstadoFantasma, action):
        """
        Allow an action to be performed to a copy of the state given.
            state:EstadoFantasma - the state to perform action on
            action - The step to take
        """
        res = copy.deepcopy(state)
        res.objective -=1
        res.fear -= 1
        # apply action to pac_pos
        dir = dires[action]
        res.pacman_pos = (res.pacman_pos[0]+dir[0],res.pacman_pos[1]+dir[1])
        # check for pill_pos
        for each_pill in res.pill_pos:
            if each_pill == res.pacman_pos:
                res.pill_pos.remove(each_pill)
                res.fear = self.power
                break
        # add new pos to path
        if res.pacman_pos in res.path.keys():
            res.path[res.pacman_pos] += 1
        else:
            res.path[res.pacman_pos] = 1
        return res
    
    def goal_test(self, state:EstadoFantasma):
        """
        Checks if the goal is reached.
            state:EstadoFantasma - the state to check for
        """
        return state.objective == 0 

    def path_cost(self, c, state1, action, state2):
        """
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1.
        c - cost
        state1 - state to act upon
        action - duh
        state2 - state resulted from action
        """
        custo = 0
        for cost in state2.path.values():
            custo += self.node_cost_calculation(cost)
        return custo-1

    def node_cost_calculation(self, times_visited):
        """
        Given time visited, calculate the total cost for visiting this node.
        """
        cost = 0
        if times_visited == 1:
            cost = 1
        else:
            cost = self.node_cost_calculation(times_visited-1) + times_visited
        return cost


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
        """
        Returns a grid that is pretty printed according to the given state.
        """
        self.display_grid = self.replace_symbol(state.pacman_pos,'@')
        for each_pill_pos in state.pill_pos:
            self.display_grid = self.replace_symbol(each_pill_pos,'*')
        return self.display_grid
