
from collections import namedtuple
from searchPlus import *
from MedoTotal import MedoTotal
import timeit    # Para tirar
import queue

parametros="T=26\nM=6\nP=10"
linha1= "= = = = = = = = = =\n"
linha2= "= @ . * . . * . . =\n"
linha3= "= . = = = = = = . =\n"
linha4= "= . = F . . . . . =\n"
linha5= "= . = . . . . . . =\n"
linha6= "= . = . . . . . . =\n"
linha7= "= . = . . . . . . =\n"
linha8= "= * . . . . . . . =\n"
linha9= "= . . . . . . . . =\n"
linha10="= = = = = = = = = =\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9+linha10
mundoStandard=parametros + "\n" + grelha

# A subclasse de Problem: MedoTotal
#
class MedoTotalTurbo(MedoTotal):
    """Encontrar um caminho numa grelha 2D com obstáculos. Os obstáculos são células (x, y)."""
    def __init__(self, texto_input=mundoStandard):
        super().__init__(texto_input)
        self.pellet_map={}


    # breadth search for the closest pill
    def find_closest_pill(self,state):
        # if npellet is the same as the last u checked
        # check a dictionary {(x,y):npellet,dist_to_pellet}
        if(state.pacman in self.pellet_map.keys() and\
           len(state.pastilhas) == self.pellet_map[state.pacman][0]):
            return self.pellet_map[state.pacman][1]

        frontier = queue.Queue()
        frontier.put(state.pacman)
        came_from = {}
        came_from[state.pacman] = None

        while not frontier.empty():
            current_node = frontier.get()

            # if a pill is found!
            if current_node in state.pastilhas:
                count = 0
                while came_from[current_node] is not None :
                    current_node = came_from[current_node] # if we're not back at the start, go back a step
                    count+=1
                self.pellet_map[state.pacman] = (len(state.pastilhas),count)
                return count # figure out the path length and return
            
            #for all neighbors of the current
            for each_neighbor in list(map(lambda d: (current_node[0]+d[0], current_node[1]+d[1]), self.directions.values())):
                    if each_neighbor not in (self.obstacles | {self.fantasma}) and\
                        each_neighbor not in came_from: #every node that was visited gets added to the dict 
                        #NoTE TO SELF!!!: check obstacle before proceeding
                        came_from[each_neighbor] = current_node # pointing where each neighbor came from to the current node
                        frontier.put(each_neighbor)
        return 0
    
    def actions(self, state):
        x, y = state.pacman
        if self.falha_antecipada(state): return []
        else:
            return [act for act in self.directions.keys() 
                if (x+self.directions[act][0],y+self.directions[act][1]) not in (self.obstacles | {self.fantasma}) and 
                not self.falha_antecipada(self.result(state,act))]

    # situações de falha antecipada
    #
    def falha_antecipada(self,state):
        if state.tempo <= state.medo:
            return False
        if state.pastilhas == set(): # se não há mais pastilhas e eram necessárias
            return True
        minDist = self.find_closest_pill(state)
        if minDist > state.medo: # se não há tempo (manhatan) para chegar à próxima super-pastilha
            return True
        if (state.medo + self.poder * len(state.pastilhas)) < state.tempo:
            # se o poder de todas as pastilhas mais o medo são insuficientes.
            return True
        return False

def depth_first_tree_search_all_count(problem,optimal=False,verbose=False):

    #if optimal, skip outta loop if cost is higher
    """
    class Node(
    state: Any,
    parent: Any | None = None,
    action: Any | None = None,
    path_cost: int = 0
    )

    resultado,max_mem,visitados,finais = depth_first_tree_search_all_count(gx)
    - result state
    - max_mem?
    - number of visited nodes
    - number of branches that reached goal state
    """
    frontier=Stack()
    visited=0
    finais=0
    best=None # define somewhere else
    max_mem=0
    c=0
    # based on tree_search(problem, frontier) from searchPlus.py
    frontier.append(Node(problem.initial))
    while frontier:
        node = frontier.pop()
        if optimal and best and node.path_cost >= best.path_cost:
            continue
        visited+=1
        if problem.goal_test(node.state):
            finais+=1 # return node
            if best is None or best.path_cost > node.path_cost:
               best = node
        else:
            expansion = reversed(node.expand(problem))
            if optimal and best:
                expansion = [each_node for each_node in expansion if each_node.path_cost < best.path_cost]
            frontier.extend(expansion)
            if frontier.__len__() > max_mem:
                max_mem = frontier.__len__()

        if verbose:
            print("---------------------\n\n" + problem.display(node.state))

            print("Custo: " + str(node.path_cost))
    return (best,max_mem,visited,finais)