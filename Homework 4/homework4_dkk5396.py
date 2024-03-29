############################################################
# CMPSC 442: Logic
############################################################

student_name = "David Kim"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import itertools

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
        #if isinstance(other, Atom) == False:
            #return False
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
        #print(assignment) #in case for some strange reason assignment has more than one key
        #print(self.name)
        #if isinstance(self, Atom) == True:
            #return self.name
        atomKeys = assignment.keys()
        atomKeys = list(atomKeys)
        return assignment.get(self.name) #I have no idea what it wants me to return if evaluate() is called on Atom(), so I'll just return the value in the assignment dictionary (there should only be one key in it, anyway)
        #pass
    def to_cnf(self):
        print("Atom")
        return self
        #pass

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        #if isinstance(other, Not) == False:
            #return False
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
            extractAtom = extractAtom.atom_names()
        notSet = notSet.union(extractAtom)

        return notSet
        #pass
    def evaluate(self, assignment):
        #print(assignment) #in case for some strange reason assignment has more than one key       
        exprFlag = False
        #boolExtract = ""
        if isinstance(self.arg, Atom) == False:
            exprFlag = True
        
        if isinstance(self.arg, Atom) == True:
            boolExtract = self.arg.evaluate(assignment)
            if boolExtract == True:
                return False
            if boolExtract == False:
                return True
            #return boolExtract
        

        if exprFlag == True:
            newBool = self.arg.evaluate(assignment)
            #if assignment.get(newBool) == True:
                #return False
            #if assignment.get(newBool) == False:
                #return True
            if newBool == True:
                    return False
            if newBool == False:
                    return True



        #by this point, it should be confirmed that assignment (which is valAssignment) is a dictionary, so continue with my original code
        #notKeys = assignment.keys()
        #notKeys = list(notKeys)
        #realNotKey = notKeys[0] #there's only one key in the assignment dictionary, so just call it realNotKey
        valueOfKey = assignment.get(self.arg)
        #return not valueOfKey #Honestly, I don't trust Python enough to do this
        if valueOfKey == True:
            return False
        if valueOfKey == False:
            return True
        #pass
    def to_cnf(self):
        if isinstance(self.arg, Atom) == True:
            return Not(self.arg)
        if isinstance(self.arg, Not) == True:
            return self.arg
        if isinstance(self.arg, And) == True: #try to just iterate through .disjuncts and apply Not to each one, then add it to a tuple (or a list, I'm not sure) and then put that tuple in the return that I have right now
            notList = []
            for x in self.arg.conjuncts:
                notList.append(Not(x))
            notTuple = tuple(notList)
            return Or(notTuple).to_cnf()
        if isinstance(self.arg, Or) == True:
            notList = []
            for x in self.arg.disjuncts:
                notList.append(Not(x))
            notTuple = tuple(notList)
            return And(notTuple).to_cnf()
        #if isinstance(self.arg, Implies) == True:

        #pass
        
