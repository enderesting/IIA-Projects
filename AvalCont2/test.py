from collections import namedtuple
from searchPlus import *
from MedoTotal import MedoTotal
import timeit    # Para tirar
import queue

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

            # if optimal:
            #     # if new_node < best cost
            #         # expand

            if not optimal or (best is None or new_node.path_cost < best.path_cost):
                is_goal, is_best = problem.goal_test(new_node.state), (best is None or new_node.path_cost < best.path_cost)
                if is_goal:
                    finais += 1
                    if best is None or is_best:
                        best = new_node
                    visited += 1
                    if verbose: pretty_print(problem,new_node,is_goal,is_best)
                else: # if its not goal,
                    expansion.append(new_node)

            # is_goal, is_best = problem.goal_test(new_node.state), (best is None or new_node.path_cost < best.path_cost)
            # if is_goal:
            #     finais += 1
            #     if best is None or is_best:
            #         best = new_node
            #     visited += 1
            #     if verbose: pretty_print(problem,new_node,is_goal,is_best)
            # else:
            #     if optimal and best and new_node.path_cost >= best.path_cost: # a goal that isnt optimal isnt processed either
            #         continue
            #     else:
            #         expansion.append(new_node)
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


# parametros="T=6\nM=4\nP=10"
# linha1= "= = = = = =\n"
# linha2= "= . @ F * =\n"
# linha3= "= . . . . =\n"
# linha4= "= . = . . =\n"
# linha5= "= . = . . =\n"
# linha6= "= = = = = =\n"
# grelha=linha1+linha2+linha3+linha4+linha5+linha6
# mundoStandard2=parametros + "\n" + grelha
# gx=MedoTotal(mundoStandard2)
#print(gx.display(gx.initial))

# resultado,max_mem,visitados,finais = depth_first_tree_search_all_count(gx,verbose=True)

# stop = timeit.default_timer()
# print('*'*20)
# if resultado:
#     print("\nSolução Prof-total (árvore) com custo", str(resultado.path_cost)+":")
#     print(resultado.solution())
# else:
#     print('\nSem Solução')
# print('Visitados=',visitados)
# print('Dimensão máxima da memória',max_mem)
# print('Estados finais:',finais)

# start = timeit.default_timer()

# resultado,max_mem,visitados,finais = depth_first_tree_search_all_count(gx,True,True)

# stop = timeit.default_timer()
# print('*'*20)
# if resultado:
#     print("\nSolução Prof-total (árvore) com custo", str(resultado.path_cost)+":")
#     print(resultado.solution())
# else:
#     print('\nSem Solução')
# print('Visitados=',visitados)
# print('Dimensão máxima da memória',max_mem)
# print('Estados finais:',finais)
# print('Time: ', stop - start)

parametros="T=15\nM=6\nP=10"
linha1= "= = = = = =\n"
linha2= "= * F @ * =\n"
linha3= "= . . . . =\n"
linha4= "= . = . . =\n"
linha5= "= . = . . =\n"
linha6= "= = = = = =\n"
grelha=linha1+linha2+linha3+linha4+linha5+linha6
mundoStandard2=parametros + "\n" + grelha
gx=MedoTotal(mundoStandard2)
print(gx.display(gx.initial))



#sem optimizacao
start = timeit.default_timer()

resultado,max_mem,visitados,finais = depth_first_tree_search_all_count(gx,optimal=True)

stop = timeit.default_timer()
print('*'*20)
if resultado:
    print("Solução Prof-total (grafo) com custo", str(resultado.path_cost)+":")
    print(resultado.solution())
else:
    print('Sem Solução')
print('Visitados=',visitados)
print('Dimensão máxima da memória',max_mem)
print('Estados finais:',finais)
print('Time: ', stop - start)