############################################################
# CMPSC442: Classification
############################################################

student_name = "David Kim"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import email.iterators
#import email.policy
import math
import os, os.path
#import collections
from collections import Counter

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    tokenList = []
    #policy = email.policy.EmailPolicy(utf8=True)

    openMessage = open(email_path, encoding="utf8") #without this, none of the other email methods work. Would've been good to know beforehand.
    emailMessage = email.message_from_file(openMessage) 

    for part in email.iterators.body_line_iterator(emailMessage): #traverses the message line by line, and each line is an str
        line = part.split() #part is an str, so it can be split into a list
        tokenList.extend(line)
    return tokenList
    #pass

def log_probs(email_paths, smoothing):
    #need to build a dictionary and fill the values with calculations
    #floatSmoothing = float(smoothing) #converts string for smoothing into a float, if it is not already a float
    probDict = {}
    fullTokenList = []
    for path in email_paths:
        #print(f'path: {path}')
        emailTokenList = load_tokens(path)
        fullTokenList.extend(emailTokenList)
    fullTokenSet = set(fullTokenList)
    sigmaCount = len(fullTokenList)     #this is the value of Sigma count(w')
    fullCount = len(fullTokenSet)       #this is the value of |V|
    #print(sigmaCount)
    #print(fullCount)

    #from here, I should iterate through emailTokenList and run the Laplace probabilities and put the results in a dictionary (if the key is not already in the dictionary, I think)
    # Ok, so count(w) is just the number of occurances of a single word, which I already knew.
    # But |V| is the count of all unique words, while Sigma count(w') is just the length of the entire list (or in other words, the count of EVERY word, whether it's unique or not).
    # And a (which is really alpha) is just the smoothing var.
    #for token in fullTokenList:
    sumCount = 0
    #print(len(fullTokenSet))

    fastCount = Counter()
    fastCount.update(fullTokenList)
    #print(type(fastCount))
    fastCount = dict(fastCount)
    #print(type(fastCount))

    for token in fastCount:
        tokenCount = fastCount.get(token)
        calcProb = (tokenCount + smoothing) / (sigmaCount + (smoothing * (fullCount + 1)))
        calcProb = math.log(calcProb)
        probDict.update({token: calcProb})

    #old code before I learned how to use Counter() for a faster count(w)
    """
    for token in fullTokenSet: #if this doesn't work well, use fullTokenList
        #print(token)
        tokenCount = fullTokenList.count(token) #this is the value of count(w)
        #print(token)
        calcProb = (tokenCount + smoothing) / (sigmaCount + (smoothing * (fullCount + 1))) #this is the equation for P(w)        
        #print(calcProb)
        sumCount = sumCount + calcProb
        calcProb = math.log(calcProb)
        #print(f'calcProb: {calcProb}')
        probDict.update({token: calcProb})
    """
    #print(sum(probDict.values()))
    #print(sumCount)
    calcUNK = smoothing / (sigmaCount + (smoothing * (fullCount + 1)))                     #this is the equation for P(<UNK>)
    sumCount = sumCount + calcUNK
    #print(sumCount)
    calcUNK = math.log(calcUNK)
    
    probDict.update({"<UNK>": calcUNK})
    return probDict
    #pass

