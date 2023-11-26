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
    
    def variables():
        """
        returns a list of variables
        e.g. ['A', 'B', 'C']
        """
        def prop_symbols(x):
            """Return the set of all propositional symbols in x."""
            if not isinstance(x, Expr):
                return set()
            elif is_prop_symbol(x.op):
                return {str(x)}
            else:
                return {symbol for arg in x.args for symbol in prop_symbols(arg)}
        vars = set()
        for f in formulas:
            vars.update(prop_symbols(f))
        return sorted(vars)

    vars = variables()

    def domains():
        """
        for each variable, returns values it could be. unary expressions are applied to each variable's domain
        e.g. {'A': [False, True], 'B': [False, True], 'C': [False, True]}
        """
        dic = {}
        literals = [x for x in kb.clauses if len(disjuncts(x)) == 1]
        for l in literals:
            if l.op == '~':
                dic[str(l.args[0])] = [False]
            else:
                dic[l.op] = [True]
        for v in vars:
            if str(v) not in dic:
                dic[v] = [False,True]
        return dic
    
    def extract_prop(literal:Expr):
        """
        given ~A returns A
        given A returns A
        make sure the input is actually a literal
        """
        if len(literal.args) == 1 and is_prop_symbol(str(literal.args[0])):
            return literal.args[0]
        elif is_prop_symbol(literal.op):
            return literal
    

    def neighbors():
        """
        returns each variable and its neighbor in disjunction in a CNF form.
        single literals have no neighbors
        e.g. {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
        """
        nbs = {}
        for i in vars: 
            nbs[i] = [] 
        for clause in kb.clauses: #[(B | ~A), (C | ~A), ~A]
            lit_list = disjuncts(clause) # (Z | ~A) -> [Z, ~A]
            for lit in lit_list:
                this_lit = extract_prop(lit)
                for other in lit_list:
                    other_lit = extract_prop(other)
                    if other_lit is not this_lit and other_lit not in nbs[str(this_lit)]:            
                                nbs[str(this_lit)].append(str(other_lit)) 
        return nbs

    def constraints(var1, var1_value, var2, var2_value):
        """
        given var1 var2 and its respective values, checks if it can be satisfied in the current kb.
        """
        model = {expr(var1) : var1_value, expr(var2) : var2_value}
        # var1 = '~'+var1 if not var1_value else var1
        # var2 = '~'+var2 if not var2_value else var2
        # final = var1 + ' & ' + var2
        # huge = expr(final)
        # result = kb.ask_if_true(huge)
        # return result

        result = True
        for clause in kb.clauses:
           disjunction = disjuncts(clause)
           if len(disjunction) == 2:
               prop1, prop2 = disjunction[0], disjunction[1]
               prop1 = prop1.op if len(prop1.args) == 0 else str(prop1.args[0])
               prop2 = prop2.op if len(prop2.args) == 0 else str(prop2.args[0])
               if (var1 == prop1 or var1 == prop2) and (var2 == prop1 or var2 == prop2):
                   satisfies = False if not pl_true(clause, model) else True # if it's true/none, returns satisfies
                   result = result and satisfies
        return result
    
    return CSP(vars,domains(),neighbors(),constraints)

# x={expr('A ==> (B & C)'),expr('A')}
# print(csp_prop(x))


x = expr('(A ==> (B & C))')
y = expr('A|~A')
z = [x,y]
csp_p = csp_prop(z)
# print(tt_entails(expr('A ==> (B & C)'), expr('~A | B | C'),True))

kb = PropKB()
for i in z:
    kb.tell(i)
print(kb.clauses)
print('\n now the csp')
# print(kb.ask_if_true(expr('B & A')))
# print(kb.ask_if_true(expr('~B & A')))



print(z)
print(csp_p.variables)
print(csp_p.domains)
print(csp_p.neighbors)# it repeats stuff
print(csp_p.constraints)
assignment = backtracking_search(csp_p)
print('assignment = ',assignment )