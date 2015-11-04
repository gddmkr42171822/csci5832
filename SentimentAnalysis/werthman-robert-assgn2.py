'''
Robert Werthman

Naive-Bayes with add one smoothing
P(word|-) = (frequency of the word in negative reviews class + 1)/
            (total count of all words in negative reviews class + number of words in entire vocabulary of training set (V)) 
P(review|-) = probability of each of the words being negative multiplied together
'''
import re
import math

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
        # Create a dictionary with the key being the word and the value being the count
        for word in line:
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
    f.close()
    return d        

def gatherReviews(file):
    '''
    Return a dictionary of the reviews in a file
    '''
    d = {}
    f = open(file,'r')
    for line in f:
        # Remove end of punctuation
        line = re.sub('[.,!?]', '', line)
         # Make everything lowercase
        line = line.lower()
        # Split words on spaces in the line
        line = line.split()
        # Put review ID in the dictionary as key and rest of the words of the review as value
        d[line[0]] = line[1:]
    f.close()
    return d

def probabilityOfClass(reviewClass,review,vocabulary):
    '''
    Returns a list of probabilities for each word in a review given a class
    '''
    listOfProbabilities = []
    # Add up all the words in a review class
    totalCountOfWordsInClass = 0
    for word in reviewClass:
        totalCountOfWordsInClass += reviewClass[word]
    # Calculate the probability of each word given a review class
    for word in review:
        freqOfWordInClass = 0
        if word in reviewClass:
            freqOfWordInClass = reviewClass[word]
        else:
            freqOfWordInClass = 0
        probabilityOfWord = ((freqOfWordInClass+1)*1.0)/((totalCountOfWordsInClass+len(vocabulary))*1.0)
        listOfProbabilities.append(math.log(probabilityOfWord))
    return listOfProbabilities
        
    
    



def main():
    # Create a dictionary with all the words in the positive review set
    posWords = wordCount('hotelPosT-train.txt')
    # Create a dictionary with all the words in the negative review set
    negWords = wordCount('hoteNegT-train.txt')
    # Create a dictionary of all the words in the training set
    vocabulary = posWords.copy()
    vocabulary.update(negWords)
    # Retrieve the reviews from a file and add them in a dictionary with the review ID as the key
    reviews = gatherReviews('hotelPosT-train.txt')
    #reviews = gatherReviews('hoteNegT-train.txt')
    # Check if the reviews are positive or negative
    line = 1
    for review in reviews:
        negProb = probabilityOfClass(negWords, reviews[review], vocabulary)
        posProb = probabilityOfClass(posWords, reviews[review], vocabulary)
        negProb = reduce(lambda x,y: x+y, negProb)
        posProb = reduce(lambda x,y: x+y, posProb)
        if posProb > negProb:
            print "{0}. {1}\tPOS".format(line,review)
        elif posProb < negProb:
            print "{0}. {1}\tNEG".format(line,review)
        line += 1
    

if __name__ == '__main__':
    main()