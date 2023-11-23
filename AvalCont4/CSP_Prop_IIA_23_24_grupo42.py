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

    def variables(formulas): # fix this bitch later
        return list(domains(formulas).keys())
    
    def domains(formulas):
        """Return the set of all propositional symbols in x."""
        dic = {}
        for expression in formulas:
            # print("boo",i)
            if not isinstance(expression, Expr):
                return set()
            elif len(expression.args) == 1 and is_prop_symbol(str(expression.args[0])): # ~A
                dic[str(expression.args[0])] = [False]
            elif is_prop_symbol(expression.op): # A
                dic[expression.op] = [True]
            else:
                dic = domains_aux(expression,dic)
        return dic #list(dict.fromkeys(dic))

    def domains_aux(expression,dic):
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
    
    def neighbors():
        pass

    def constraints():
        pass
    
    return CSP(variables(formulas),domains(formulas),neighbors(),constraints())

x={expr('A ==> (B & C)'),expr('A')}
print(csp_prop(x))