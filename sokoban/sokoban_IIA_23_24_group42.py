from planningPlus import *
from logic import *
from utils import *
from search import * 

# receives a text input of the grid, and returns a ForwardPlan with initial state, objectives, and expanded actions
def sokoban(grid):

    problem = PlanningProblem(initial=estado, goals=goals, actions=[], domain=[])
    problem.expand_actions = [] #idk if im understanding this correct. 

    def estado():
        pass

    def goals():
        pass

    return ForwardPlan(problem)

# is a subclass of Problem??? either way, it should have the same attrib. of Problem
# so it can be passed to search.py for solving
class ForwardPlan(Problem):
    def __init__(self,initial:PlanningProblem):
        initial.expand_actions = self.generate_actions(self)
        Problem.__init__(initial) # initial being "problem" defined in sokoban(grid)
        # "generate all actions and store it in expanded_actions"?????
    
    def generate_actions(self):
        self.actions = [] #?? generate it here?? HOW DO I ""STORE IN THE EXPANDED_ACTIONS"" ATTRIBUTE




# test 1
linha1= "##########\n"
linha2= "#........#\n"
linha3= "#..$..+..#\n"
linha4= "#........#\n"
linha5= "##########\n"
grelha=linha1+linha2+linha3+linha4+linha5
try:
    p=sokoban(grelha)
    travel_sol = breadth_first_graph_search_plus(p)
    if travel_sol:
        print('Solução em',len(travel_sol.solution()),'passos')
    else:
        print('No way!')
except Exception as e:
    print(repr(e))