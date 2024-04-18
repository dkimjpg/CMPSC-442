############################################################
# CMPSC 442: Hidden Markov Models
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.



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

class Tagger(object):

    def __init__(self, sentences):
        pass

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