class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        #if isinstance(other, And) == False:
            #return False
        #if self.conjuncts == other.conjuncts:
        if self.conjuncts == other:
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
            if isinstance(extractAtom, set) == False:    #checks if element is a string or not, if not, then extract until it is a string
                extractAtom = extractAtom.atom_names()   #call atom_names() on the element, it will call other functions that also have atom_names() until it reaches atom(), which it will then return a set
            conjunctSet = conjunctSet.union(extractAtom) #once element or elements are fully extracted, union it with the set
        return conjunctSet
        #newConjunctList = list(conjunctSet)
        #return f'set({newConjunctList})'

        #return f'set([{self.conjuncts}])'
        #pass
    def evaluate(self, assignment):        
        exprFlag = False
        for literal in self.conjuncts: #go through the conjuncts dictionary and check if there are any expressions instead of Atom objects, if there are, set the exprFlag to True
            if isinstance(literal, Atom) == False: #checks if current element is not an Atom()
                exprFlag = True

        #if exprFlag == True: #need to extract boolean values            
            #listAssignment = []
        for literal in self.conjuncts:
            newBool = literal.evaluate(assignment) #evaluating literal should yield a list
            #listAssignment.extend(newBool)
            if newBool == False: #a literal with a value of False was found, return False
                return False


        #for literal in listAssignment:
            #if assignment.get(literal) == False: #a literal with a value of True was found, return True
                #return False
        return True #assuming that not a single False was found in the literals



        #pass
    def to_cnf(self):        
        tupleExtractionList = []
        copyConjuncts = list(self.conjuncts)
        while isinstance(copyConjuncts[0], tuple) == True:
            for contents in copyConjuncts[0]:
                tupleExtractionList.append(contents)
            copyConjuncts = tupleExtractionList

        checkAndFlag = False
        for literal in copyConjuncts: #checks for any Or that is inside Or, simplifies to take out the Or            
            if isinstance(literal, And) == True:
                checkAndFlag = True
                orLiteralList = []
                for orLiterals in literal.conjuncts:
                    orLiteralList.append(orLiterals)
                copyConjuncts.extend(orLiteralList)
                indexOfLiteral = copyConjuncts.index(literal)
                copyConjuncts.pop(indexOfLiteral)
        
        if checkAndFlag == True:
            return And(tuple(copyConjuncts))
        

        conjunctsList = []
        
        iterateList = list(self.conjuncts)
        if isinstance(iterateList[0], tuple):
            iterateList = tupleExtractionList
        #iterateList = iterateList[0]
        for literal in iterateList:
            conjunctsList.append(literal.to_cnf())
        
        for literal in conjunctsList: #checks for any Or that is inside Or, simplifies to take out the Or            
            if isinstance(literal, And) == True:
                checkAndFlag = True
                orLiteralList = []
                for orLiterals in literal.conjuncts:
                    orLiteralList.append(orLiterals)
                conjunctsList.extend(orLiteralList)
                indexOfLiteral = conjunctsList.index(literal)
                conjunctsList.pop(indexOfLiteral)

        #if checkAndFlag == True:
            #return And(tuple(conjunctsList))
        
        return And(tuple(conjunctsList))


        #reverseTuple = list(self.conjuncts)
        #reverseTuple.reverse()
        #reverseTuple = tuple(reverseTuple)
        #return And(reverseTuple)
        #pass

