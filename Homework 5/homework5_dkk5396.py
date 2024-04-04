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

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    tokenList = []

    openMessage = open(email_path, 'r') #without this, none of the other email methods work. Would've been good to know beforehand.
    emailMessage = email.message_from_file(openMessage) 

    for part in email.iterators.body_line_iterator(emailMessage): #traverses the message line by line, and each line is an str
        line = part.split() #part is an str, so it can be split into a list
        tokenList.extend(line)
    return tokenList
    #pass

def log_probs(email_paths, smoothing):
    #need to build a dictionary and fill the values with calculations
    probDict = {}
    for path in email_paths:
        emailTokenList = load_tokens(path)
        #from here, I should iterate through emailTokenList and run the Laplace probabilities and put the results in a dictionary (if the key is not already in the dictionary, I think)
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

ham_dir = "homework5_data/train/ham/"
print(load_tokens(ham_dir+"ham1")[200:204])
#print(load_tokens(ham_dir+"ham1"))
print(load_tokens(ham_dir+"ham2")[110:114])
spam_dir = "homework5_data/train/spam/"
print(load_tokens(spam_dir+"spam1")[1:5])
print(load_tokens(spam_dir+"spam2")[:4])