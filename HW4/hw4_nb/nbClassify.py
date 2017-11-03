'''Loads test data and determines category of each test.  Assumes
train/test data with one text-document per line.  First item of each
line is category; remaining items are space-delimited words.

Author: Your name here

Date: XX.Oct.2017

Do I need to use python 2 or 3?
What kind of terminal commands should I incorporate?
Do I just use the Naieve Bayes probability equation for version 1?
How do we attach weights? By just muliplying by a coefficient?
For which part did you want us to use a dictionary?
How is argmax supposed to work?


'''
from __future__ import print_function
import sys
import math

class NaiveBayes():
    '''Naive Bayes classifier for text data.
    Assumes input text is one text sample per line.
    First word is classification, a string.
    Remainder of line is space-delimited text.
    '''

    def __init__(self,train):
        '''Create classifier using train, the name of an input
        training file.
        '''
        self.dict = {}
        self.learn(train) # loads train data, fills prob. table
        self.vocSize = len(self.vocab) # unique words in vocab

    def learn(self,traindat):
        '''Load data for training; adding to
        dictionary of classes and counting words.'''
        with open(traindat,'r') as fd:
            for line in fd.readlines():
                id, *word = line.split()
                print(word)



def argmax(lst):
    return lst.index(max(lst))

def main():
    if len(sys.argv) != 3:
        print("Usage: %s trainfile testfile" % sys.argv[0])
        sys.exit(-1)

    nbclassifier = NaiveBayes(sys.argv[1])
    nbclassifier.printClasses()
    nbclassifier.runTest(sys.argv[2])

if __name__ == "__main__":
    main()
