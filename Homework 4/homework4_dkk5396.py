############################################################
# CMPSC 442: Logic
############################################################

student_name = "David Kim"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.



############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        #these print statements are to check if other is like self.name or if other is like self, need to know the difference
        #print(self.name)
        #print(other.name)
        if self.name == other: 
            return True
        else:
            return False
        #pass
    def __repr__(self): #do this later
        return f'Atom({self.name})'
        #pass
    def atom_names(self):
        return f'set([{repr(self.name)}])' #check if this works properly
        #pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        if self.arg == other: 
            return True
        else:
            return False
        #pass
    def __repr__(self):
        pass
    def atom_names(self):
        return f'Not({repr(self.arg.name)})'
        #pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass
        
class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        if self.conjuncts == other.conjuncts: 
            return True
        else:
            return False
        #pass
    def __repr__(self):
        #return f'And({repr(self.conjuncts.name)})'
        #pass
    def atom_names(self):
        conjunctList = list(self.conjuncts)
        print(conjunctList[0].name)
        #print(len(self.conjuncts))
        #return f'set([{self.conjuncts}])'
        #pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        if self.name == other: 
            return True
        else:
            return False
        #pass
    def __repr__(self):
        pass
    def atom_names(self):
        return f'set([{repr(self.arg.name)}])'
        #pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        if self.name == other: 
            return True
        else:
            return False
        #pass
    def __repr__(self):
        impList = [self.left, self.right]
        return f'Implies({repr(impList)})'
        #pass
    def atom_names(self):
        
        return f'set([{repr(self.arg.name)}])'
        #pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        if self.name == other: 
            return True
        else:
            return False
        #pass
    def __repr__(self):
        pass
    def atom_names(self):
        pass
    def evaluate(self, assignment):
        pass
    def to_cnf(self):
        pass

def satisfying_assignments(expr):
    pass

class KnowledgeBase(object):
    def __init__(self):
        pass
    def get_facts(self):
        pass
    def tell(self, expr):
        pass
    def ask(self, expr):
        pass

############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

# Populate the knowledge base using statements of the form kb1.tell(...)
kb1 = KnowledgeBase()

# Write an Expr for each query that should be asked of the knowledge base
mythical_query = None
magical_query = None
horned_query = None

# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = None
is_magical = None
is_horned = None

# Puzzle 2

# Write an Expr of the form And(...) encoding the constraints
party_constraints = None

# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = None

# Write your answer to the question in the assignment
puzzle_2_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
# guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""


#####################################################
# Test Cases
#####################################################

print("Section 1: Propositional Logic")

print("\n1.1")
print(Atom("a") == Atom("a")) #should return True
print(Atom("a") == Atom("b")) #should return False
print(And(Atom("a"), Not(Atom("b"))) == And(Not(Atom("b")), Atom("a"))) #should return True


print("\n1.2")
a, b, c = map(Atom, "abc")
print(Implies(a, Iff(b, c))) #should return: Implies(Atom(a), Iff(Atom(b), Atom(c)))
a, b, c = map(Atom, "abc")
print(And(a, Or(Not(b), c))) #should return: And(Atom(a), Or(Not(Atom(b)), Atom(c)))


"""
print("1.3")
print(Atom("a").atom_names())
print(Not(Atom("a")).atom_names())
a, b, c = map(Atom, "abc")
expr = And(a, Implies(b, Iff(a, c)))
print(expr.atom_names())
"""