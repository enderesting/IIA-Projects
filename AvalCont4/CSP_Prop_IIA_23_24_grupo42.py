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
def csp_prop(formulas:Expr):

    def variables(x): # fix this bitch later
        """Return the set of all propositional symbols in x."""
        boobs = []
        for i in x:
            # print("boo",i)
            if not isinstance(i, Expr):
                return []
            elif is_prop_symbol(i.op):
                boobs += [f'{i}']
            else:
                boobs += [symbol for arg in i.args for symbol in variables({arg})]
        return list(dict.fromkeys(boobs))
    
    def domains(formulas): # fix this bitch later
        """Return the set of all propositional symbols in x."""
        dic = {}
        for expression in formulas:
            # print("boo",i)
            if not isinstance(expression, Expr):
                return set()
            elif len(expression.args) == 1 and is_prop_symbol(expression.args[0]): # ~A
                dic[expression] = [False]
            elif is_prop_symbol(expression.op): # A
                dic[expression] = [True]
            else:
                dic += [symbol for arg in expression.args for symbol in variables({arg})]
        return list(dict.fromkeys(dic))
    
    def neighbors():
        pass

    def constraints():
        pass
    
    return CSP(variables(formulas),domains(),neighbors(),constraints())
