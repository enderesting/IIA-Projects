"""
Yichen Cao "Mimi" fc58165
Gonçalo Fernandes fc58194
Github repo: https://github.com/enderesting/IIA-Projects
"""
from collections import namedtuple
from searchPlus import *
from MedoTotal import *
from GrafoAbstracto import *
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

"""
Problema 1
"""
class MedoTotalTurbo(MedoTotal):
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
                #calculate path + update count
                while came_from[current_node] is not None:
                    current_node = came_from[current_node]
                    count+=1
                self.pellet_map[state.pacman] = (len(state.pastilhas),count)
                return count 
            
            #find all neighbors of the current node...
            for each_neighbor in list(map(lambda d: (current_node[0]+d[0], current_node[1]+d[1]), self.directions.values())):
                    #every node that is visited now gets added to the dict 
                    if each_neighbor not in (self.obstacles | {self.fantasma}) and\
                        each_neighbor not in came_from:
                        # pointing where each neighbor came from to the current node
                        came_from[each_neighbor] = current_node
                        frontier.put(each_neighbor)
        return 0
    
    # slightly different implementation of fail check that uses the find_closest_pill function
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

"""
Problema 2
"""
# DFS that returns best score, max length of the stack, number of visited nodes, and number of goals
# in a 4-tuple.
def depth_first_tree_search_all_count(problem,optimal=False,verbose=False):
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
        visited += 1
        if verbose: pretty_print(problem,node)
        expansion = []
        for new_node in node.expand(problem):
            if not optimal or (best is None or new_node.path_cost < best.path_cost):
                is_goal, is_best = problem.goal_test(new_node.state), (best is None or new_node.path_cost < best.path_cost)
                if is_goal:
                    finais += 1
                    if best is None or is_best:
                        best = new_node
                    visited += 1
                    if verbose: pretty_print(problem,new_node,is_goal,is_best)
                else:
                    expansion.append(new_node)
        frontier.extend(reversed(expansion))
        if frontier.__len__() > max_mem:
            max_mem = frontier.__len__()
    return (best,max_mem,visited,finais)

def pretty_print(problem,node,is_goal=False,is_best=False):
    print("---------------------\n\n" + problem.display(node.state))
    if is_goal:
        print("GGGGooooooallllll --------- com o custo: " + str(node.path_cost))
        if is_best:
            print("Di best goal até agora")
    else:
        print("Custo: " + str(node.path_cost))


"""
Problema 3
"""
# IDA* graph search that returns the winning state along with
# the number of visited nodes.
def ida_star_graph_search_count(problem,f,verbose=False):
    
    def heuristic(node):
        if isinstance(problem, MedoTotal):
            return problem.minimal_h(node)
        else:
            return problem.h1(node)
    
    initial = Node(problem.initial)
    frontier = Stack()
    visited = 0
    threshold = f(initial)
    
    if verbose:
        print(f"------Cutoff at {threshold}")
    
    while True:
        frontier.append(initial)
        pruned_nodes = set()
        visited_nodes = set()
        while frontier:
            node = frontier.pop()
            visited_nodes.add(node)
            visited += 1
            node_f = f(node)
            
            if verbose:
                print(f"\n{node.state}")
                print(f"Cost: {node_f - heuristic(node)} f= {node_f}")
                
            if node_f > threshold:
                pruned_nodes.add(node_f)
                if verbose:
                    print(f"Out of cutoff -- minimum out: {node_f}")
            elif problem.goal_test(node.state):
                visited += len(frontier)
                if verbose:
                    print("Goal found within cutoff!")
                return (node, visited)
            else:
                for new_node in reversed(node.expand(problem)):
                    if new_node not in frontier and new_node not in visited_nodes:
                        frontier.append(new_node)
        if len(pruned_nodes) == 0:
            break
        threshold = min(pruned_nodes)
        if verbose:
            print(f"\n\n------Cutoff at {threshold}")
    return (None, visited)