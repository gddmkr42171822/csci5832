'''
Robert Werthman

Naive-Bayes with add one smoothing
P(word|-) = (count of the word in negative reviews class + 1)/
            (count of all words in negative reviews class + number of words in entire vocabulary of training set) 
P(review|-) = probability of each of the words being negative multiplied together
'''
import re

def wordCount(file):
    '''
    Return a dictionary of the word counts in a file
    '''
    d = {}
    f = open(file, 'r')
    for line in f:
        # Remove end of punctuation
        line = re.sub('[.,!?]', '', line)
        # Make everything lowercase
        line = line.lower()
        # Split words on spaces in the line
        line = line.split()
        # Remove the ID-.... from the line
        line = line[1:]
        # Create a dictionary with key being the word and value being the count
        for word in line:
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
    return d        





def main():
    posWords = wordCount('hotelPosT-train.txt')
    negWords = wordCount('hoteNegT-train.txt')

if __name__ == '__main__':
    main()