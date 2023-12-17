from planningPlus import *
from logic import *
from utils import *
from search import * 

# receives a text input of the grid, and returns a ForwardPlan with initial state, objectives, and expanded actions
# def sokoban(grid):

def sokoban(puzzle):
    init = []
    objCoords = []
    freeCoords = []
    isSpaceCoords = []
    lines = puzzle.split("\n")[:-1]
    for y in range(len(lines)-1):
        for x in range(len(lines[y])-1):
            n_pos = lines[y][x]
            if n_pos != "#":
                isSpaceCoords.append((x,y))
            if n_pos == ".":
                freeCoords.append((x,y))
                init.append(expr(f'Free(X{x},Y{y})'))
            # elif n_pos == "#":
            #     init.append(expr(f'Wall(X{x},Y{y})'))
            elif n_pos == "o":
                objCoords.append([x,y])
                #init.append(expr(f'Obj(X{x},Y{y})'))
                freeCoords.append((x,y))
                init.append(expr(f'Free(X{x},Y{y})'))
            elif n_pos == "@":
                init.append(expr(f'Sokoban(X{x},Y{y})'))
            elif n_pos == "+":
                objCoords.append([x,y])
                init.append(expr(f'Sokoban(X{x},Y{y})'))
                #init.append(expr(f'Obj(X{x},Y{y})'))
            elif n_pos == "$":
                init.append(expr(f'Box(X{x},Y{y})'))
            elif n_pos == "*":
                objCoords.append([x,y])
                init.append(expr(f'Box(X{x},Y{y})'))
                #init.append(expr(f'Obj(X{x},Y{y})'))
    goal = ''
    for [x,y] in objCoords:
        goal += f'Box(X{x},Y{y}) &'
    goal = goal[:-2]

    # for every freeCoord, go through four directions and eliminate
    '''
    # - Wall
    o - Empty objective
    @ - Sokoban on nothing
    + - Sokoban on objective
    $ - Box on nothing
    * - Box on objective

    the big thing will be that after we make 
    fp = ForwardPlan(problem)
    we'll need to do
    fp.expanded_actions = ...  <- all the actions
    '''
    problem = PlanningProblem(initial=init, goals=goal, actions=[], domain=[])
    fp = ForwardPlan(problem)

    # def createMoveAction(from_pos,to_pos):
    #     precond = expr(f'Sokoban(X{from_pos[0]},Y{from_pos[1]}) & Free(X{to_pos[0]},Y{to_pos[1]})')
    #     efeito =  expr(f'Free(X{from_pos[0]},Y{from_pos[1]}) & Sokoban(X{to_pos[0]},Y{to_pos[1]}) \
    #                     & ~Sokoban(X{from_pos[0]},Y{from_pos[1]}) & ~Free(X{to_pos[0]},Y{to_pos[1]})')
    #     return Action(expr(f'Move(X{from_pos[0]},Y{from_pos[1]},X{to_pos[0]},Y{to_pos[1]})'), precond, efeito)
    
    # def createPushAction(from_pos,box_pos,to_pos):
    #     precond = expr(f'Sokoban(X{from_pos[0]},Y{from_pos[1]}) & Box(X{box_pos[0]},Y{box_pos[1]}) & Free(X{to_pos[0]},Y{to_pos[1]})')
    #     efeito =  expr(f'Free(X{from_pos[0]},Y{from_pos[1]}) & ~Free(X{box_pos[0]},Y{box_pos[1]}) & ~Free(X{to_pos[0]},Y{to_pos[1]}) \
    #                     & Sokoban(X{box_pos[0]},Y{box_pos[1]}) & ~Sokoban(X{from_pos[0]},Y{from_pos[1]})\
    #                     & Box(X{to_pos[0]},Y{to_pos[1]}) & ~Box(X{box_pos[0]},Y{box_pos[1]})')
    #     return Action(expr(f'PushBox(X{from_pos[0]},Y{from_pos[1]},X{box_pos[0]},Y{box_pos[1]},X{to_pos[0]},Y{to_pos[1]})'), precond, efeito)
    

    def createMoveAction(from_pos,to_pos):
        precond = expr(f'Sokoban(X{from_pos[0]},Y{from_pos[1]}) & Free(X{to_pos[0]},Y{to_pos[1]})')
        efeito =  expr(f'Free(X{from_pos[0]},Y{from_pos[1]}) & Sokoban(X{to_pos[0]},Y{to_pos[1]})')
        return Action(expr(f'Move(X{from_pos[0]},Y{from_pos[1]},X{to_pos[0]},Y{to_pos[1]})'), precond, efeito)
    
    def createPushAction(from_pos,box_pos,to_pos):
        precond = expr(f'Sokoban(X{from_pos[0]},Y{from_pos[1]}) & Box(X{box_pos[0]},Y{box_pos[1]}) & Free(X{to_pos[0]},Y{to_pos[1]})')
        efeito =  expr(f'Free(X{from_pos[0]},Y{from_pos[1]}) \
                        & Sokoban(X{box_pos[0]},Y{box_pos[1]})\
                        & Box(X{to_pos[0]},Y{to_pos[1]}) ')
        return Action(expr(f'PushBox(X{from_pos[0]},Y{from_pos[1]},X{box_pos[0]},Y{box_pos[1]},X{to_pos[0]},Y{to_pos[1]})'), precond, efeito)
    
    # `<Node (Box(X2, Y1) & Box(X3, (Y1 & ~Box(X2, Y1))) & Free(X1, Y1) & NotFree(X2, Y1) & NotFree(X3, Y1) & NotSokoban(X1, Y1) & Sokoban(X2, Y1))>`
    actions = []
    dir_dict = [(0,-1),(1,0),(0,1),(-1,0)]
    for current_pos in isSpaceCoords:
        for dir in dir_dict:
            n_pos = (current_pos[0]+dir[0],current_pos[1]+dir[1])
            if n_pos in freeCoords:
                # move
                actions.append(createMoveAction(current_pos,n_pos))
            nn_pos = (n_pos[0]+dir[0],n_pos[1]+dir[1])
            if nn_pos in freeCoords:
                # pushbox
                actions.append(createPushAction(current_pos,n_pos,nn_pos))
    fp.expanded_actions = actions
    # print(actions)

    # fp.expanded_actions = [Action('Move(player,from,to,dir)', # move <player> from _ to _ position 
    #                 precond='At(player,from) & Free(to) & MoveTo(from,to,dir)',
    #                 effect='At(player,to) & Free(from) & ~At(player,from) & ~Free(to)'),
    #                 # domain='Disco(d) & Menor(d,x) & Menor(d,y)'),
    #             Action('PushToGoal(player,block,ppos,from,to,dir)', 
    #                 precond='At(player,ppos) & At(box,from) & Free(to) & MoveTo(ppos,from,dir) & MoveTo(from,to,dir) & Goal(to)',
    #                 effect='At(player,from) & At(box,to) & Free(ppos) & ~At(player,ppos) & ~At(box,from) & ~Free(to)'), # at(box,goal)
    #                 # domain='Disco(d) & Menor(d,x) & Menor(d,y)'),
    #             Action('PushToNonGoal(player,block,ppos,from,to,dir)', 
    #                 precond='At(player,ppos) & At(box,from) & Free(to) & MoveTo(ppos,from,dir) & MoveTo(from,to,dir) & ~Goal(to)',
    #                 effect='At(player,from) & At(box,to) & Free(ppos) & ~At(player,ppos) & ~At(box,from) & ~Free(to)'), # ~at(box,goal)
    #                 # domain='Disco(d) & Menor(d,x) & Menor(d,y)'),
    #                 ] # i straight up dont know what domain does here. need to get rid of them

    return fp
    

    '''
    Action('MoveUp(x1,y1,x2,y2)')
        precond = Sokoban(x1,y1),Free(x2,y2)
        effect = Free(x1,y1),Sokoban(x2,y2)
        domain = 
        ? how to check: x1 == x2, (y2-y1) == 1 have Above(x,y)


    '''
    # fp.expanded_actions =   # function that calculates the actions? 
                            # [  Action('MoveParaMesa(b, x)',
                            #     precond='Sobre(b, x) & Livre(b)',
                            #     effect='Sobre(b, Mesa) & Livre(x) & ~Sobre(b, x)',
                            #     domain='Bloco(b) & Bloco(x)'),
                            # Action('Move(b, x, y)',
                            #     precond='Sobre(b, x) & Livre(b) & Livre(y)',
                            #     effect='Sobre(b, y) & Livre(x) & ~Sobre(b, x) & ~Livre(y)',
                            #     domain='Bloco(b) & Bloco(y)')]
    '''
    

    '''


# test 1
linha1= "######\n"
linha2= "#@.$o#\n"
linha3= "######\n"
grelha=linha1+linha2+linha3
try:
    p=sokoban(grelha)
    print(p.initial)
    print(p.actions(p.initial))
    print(p.expanded_actions)
    travel_sol = breadth_first_graph_search_plus(p)
    if travel_sol:
        print('Solução em',len(travel_sol.solution()),'passos')
    else:
        print('No way!')
except Exception as e:
    print(repr(e))
    
     	

# linha1= "##########\n"
# linha2= "#........#\n"
# linha3= "#..$..+..#\n"
# linha4= "#........#\n"
# linha5= "##########\n"
# grelha=linha1+linha2+linha3+linha4+linha5
# try:
#     p=sokoban(grelha)
#     travel_sol = breadth_first_graph_search_plus(p)
#     if travel_sol:
#         print('Solução em',len(travel_sol.solution()),'passos')
#     else:
#         print('No way!')
# except Exception as e:
#     print(repr(e))