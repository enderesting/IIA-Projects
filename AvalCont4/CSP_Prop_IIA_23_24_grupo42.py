'''
Yichen Cao "Mimi" fc58165
Gonçalo Fernandes fc58194
Github repo: https://github.com/enderesting/IIA-Projects
'''
from csp import *
from utils import *
from logic import *

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
            if not isinstance(x,Expr):
                return set()
            elif is_prop_symbol(x.op):
                return {str(x)}
            else:
                return {symbol for arg in x.args for symbol in prop_symbols(arg)}
        vares = set()
        for f in formulas:
            vares.update(prop_symbols(f))
        return sorted(vares)

    vares = variables()

    def domains():
        """
        for each variable, returns values it could be. unary expressions are applied to each variable's domain
        e.g. {'A': [False, True], 'B': [False, True], 'C': [False, True]}
        """
        dic = {}
        for i in vares:
            dic[i] = [False, True]
        literals = [x for x in kb.clauses if len(disjuncts(x)) == 1]
        for l in literals:
            if l.op == '~':
                dic[str(l.args[0])] = [value for value in dic[str(l.args[0])] if value is False]
            else:
                dic[l.op] = [value for value in dic[l.op] if value is True]
        return dic
    
    def extract_prop(literal:Expr):
        """
        given ~A returns A
        given A returns A
        make sure the input is actually a literal
        returns a string!
        """
        if len(literal.args) == 1 and is_prop_symbol(str(literal.args[0])):
            return str(literal.args[0])
        elif is_prop_symbol(literal.op):
            return str(literal)

    def neighbors():
        """
        returns each variable and its neighbor in disjunction in a CNF form.
        single literals have no neighbors
        e.g. {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
        """
        nbs = {}
        for i in vares: 
            nbs[i] = [] 
        for clause in kb.clauses: #[(B | ~A), (C | ~A), ~A]
            lit_list = disjuncts(clause) # (Z | ~A) -> [Z, ~A]
            for lit in lit_list:
                this_lit = extract_prop(lit)
                for other in lit_list:
                    other_lit = extract_prop(other)
                    if other_lit is not this_lit and other_lit not in nbs[this_lit]:            
                        nbs[this_lit].append(other_lit) 
                        nbs[this_lit].sort()
        return nbs

    def constraints(var1, var1_value, var2, var2_value):
        """
        given var1 var2 and its respective values, checks if it can be satisfied in the current kb.
        or rather, if it "doesn't contradict with anything in the kb"
        """
        model = {expr(var1) : var1_value, expr(var2) : var2_value}

        result = True
        for clause in kb.clauses:
           disjunction = disjuncts(clause)
           if len(disjunction) == 2:
               p1, p2 = disjunction[0], disjunction[1]
               prop1 = extract_prop(p1)
               prop2 = extract_prop(p2)
               if (var1 == prop1 or var1 == prop2) and (var2 == prop1 or var2 == prop2):
                   satisfies = pl_true(clause,model) # False if not pl_true(clause, model) else True # if it's true/none, returns satisfies
                   result = result and satisfies
        return result
    
    return CSP(vares,domains(),neighbors(),constraints)


x = expr('(A ==> (C & B))')
y = expr('A')
z = [x,y]

kb = PropKB()
for i in z:
    exp = expr(i)
    print(exp)
    kb.tell(exp)

print(kb.clauses)

print('\n now the csp')
# print(kb.ask_if_true(expr('B & A')))
# print(kb.ask_if_true(expr('~B & A')))

csp_p = csp_prop(kb.clauses)

print(z)
print(csp_p.variables)
print(csp_p.domains)
print(csp_p.neighbors)# it repeats stuff
print(csp_p.constraints)
assignment = backtracking_search(csp_p)
print('assignment = ',assignment )