class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):

        #if self.disjuncts == other.disjuncts:
        #if isinstance(other, Or) == False:
            #return False
        if self.disjuncts == other or other == self.disjuncts: #check this
            return True

        else:
            return False
        #pass
    def __repr__(self):

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
            if isinstance(extractAtom, set) == False:    #checks if element is a string or not, if not, then extract until it is a string
                extractAtom = extractAtom.atom_names()   #call atom_names() on the element, it will call other functions that also have atom_names() until it reaches atom(), which it will then return a set
            disjunctSet = disjunctSet.union(extractAtom) #once element or elements are fully extracted, union it with the set
        return disjunctSet
        #return f'set([{repr(self.arg.name)}])'
        #pass
    def evaluate(self, assignment):
        exprFlag = False
        for literal in self.disjuncts: #go through the assignment dictionary and check if there are any expressions instead of dictionaries, if there are, set the exprFlag to True
            if isinstance(literal, Atom) == False:
                exprFlag = True
        
        if exprFlag == True: #need to extract boolean values
            #listAssignment = []
            for literal in self.disjuncts:
                newBool = literal.evaluate(assignment) #evaluating literal should yield a list of some sort
                #listAssignment.extend(newBool)
                if newBool == True: #a literal with a value of True was found, return True
                    return True
                

            #for literal in listAssignment:
                #if assignment.get(literal) == True: #a literal with a value of True was found, return True
                    #return True
            return False #assuming that not a single True was found in the literals
        


        if exprFlag == False: #all entries are just dictionaries (which makes things easier)
            #andKeys = assignment.keys()
            for literal in assignment:
                if assignment.get(literal) == True: #a literal with a value of True was found, return True
                    return True
            return False #all literals were False, so return False
        #pass
    def to_cnf(self):
        #print("or rightnow")
        
        #self.disjuncts is a frozen set, so I need to convert it to something else before changing it
        
        tupleExtractionList = []
        copyDisjuncts = list(self.disjuncts)        
        if isinstance(copyDisjuncts[0], tuple) == True:
            for contents in copyDisjuncts[0]:
                tupleExtractionList.append(contents)
            copyDisjuncts = tupleExtractionList

        #print(copyDisjuncts)

        checkOrFlag = False
        for literal in copyDisjuncts: #checks for any Or that is inside Or, simplifies to take out the Or            
            if isinstance(literal, Or) == True:
                checkOrFlag = True
                #print("in or of ORs right now")
                #print(self.disjuncts)
                #print(literal)
                orLiteralList = []
                for orLiterals in literal.disjuncts:
                    orLiteralList.append(orLiterals)
                copyDisjuncts.extend(orLiteralList)
                print(f'copyDisjuncts: {copyDisjuncts}')
                print(f'literal: {literal}')
                indexOfLiteral = copyDisjuncts.index(literal)
                copyDisjuncts.pop(indexOfLiteral)
        
        print("Or")

        if checkOrFlag == True:
            return Or(tuple(copyDisjuncts))

        checkAndFlag = False
        secondDisjunctsCopy = list(self.disjuncts)
        if isinstance(secondDisjunctsCopy[0], tuple):
            secondDisjunctsCopy = tupleExtractionList
            print("got here ----------------------")
        print(f'secondDisjuncts: {secondDisjunctsCopy}')
        print(f'secondDisjuncts[0]: {secondDisjunctsCopy[0]}')
        andIndex = 0 #assumes that there is only one And in an Or, if there's multiple, I've got no idea how to implement distributivity of Or over And
        for literal in secondDisjunctsCopy:
            if isinstance(literal, And) == True:
                print(f'checkAndFlag is True')
                checkAndFlag = True
                andIndex = secondDisjunctsCopy.index(literal)

        
        
        distributivityList = []
        
        if checkAndFlag == True: #at this point, I'm just assuming there's only going to be two things for an And whenever I need to implement distributivity of Or over And
            andExpr = list(secondDisjunctsCopy[andIndex].conjuncts)
            print(f'andExpr before tupleExtract: {andExpr}')
            if isinstance(andExpr[0], tuple) == True:                
                andTupleExtract = []
                for contents in andExpr[0]:
                    andTupleExtract.append(contents)
                andExpr = andTupleExtract
                print(f'andExpr: {andExpr}')
                print(f'andExpr[0]: {andExpr[0]}')
                print("gniwgesfojaesiofjiojgiorjiogjwioguorgiuoq4wgtiuqeiugtqeiugiuqegiuogwiuoniuogf")
                print(f'andExpr: {andExpr}')
                countAnds = len(secondDisjunctsCopy)
                countAndsCounter = 0
                for literal in secondDisjunctsCopy:
                    if isinstance(literal, And) == True:
                        countAndsCounter = countAndsCounter + 1
                if countAndsCounter == countAnds: #it's all Ands
                    finalOrList = []
                    extractAnds = []
                    for p in secondDisjunctsCopy:
                        for extr in p.conjuncts:
                            for exxxx in extr:
                                #print(exxxx)
                                extractAnds.append(exxxx)
                    print(f'extractAnds: {extractAnds}')
                    for extAnd in extractAnds:
                        for extPair in extractAnds:
                            #print(extAnd)
                            #print(extPair)
                            pair = [extAnd, extPair]
                            makeOrPair = Or(tuple(pair))
                            if not(extAnd == extPair):
                                if makeOrPair not in finalOrList:
                                    if len(finalOrList) == 0:
                                            finalOrList.append(makeOrPair)
                                    
                                    for go in finalOrList:
                                        if not(makeOrPair == go) and makeOrPair not in finalOrList:
                                            finalOrList.append(makeOrPair)
                    return And(tuple(finalOrList))

                for literal in secondDisjunctsCopy:
                    if isinstance(literal, And) == False:
                        distributivityList.append(Or(tuple([literal, andExpr[0]])))
                        distributivityList.append(Or(tuple([literal, andExpr[1]])))
                print(f'distributivity List: {distributivityList}')
                return And(tuple(distributivityList))


        print("checking all literals in Or")
        print(self.disjuncts)

        #checks if all elements are Atoms
        allAtomCheckFlag = True
        for literal in self.disjuncts:
            if isinstance(literal, Atom) == False:
                allAtomCheckFlag = False
        if allAtomCheckFlag == True:
            return Or(tuple(self.disjuncts))

        disjunctsList = []

        for literal in self.disjuncts: #checks for any And that is inside Or, does distributivity of Or over And if true
            print(f'literal in disjunctsList: {literal}')
            disjunctsList.append(literal.to_cnf())
            #if isinstance(literal, And) == True:
                #print("in or right now")
                #disjunctsList = tuple(self.disjuncts)    
        print(f'disjunctsList after stuff: {disjunctsList}')
        return Or(tuple(disjunctsList)).to_cnf()
        #return And(Or(disjunctsList).to_cnf()) #this probably isn't right, but it's the only thing I can think of doing right now.


        #for literal in copyDisjuncts: #checks for any Or that is inside Or, simplifies to take out the Or

        #pass

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        #if isinstance(other, Implies) == False:
            #return False
        if self.left == other.left and self.right == other.right: 
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
            impSet = impSet.union(extractAtom)         #once element or elements are fully extracted, union it with the set
        return impSet
        #return f'set([{repr(self.arg.name)}])'
        #pass
    def evaluate(self, assignment):
        exprFlag = False
        
        if isinstance(self.left, Atom) == False:
            exprFlag = True
        if isinstance(self.right, Atom) == False:
            exprFlag = True
        
        #if exprFlag == True:
        leftBool = self.left.evaluate(assignment)
        rightBool = self.right.evaluate(assignment)
        #if assignment.get(leftBool) == True and assignment.get(rightBool) == False:
            #return False
        if leftBool == True and rightBool == False:
            return False
        return True


        #pass
    def to_cnf(self):
        #print("asdfasdf")
        #print(self.left)
        #print(self.left.to_cnf())
        #print(self.right)
        #print(self.right.to_cnf())
        #return Or(Not(self.left).to_cnf(), self.right.to_cnf())
        print("Implies")
        return Or(Not(self.left), self.right).to_cnf()
        #pass

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
        #pass
    def __eq__(self, other):
        #if isinstance(other, Iff) == False:
            #return False
        if self.left == other.left and self.right == other.right: 
            return True
        if self.left == other.right and self.right == other.left:
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
            iffSet = iffSet.union(extractAtom)         #once element or elements are fully extracted, union it with the set
        return iffSet
        #pass
    def evaluate(self, assignment):
        exprFlag = False
        
        if isinstance(self.left, Atom) == False:
            exprFlag = True
        if isinstance(self.right, Atom) == False:
            exprFlag = True
        
        #if exprFlag == True:
        leftBool = self.left.evaluate(assignment)
        rightBool = self.right.evaluate(assignment)

        #if assignment.get(leftBool) == True and assignment.get(rightBool) == True:
            #return True
        #if assignment.get(leftBool) == False and assignment.get(rightBool) == False:
            #return True
        if leftBool == True and rightBool == True:
            return True
        if leftBool == False and rightBool == False:
            return True
        return False

        #pass
    def to_cnf(self):
        print("Iff")
        return And(Implies(self.left, self.right), Implies(self.right, self.left)).to_cnf() #not sure if And does not need .to_cnf or if they all need it
        #pass

