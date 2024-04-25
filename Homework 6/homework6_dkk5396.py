############################################################
# CMPSC 442: Hidden Markov Models
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import collections

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    openMessage = open(path) #, encoding="utf8")
    corpusList = []
    for line in openMessage.readlines():
        currentList = []
        currentLine = line.split() #split by whitespace, since that's what each entry is separated by
        for part in currentLine:
            partList = part.split("=")
            currentList.append(partList)
        corpusList.append(currentList)
    #print(corpusList)
    return(corpusList)
    #pass

#def getTokens():

def extractTag(line, position):
    tag = line[position].split("=")
    tagExtraction = tag[1]
    return tagExtraction

def extractToken(line, position):
    token = line[position].split("=")
    tokenExtraction = token[1]
    return tokenExtraction


TAGS = ('NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET', 'ADP', 'NUM', 'CONJ', 'PRT', '.', 'X')

class Tagger(object):

    def __init__(self, sentences):
        smoothingProb = 1e-10
        self.pi = {}
        self.alpha = {}
        self.beta = {}

        #filling all the dictionaries with 0's
        for tag in TAGS:
            self.pi[tag] = 0
            self.alpha[tag] = {}
            for innerTag in TAGS:
                self.alpha[tag][innerTag] = 0
            self.beta[tag] = collections.defaultdict(int) #beta needs a default dict since each tag in beta will be a dictionary with all keys initially set to 0

        #begin counting for pi, alpha, and beta
        for line in sentences:
            #pi counting
            getFirstTag = extractTag(line, 0)
            self.pi[getFirstTag] += 1
            #extractTag = line[0].split("=")
            #extractTag = extractTag[1]
            #self.pi[extractTag] += 1

            #beta counting for first element in line (this is necessary because the for loop after this skips the first element)
            getFirstToken = extractToken(line, 0)
            self.beta[getFirstTag][getFirstToken] += 1

            #alpha counting and beta counting

            #Extra Note: I might have to use Counter() for alpha and beta counting if my implementation is not fast enough. 
            for currentToken in range(1, len(line)):
                #alpha counting
                #extractTag = line[currentToken]
                getTag = extractTag(line, currentToken)
                getPreviousTag = extractTag(line, currentToken - 1)
                self.alpha[getPreviousTag][getTag] += 1

                #beta counting
                getToken = extractToken(line, currentToken)
                self.beta[getTag][getToken] += 1

                """
                #Use the following if what I used doesn't work
                for (token, tag) in sentence:
                self.b[tag][token] += 1
                """
            
        #pi smoothing
        #finds total for pi based on pi counting
        piTotal = sum(self.pi.values()) + (smoothingProb * len(self.pi.keys())) #may or may not need to add 1 to the len(self.pi,keys()) since this is Laplace smoothing
        #Use the piTotal calculation below if my implemntation doesn't work
        #piTotal = 0
        #for tag in TAGS:
            #piTotal = self.pi[tag] + smoothingProb
        
        #applies smoothing
        for tag in TAGS:
            self.pi[tag] = float(float(self.pi[tag] + smoothingProb) / piTotal)
        
        #alpha smoothing
        #alphaTotal = sum(self.alpha.values()) + (smoothingProb * len(self.pi.keys())) #don't use this, I think I need to use some sort of dictionary comprehension if I want this to work properly
        #alphaTotal = 0
        for tag in TAGS:
            #finds total for alpha based on alpha counting
            alphaTotal = 0
            if self.alpha[tag]: #checks if the value for self.alpha[tag] is not empty, or in other words, looks like {}
                alphaTotal = alphaTotal + sum(self.alpha[tag].values()) + (smoothingProb * len(self.alpha[tag].keys())) #assuming that each dictionary entry has a dictionary within it
            #alphaTotal = alphaTotal + alphaDictTotal
            
            #applies smoothing
            for innerTag in TAGS:
                self.alpha[tag][innerTag] = float(float(self.alpha[tag][innerTag] + smoothingProb) / alphaTotal)
        
        #beta smoothing
        for tag in TAGS:
            #finds total for beta based on beta counting
            betaTotal = smoothingProb
            if self.beta[tag]:
                betaTotal = sum(self.beta[tag].values())
            
            #applies smoothing
            for token in self.beta[tag]:
                self.beta[tag][token] = float(float(self.beta[tag][token] + smoothingProb) / betaTotal)

        #pass

    def most_probable_tags(self, tokens):
        pass

    def viterbi_tags(self, tokens):
        pass


#####################################################
# Test Cases
#####################################################

print("Question 1\n")
c = load_corpus("brown-corpus.txt")
print(c[1402]) #offset: 2806
print()
print(c[1799]) #offset: 3600

print("\nQuestion 2\n")