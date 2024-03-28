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
        #print(assignment) #in case for some strange reason assignment has more than one key       
        exprFlag = False
        #boolExtract = ""
        #print(self.arg)
        if isinstance(self.arg, Atom) == False:
            exprFlag = True
        
        if isinstance(self.arg, Atom) == True:
            #print(self.arg)
            boolExtract = self.arg.evaluate(assignment)
            if boolExtract == True:
                return False
            if boolExtract == False:
                return True
            #print("boolExtract")
            #print(boolExtract)
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

        """
        valAssignment = assignment
        if isinstance(valAssignment, dict) == False: #checks if valAssignement is a dictionary, if not, extract the dictionary by calling evaluate
            checkAssignment = valAssignment.evaluate() #checkAssignment should return a boolean value, if I'm not mistaken
            #print(checkAssignment)
            #valAssignment = valAssignment.update({realNotKey: checkAssignment}) #update valAssignment so its value is a boolean value
            if checkAssignment == True:
                return False
            else:
                return True
        """

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
        print("got into not")
        if isinstance(self.arg, Not) == True:
            return self.arg
        if isinstance(self.arg, And) == True: #try to just iterate through .disjuncts and apply Not to each one, then add it to a tuple (or a list, I'm not sure) and then put that tuple in the return that I have right now
            notList = []
            for x in self.arg.conjuncts:
                #print(x)
                notList.append(Not(x))
            notTuple = tuple(notList)
            return Or(notTuple)
        if isinstance(self.arg, Or) == True:
            notList = []
            for x in self.arg.disjuncts:
                
                notList.append(Not(x))
            notTuple = tuple(notList)
            return And(notTuple)
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

        #print(len(self.conjuncts))
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
            #print(literal, newBool)
            if newBool == False: #a literal with a value of False was found, return False
                return False

            """
            if isinstance(literal, Atom) == False:
                newBool = literal.evaluate() #evaluating literal should yield a boolean
                if newBool == False:
                    return False
            if isinstance(literal, Atom) == True:
                if assignment.get(literal) == False: #a literal with a value of False was found, return False
                    return False
            """
        #for literal in listAssignment:
            #if assignment.get(literal) == False: #a literal with a value of True was found, return True
                #return False
        #print(self.conjuncts)
        return True #assuming that not a single False was found in the literals

        """
        for literal in self.disjuncts:
            boolList = []
            if isinstance(literal, Atom) == True:
                boolExtract = literal.evaluate(assignment)
                #print("boolExtract")
                #print(boolExtract)
                boolList.extend(boolExtract)
            return boolList
        """
        """
        if exprFlag == False: #all entries are just dictionaries (which makes things easier)
            #andKeys = assignment.keys()
            for literal in assignment:
                if assignment.get(literal) == False: #a literal with a value of False was found, return False
                    return False
            return True #all literals were True, so return True
        """

        #pass
    def to_cnf(self):
        conjunctsList = []
        for literal in self.conjuncts:
            conjunctsList.append(literal.to_cnf())
        return And(tuple(conjunctsList))
        """
        for literal in self.conjuncts:
            if isinstance(literal, And) == True:
                conjunctsList = tuple(self.conjuncts)
                return And(Or(conjunctsList).to_cnf())
        """

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
        #print(f'selfDisjunct: {self.disjuncts}')
        #print(f'other: {other}')
        #if self.disjuncts == other.disjuncts:
        #if isinstance(other, Or) == False:
            #return False
        if self.disjuncts == other: #check this
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
                
                """
                if isinstance(literal, dict) == False: #literal is not a dictionary
                    newBool = literal.evaluate() #evaluating literal should yield a boolean
                    if newBool == True:
                        return True
                if isinstance(literal, dict) == True: #literal is a dictionary
                    if assignment.get(literal) == True: #a literal with a value of True was found, return True
                        return True
                """
            #for literal in listAssignment:
                #if assignment.get(literal) == True: #a literal with a value of True was found, return True
                    #return True
            return False #assuming that not a single True was found in the literals
        
        """
        for literal in self.disjuncts:
            boolList = []
            if isinstance(literal, Atom) == True:
                boolExtract = literal.evaluate(assignment)
                #print("boolExtract")
                #print(boolExtract)
                boolList.extend(boolExtract)
            return boolList
        """

        if exprFlag == False: #all entries are just dictionaries (which makes things easier)
            #andKeys = assignment.keys()
            for literal in assignment:
                if assignment.get(literal) == True: #a literal with a value of True was found, return True
                    return True
            return False #all literals were False, so return False
        #pass
    def to_cnf(self):
        #print("or rightnow")
        
        for literal in self.disjuncts: #checks for any And that is inside Or, does distributivity of Or over And if true
            if isinstance(literal, And) == True:
                #print("in or right now")
                disjunctsList = tuple(self.disjuncts)
                return And(Or(disjunctsList).to_cnf()) #this probably isn't right, but it's the only thing I can think of doing right now.
        
        #self.disjuncts is a frozen set, so I need to convert it to something else before changing it
        copyDisjuncts = list(self.disjuncts)
        #print(copyDisjuncts)

        
        for literal in copyDisjuncts: #checks for any Or that is inside Or, simplifies to take out the Or            
            if isinstance(literal, Or) == True:
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
                #print("changedsomething")
                #print(copyDisjuncts)
                
                #disjunctsList = list(self.disjuncts)
                #literal = tuple(orLiteralList) #disjunctsList.extend(list(literal.disjuncts))
                #literal = "crap"
                #copyDisjuncts[literal] = "crap"
                #print(literal)
                #return tuple(disjunctsList)
            #print(literal)
            #print(copyDisjuncts)
        #print(copyDisjuncts)
        return Or(tuple(copyDisjuncts))
        

        #for literal in copyDisjuncts: #checks for any Or that is inside Or, simplifies to take out the Or
        """
        for literal in range(0, len(copyDisjuncts)):
            if isinstance(copyDisjuncts[literal], Or) == True:
                print("in or of ORs right now")
                #print(self.disjuncts)
                #print(copyDisjuncts[literal])
                orLiteralList = []
                for orLiterals in copyDisjuncts[literal].disjuncts:
                    orLiteralList.append(orLiterals)
                #disjunctsList = list(self.disjuncts)
                #literal = tuple(orLiteralList) #disjunctsList.extend(list(literal.disjuncts))
                copyDisjuncts[literal] = tuple(orLiteralList)
                #copyDisjuncts[literal] = "crap"
                #print(literal)
                #return tuple(disjunctsList)
            #print(copyDisjuncts[literal])
            #print(copyDisjuncts)
        """
        #print(copyDisjuncts)
        return Or(tuple(copyDisjuncts))

        reverseTuple = list(self.disjuncts)
        reverseTuple.reverse()
        reverseTuple = tuple(reverseTuple)
        #return reverseTuple
        return Or(reverseTuple) #might want to check this
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

        """
        for literal in assignment: #go through the assignment dictionary and check if there are any expressions instead of dictionaries, if there are, set the exprFlag to True
            if isinstance(literal, dict) == False:
                exprFlag == True
        """

        """
        if isinstance(self.left, Atom) == True or isinstance(self.right, Atom) == True:
            boolLeft = self.left.evaluate(assignment)
            boolRight = self.right.evaluate(assignment)
            return [boolLeft, boolRight]
        """

        """
        if exprFlag == False:
            #impKeys = assignment.keys()
            #impKeys = list(impKeys)
            #if assignment.get(impKeys[0]) == True and assignment.get(impKeys[1]) == False:
            print(assignment)
            print(assignment.get(self.left))
            print(assignment.get(self.right))
            if assignment.get(self.left) == True and assignment.get(self.right) == False:
                return False
            else:
                return True
        """
        

        """
        trueFlag = False
        counter = 1

        for literal in assignment: #iterate through all the keys in assignment (which is just a dictionary)
            #first of all, there should only be two keys in assignment, so in this case, the only thing 
            # that matters is if the first key is True and the second key is False, so just check for that.
            
            valueLiteral = literal
            if isinstance(literal, dict) == False: #checks if literal is a dictionary, if not, extract the dictionary by calling evaluate
                valueLiteral = literal.evaluate()
            
            #at this point, valueLiteral should be a dictionary, if not, something's wrong with the previous check
            #print(valueLiteral)

            if counter == 1:
                if assignment.get(valueLiteral) == True:
                    trueFlag = True
            if counter == 2: #indicates that the second literal is being checked
                if trueFlag == True: #first literal was True
                    if assignment.get(valueLiteral) == False:
                        return False #second literal turns out ot be False
                    else: #the second literal turns out to be True
                        return True
                else: #first literal was False
                    return True
            counter = 2 #indicates that the first literal has finished checking, the next iteration will check the second literal
        """
        #pass
    def to_cnf(self):
        #print("asdfasdf")
        #print(self.left)
        #print(self.left.to_cnf())
        #print(self.right)
        #print(self.right.to_cnf())
        #return Or(Not(self.left).to_cnf(), self.right.to_cnf())
        
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

        """
        if isinstance(self.left, Atom) == True or isinstance(self.right, Atom) == True:
            boolLeft = self.left.evaluate(assignment)
            boolRight = self.right.evaluate(assignment)
            return [boolLeft, boolRight]
        """
        """
        if exprFlag == False:
            iffKeys = assignment.keys()
            iffKeys = list(iffKeys)

            if assignment.get(iffKeys[0]) == True and assignment.get(iffKeys[1]) == True:
                return True
            if assignment.get(iffKeys[0]) == False and assignment.get(iffKeys[1]) == False:
                return True
            return False
        """
        #pass
    def to_cnf(self):
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

    """
    extractLen = 4
    bools = [True, False]
    for x in range(extractLen + 1):
        for subset in itertools.combinations(bools, x):
            print(subset)
    """

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
a, b, c = map(Atom, "abc")
print(Iff(a, Or(b, c)).to_cnf())
print(Or(Atom("a"), Atom("b")).to_cnf())
a, b, c, d = map(Atom, "abcd")
print(Or(And(a, b), And(c, d)).to_cnf())