def extract(expr): #this should return a list of all the variables(literals, I think) I need
    exprCurr = expr #current expression, don't really need this but I don't want to go and change all the variable names just in case
    #exprList = []
    #while isinstance(exprCurr, list) == False:
    if isinstance(exprCurr, Atom):
        #exprList.extend([exprCurr.name])
        #print(exprCurr.name)
        return [exprCurr.name]
    elif isinstance(exprCurr, Not):
        return extract(exprCurr.arg)
    elif isinstance(exprCurr, And):
        tempList = []
        for x in exprCurr.conjuncts: #iterate through each element in the conjuncts list
            tempExtract = extract(x)
            tempList.extend(tempExtract)
        return tempList
    elif isinstance(exprCurr, Or):
        tempList = []
        for x in exprCurr.disjuncts: #iterate through each element in the conjuncts list
            tempExtract = extract(x)
            tempList.extend(tempExtract)
        return extract(tempList)
    elif isinstance(exprCurr, Implies):
        leftExtract = extract(exprCurr.left)
        #print("left")
        #print(leftExtract)
        rightExtract = extract(exprCurr.right)
        #print("right")
        #print(rightExtract)
        leftExtract.extend(rightExtract)
        #print("leftExtractJoin")
        #print(leftExtract)
        return leftExtract
    elif isinstance(exprCurr, Iff):
        leftExtract = extract(exprCurr.left)
        rightExtract = extract(exprCurr.right)
        leftExtract.extend(rightExtract)
        return leftExtract