def countFilesInDir(dir): #counts the number of files in a directory, and returns the number
    return len(os.listdir(dir))
    #return len([name for name in os.listdir('.') if os.path.isfile(name)])

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spamDirList = [spam_dir + "/" + directory for directory in os.listdir(spam_dir)]
        hamDirList = [ham_dir + "/" + directory for directory in os.listdir(ham_dir)]
        self.spamDict = log_probs(spamDirList, smoothing)
        self.hamDict = log_probs(hamDirList, smoothing)
        spamCount = countFilesInDir(spam_dir)
        hamCount = countFilesInDir(ham_dir)

        spamSum = sum(self.spamDict.values())
        hamSum = sum(self.hamDict.values())
        #for x in self.spamDict:
            #spamSum = spamSum + self.spamDict[x]
        #for x in self.hamDict:
            #hamSum = hamSum + self.hamDict[x]
        
        #calcSpamProb = spamSum / spamCount
        #calcHamProb = hamSum / hamCount

        calcSpamProb = float(spamSum) / (spamCount + hamCount)
        calcHamProb = float(hamSum) / (spamCount + hamCount)

        """
        #calcSpamProb = (spamCount + smoothing) / ((spamCount + hamCount) + (smoothing * (spamCount + 1)))
        #calcHamProb = (hamCount + smoothing) / ((spamCount + hamCount) + (smoothing * (hamCount + 1)))
        
        #calcSpamProb = (spamCount + smoothing) / ((spamCount + hamCount) + spamCount)
        #calcHamProb = (hamCount + smoothing) / ((spamCount + hamCount) + hamCount)
        """

        self.spamProb = calcSpamProb
        self.hamProb = calcHamProb
        #pass
    
    def is_spam(self, email_path):
        #spamProbDict = {}
        spamCount = 0
        hamCount = 0
        freqDict = {}
        fullTokenList = []
        """
        for path in email_path:
            #print(f'spampath: {path}')
            emailTokenList = load_tokens(path)
            fullTokenList.extend(emailTokenList)
        """
        fullTokenList = load_tokens(email_path)
        fullTokenSet = set(fullTokenList)

        for token in fullTokenSet: #if this doesn't work well, use fullTokenList
            tokenCount = fullTokenList.count(token) #this is the value of count(w)
            freqDict.update({token: tokenCount})
        #for token in load_tokens(email_path):
        fullCount = len(fullTokenSet) #this is the value of |V|
        for key in freqDict.keys():
            if key in self.spamDict:
                spamCount = spamCount + self.spamDict[key] * freqDict[key]
            else:
                spamCount = spamCount + self.spamDict["<UNK>"] * freqDict[key]
            if key in self.hamDict:
                hamCount = hamCount + self.hamDict[key] * freqDict[key]
            else:
                hamCount = hamCount + self.hamDict["<UNK>"] * freqDict[key]
        
        spamProbCalc = self.spamProb * spamCount
        hamProbCalc = self.hamProb * hamCount
        print(f'spamProbCalc:{spamProbCalc}')
        print(f'hamProbCalc:{hamProbCalc}')
        #if spamProbCalc > hamProbCalc:
            #return True
        #else:
            #return False
        return spamProbCalc > hamProbCalc #figure this out, probably need to use log space calculations, there might be underflow here

        #pass

    def most_indicative_spam(self, n):
        pass

    def most_indicative_ham(self, n):
        pass



#####################################################
# Test Cases
#####################################################

print("Question 1\n")

ham_dir = "homework5_data/train/ham/"
print(load_tokens(ham_dir+"ham1")[200:204])
#print(load_tokens(ham_dir+"ham1"))
print(load_tokens(ham_dir+"ham2")[110:114])
spam_dir = "homework5_data/train/spam/"
print(load_tokens(spam_dir+"spam1")[1:5])
print(load_tokens(spam_dir+"spam2")[:4])

print("\nQuestion 2\n")

paths = ["homework5_data/train/ham/ham%d" % i for i in range(1, 11)]
p = log_probs(paths, 1e-5)
print(p["the"])
print(p["line"])


print("")
paths = ["homework5_data/train/spam/spam%d" % i for i in range(1, 11)]
p = log_probs(paths, 1e-5)
print(p["Credit"])
print(p["<UNK>"])

print("\nQuestion 4\n")
sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
print(sf.is_spam("homework5_data/train/spam/spam1"))
print(sf.is_spam("homework5_data/train/spam/spam2"))

sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham",  1e-5)
print(sf.is_spam("homework5_data/train/ham/ham1"))
print(sf.is_spam("homework5_data/train/ham/ham2"))