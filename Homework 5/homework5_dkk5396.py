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
import email.policy
from email.policy import default
import math

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
        emailTokenList = load_tokens(path)
        fullTokenList.extend(emailTokenList)
    fullTokenSet = set(fullTokenList)
    sigmaCount = len(fullTokenList)       #this is the value of Sigma count(w')
    fullCount = len(fullTokenSet)       #this is the value of |V|
    #print(sigmaCount)
    #print(fullCount)

    #from here, I should iterate through emailTokenList and run the Laplace probabilities and put the results in a dictionary (if the key is not already in the dictionary, I think)
    # Ok, so after talking to some people, count(w) is just the number of occurances of a single word, which I already knew.
    # But |V| is the count of all unique words, while Sigma count(w') is just the length of the entire list (or in other words, the count of EVERY word, whether it's unique or not).
    # And a (which is really alpha) is just the smoothing var.
    #for token in fullTokenList:
    sumCount = 0
    for token in fullTokenSet: #if this doesn't work well, use fullTokenList
        tokenCount = fullTokenList.count(token) #this is the value of count(w)
        #print(token)
        calcProb = (tokenCount + smoothing) / (sigmaCount + (smoothing * (fullCount + 1))) #this is the equation for P(w)        
        #print(calcProb)
        sumCount = sumCount + calcProb
        calcProb = math.log(calcProb)
        #print(f'calcProb: {calcProb}')
        probDict.update({token: calcProb})
    #print(sum(probDict.values()))
    #print(sumCount)
    calcUNK = smoothing / (sigmaCount + (smoothing * (fullCount + 1)))                     #this is the equation for P(<UNK>)
    sumCount = sumCount + calcUNK
    #print(sumCount)
    calcUNK = math.log(calcUNK)
    
    probDict.update({"<UNK>": calcUNK})
    return probDict
    #pass

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        pass
    
    def is_spam(self, email_path):
        pass

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