def satisfying_assignments(expr):
    extractList = extract(expr)
    #print(extractList)
    extractLen = len(extractList) #after extracting the literals, get the length of the list here
    boolCombo = list(itertools.product([True,False], repeat = extractLen)) #gives a 2d list of all the possible combinations
    #print(boolCombo)
    #from here, just iterate through boolCombo and the list of literals I extracted (whenever I get to that) and make dictionaries
    
    #I'm thinking of a for loop that has a length that's the same as boolCombo, and then another for loop inside that has
    # a length of 3 (0, 1, 2). I might need another for loop inside that so I can select the correct letter while making the
    #dictionaries

    listOfAssignments = []

    for rowIndex, row in enumerate(boolCombo):
        assignDict = {}
        for colIndex, item in enumerate(row):
            assignDict.update({extractList[colIndex]:boolCombo[rowIndex][colIndex]})
        listOfAssignments.append(assignDict)
    
    satsifyingAssignmentsList = []
    for assign in listOfAssignments:
        if expr.evaluate(assign) == True:
            satsifyingAssignmentsList.append(assign)

    #print(satsifyingAssignmentsList)
    return iter(satsifyingAssignmentsList)


    #pass

class KnowledgeBase(object):
    def __init__(self):
        self.kbSet = set()
        #pass
    def get_facts(self):
        return self.kbSet
        #pass
    def tell(self, expr):
        self.kbSet.add(expr.to_cnf())
        #pass
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

print(Or(Atom("a"), Atom("b")) == Or(Atom("b"), Atom("a"))) #should return True

print(Implies(Atom("a"),Atom("b")) == Implies(Atom("a"),Atom("b"))) #should return True

print(Iff(Atom("a"),Atom("b")) == Iff(Atom("a"),Atom("b"))) #should return True
print(Iff(Atom("a"),Atom("b")) == Iff(Atom("b"),Atom("a"))) #should return True
print(Iff(Atom("a"),Atom("b")) == Iff(Atom("b"),Atom("b"))) #should return False


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


print("\n1.4")
e = Implies(Atom("a"), Atom("b"))
print(e.evaluate({"a": False, "b": True})) #should return True
print(e.evaluate({"a": True, "b": False})) #should return False
print("\n")
a, b, c = map(Atom, "abc")
e = And(Not(a), Or(b, c)) #This would be ~a /\ (b \/ c) which is also ~a AND (b OR c)
print(e.evaluate({"a": False, "b": False, "c": True})) #should return True
"""
print(e.evaluate({"a": True, "b": True, "c": True})) #False
print(e.evaluate({"a": True, "b": True, "c": False})) #False
print(e.evaluate({"a": True, "b": False, "c": True})) #False
print(e.evaluate({"a": True, "b": False, "c": False})) #False
print(e.evaluate({"a": False, "b": True, "c": True})) #True
print(e.evaluate({"a": False, "b": True, "c": False})) #True
print(e.evaluate({"a": False, "b": False, "c": False})) #False
"""



print("\n1.5")
e = Implies(Atom("a"), Atom("b"))
a = satisfying_assignments(e)
#print(a)
print(next(a))
print(next(a))
print(next(a))

e = Iff(Iff(Atom("a"), Atom("b")), Atom("c"))
#print(e.evaluate({"a": True, "b": True,"c": False}))
#x = Iff(Atom("a"), Atom("b"))
#print(x.evaluate({"a": True, "b": True}))
print(list(satisfying_assignments(e)))

x = Implies(Atom("a"), Atom("b"))
print(list(satisfying_assignments(x)))
x = Implies(Implies(Atom("a"), Atom("b")), Atom("c"))
print(list(satisfying_assignments(x)))

print("\n1.6")
print(Atom("a").to_cnf())
print()
a, b, c = map(Atom, "abc")
print(Iff(a, Or(b, c)).to_cnf())
print("\n")
print(Or(Atom("a"), Atom("b")).to_cnf())
print("\n")
a, b, c, d = map(Atom, "abcd")
print(Or(And(a, b), And(c, d)).to_cnf())
