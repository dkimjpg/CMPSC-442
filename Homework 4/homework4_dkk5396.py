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
    def __repr__(self):
        return f'Atom({self.name})'
        #pass
    def atom_names(self):
        #return f'set([{repr(self.name)}])' #check if this works properly
        return {self.name}
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
        return f'Not({self.arg})' #maybe use repr(self.arg.name) if it doesn't work
        #pass
    def atom_names(self):
        #return f'Set({self.arg})' #maybe use repr(self.arg.name) if it doesn't work
        #conjunctList = list(self.conjuncts)
        notSet = set()
        extractAtom = self.arg
        #print(extractAtom)
        if isinstance(extractAtom, set) == False: #checks if extractAtom is a set or not, if not, then extract until it is a set
            #print("gothere")
            extractAtom = extractAtom.atom_names()
            #print(extractAtom)
        notSet = notSet.union(extractAtom)
        #print("did union")
        #print(extractAtom)
        #print(notSet)
        """
        for element in conjunctList:
            extractAtom = element
            while isinstance(element, str) == False: #checks if element is a string or not, if not, then extract until it is a string
                extractAtom = extractAtom.atom_names()   #keep calling atom_names() on the element until it is just a string

            conjunctSet.add(extractAtom)             #once element is fully extracted, add it to the set
        """
        return notSet
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
        copyAndList = list(self.conjuncts)
        return f'And({copyAndList})'
        #pass
    def atom_names(self):
        conjunctList = list(self.conjuncts)
        conjunctSet = set()
        for element in conjunctList:
            extractAtom = element
            if isinstance(extractAtom, set) == False:  #checks if element is a string or not, if not, then extract until it is a string
                extractAtom = extractAtom.atom_names() #call atom_names() on the element, it will call other functions that also have atom_names() until it reaches atom(), which it will then return a set
            conjunctSet = conjunctSet.union(extractAtom)             #once element or elements are fully extracted, union it with the set
        return conjunctSet
        #newConjunctList = list(conjunctSet)
        #return f'set({newConjunctList})'


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
        """
        copyOrSet = self.disjuncts.copy()
        copyOrList = []
        for x in copyOrSet:
            copyOrList.append(next(iter(copyOrSet)))
            #copyAndList.append(copyAndSet.pop())        
        """
        #print("or ____")
        #print(copyOrList)
        #copyOrList = [next(iter(self.disjuncts)) for _ in self.disjuncts]
        copyOrList = list(self.disjuncts)
        return f'Or({copyOrList})'
        #pass
    def atom_names(self):
        disjunctList = list(self.disjuncts)
        disjunctSet = set()
        for element in disjunctList:
            extractAtom = element
            if isinstance(extractAtom, set) == False:  #checks if element is a string or not, if not, then extract until it is a string
                extractAtom = extractAtom.atom_names() #call atom_names() on the element, it will call other functions that also have atom_names() until it reaches atom(), which it will then return a set
            disjunctSet = disjunctSet.union(extractAtom)             #once element or elements are fully extracted, union it with the set
        return disjunctSet
        #return f'set([{repr(self.arg.name)}])'
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
        #impList = [self.left, self.right]
        #print(impList[0])
        #print(impList[1])
        return f'Implies({self.left}, {self.right})'
        #pass
    def atom_names(self):
        impList = [self.left, self.right]
        impSet = set()
        for element in impList:
            extractAtom = element
            if isinstance(extractAtom, set) == False:  #checks if element is a string or not, if not, then extract until it is a string
                extractAtom = extractAtom.atom_names() #call atom_names() on the element, it will call other functions that also have atom_names() until it reaches atom(), which it will then return a set
            impSet = impSet.union(extractAtom)                  #once element or elements are fully extracted, union it with the set
        return impSet
        #return f'set([{repr(self.arg.name)}])'
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
        return f'Iff({self.left}, {self.right})'
        #pass
    def atom_names(self):
        iffList = [self.left, self.right]
        iffSet = set()
        for element in iffList:
            extractAtom = element
            if isinstance(extractAtom, set) == False:  #checks if element is a string or not, if not, then extract until it is a string
                extractAtom = extractAtom.atom_names() #call atom_names() on the element, it will call other functions that also have atom_names() until it reaches atom(), which it will then return a set
            iffSet = iffSet.union(extractAtom)                  #once element or elements are fully extracted, union it with the set
        return iffSet
        #pass
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



print("\n1.3")
print(Atom("a").atom_names())
print(Not(Atom("a")).atom_names())
a, b, c = map(Atom, "abc")
expr = And(a, Implies(b, Iff(a, c)))
print(expr.atom_names())
