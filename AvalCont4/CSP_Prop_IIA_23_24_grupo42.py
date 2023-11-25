'''
Yichen Cao "Mimi" fc58165
Gonçalo Fernandes fc58194
Github repo: https://github.com/enderesting/IIA-Projects
'''
from csp import *
from utils import *
from logic import *

"""
    A CSP is specified by the following inputs:
        variables        A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
"""

# eg formulas: {expr('A ==> (B & C)'),expr('A')}
def csp_prop(formulas:{Expr}):

    kb = PropKB()
    for x in formulas:
        kb.tell(x)

    def variables(formulas):
        """
        returns a list of variables
        e.g. ['A', 'B', 'C']
        """
        return list(domains(formulas).keys())
    
    def domains(formulas):
        """
        for each variable, returns values it could be. unary expressions are applied to each variable's domain
        e.g. {'A': [False, True], 'B': [False, True], 'C': [False, True]}
        """
        dic = {}
        for expression in formulas:
            if not isinstance(expression, Expr):
                return set()
            elif len(expression.args) == 1 and is_prop_symbol(str(expression.args[0])): # ~A
                dic[str(expression.args[0])] = [False]
            elif is_prop_symbol(expression.op): # A
                dic[expression.op] = [True]
            else:
                dic = domains_aux(expression,dic)
        keys = list(dic.keys())
        keys.sort()
        dic = {i: dic[i] for i in keys}
        return dic

    def domains_aux(expression,dic):
        """
        Auxillary function for domains()
        """
        def add_to_dict(arg):
            if arg not in dic.keys():
                dic[arg] = [False,True]
        for arg in expression.args:
            if is_prop_symbol(arg.op):
                add_to_dict(arg.op)
            elif(len(expression.args) == 1 and is_prop_symbol(str(arg.args[0]))):
                add_to_dict(str(arg.args[0]))
            else:
                dic = domains_aux(arg,dic)
        return dic
    
    def neighbors(formulas):
        """
        returns each variable and its neighbor in disjunction in a CNF form.
        single literals have no neighbors
        e.g. {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
        """
        neighbors = {}
        for i in variables(formulas):
            neighbors[i] = [] 
        for expression in formulas: # expr('A ==> (Z & C)')
            expression = to_cnf(expression) # ((Z | ~A) & (C | ~A))
            disj_list = conjuncts(expression) # [(Z | ~A), (C | ~A)]
            for prop_list in disj_list:
                prop_list = disjuncts(prop_list) # (Z | ~A) -> [Z, ~A]
                if len(prop_list) == 2:
                    prop1 = prop_list[0]
                    prop2 = prop_list[1]
                    prop1 = prop1.op if len(prop1.args) == 0 else str(prop1.args[0])
                    prop2 = prop2.op if len(prop2.args) == 0 else str(prop2.args[0])
                    
                    if prop2 not in neighbors[prop1]: neighbors[prop1].append(prop2)
                    if prop1 not in neighbors[prop2]: neighbors[prop2].append(prop1)
        return neighbors

    def constraints(var1, var1_value, var2, var2_value):
        """
        given var1 var2 and its respective values, checks if it can be satisfied in the current kb.
        """
        #model = {expr(var1) : var1_value, expr(var2) : var2_value}
        var1 = '~'+var1 if not var1_value else var1
        var2 = '~'+var2 if not var2_value else var2
        final = var1 + ' & ' + var2
        huge = expr(final)
        result = kb.ask_if_true(huge)
        return result
    
    return CSP(variables(formulas),domains(formulas),neighbors(formulas),constraints)

# x={expr('A ==> (B & C)'),expr('A')}
# print(csp_prop(x))


x = expr('(A ==> (B & C))')
y = expr('(A | ~B) & ~D')
z = [x,y]
csp_p = csp_prop(z)
# print(tt_entails(expr('A ==> (B & C)'), expr('~A | B | C'),True))

# kb = PropKB()
# kb.tell(x)
# print(kb.clauses)
# print(kb.ask_if_true(expr('B & A')))
# print(kb.ask_if_true(expr('~B & A')))



print(z)
print(csp_p.variables)
print(csp_p.domains)
print(csp_p.neighbors)# it repeats stuff
print(csp_p.constraints)