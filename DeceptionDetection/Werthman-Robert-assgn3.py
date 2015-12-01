'''
Robert Werthman
CSCI 5832
HW3 Deception Detection
'''
import re
import math
import random
import sys
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron

inc = open('incorrect-answers.txt', 'w')
def checkOutput(outputFile, answerFile):
    wrongReviews = 0
    answers = {}
    output = {}
    # Read in the IDs and tags from the correct answers file
    f = open(answerFile, 'r')
    for line in f:
        line = line.strip().split('\t')
        answers[line[0]] = line[1]
    f.close()
    # Read in the IDs and tags from the output generated by naive bayes
    f = open(outputFile)
    for line in f:
        line = line.strip().split('\t')
        output[line[0]] = line[1]
    f.close()
    # Check if each ID has the correct sentiment tag
    for key in output:
        if key in answers:
            if output[key] == answers[key]:
                pass
                #print "{0} is correct.".format(key)
            else:
                inc.write('{0} output {1} answer {2}\n'.format(key, output[key], answers[key]))
                wrongReviews += 1
                #print '{0} output {1} answer {2}'.format(key, output[key], answers[key])
                #print "{0} is incorrect.".format(key)
    #print 'Number of wrong IDs: {0}'.format(wrongReviews)
    return wrongReviews


VerbCounts = []
NounCounts = []
def wordCount(file):
    '''
    Return a dictionary of the word counts in a file
    '''
    d = {}
    f = open(file, 'r')
    for line in f:
        # Remove end of punctuation
        line = re.sub('[.,!?():;]', '', line)
        # Make everything lowercase
        line = line.lower()
        # Split words on spaces in the line
        line = line.strip().split()
        # Remove the ID-.... from the line
        line = line[1:]    
        # Create a dictionary with the key being the word and the value being the count
        for word in line:
            #word = stem(word)
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
        line = re.sub('[.,!?():;]', '', line)
         # Make everything lowercase
        line = line.lower()
        # Split words on spaces in the line
        line = line.split()
        # Put review ID in the dictionary as key and rest of the words of the review as value
        d[line[0]] = line[1:]
    f.close()
    #d = stemReviews(d)
    return d

def stemReviews(d):
    for key in d:
        review = d[key]
        stemmedReview = [stem(word) for word in review]
        d[key] = stemmedReview
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
            #print word
        else:
            freqOfWordInClass = 0
        probabilityOfWord = ((freqOfWordInClass+1)*1.0)/((totalCountOfWordsInClass+len(vocabulary))*1.0)
        listOfProbabilities.append(math.log(probabilityOfWord))
    return listOfProbabilities
        
    
def copyFile(inputFile, outputFile):
    # Open the files
    input = open(inputFile, 'r')
    output = open(outputFile, 'w')
    # Read in the lines from the input file
    lines = input.readlines()
    # Write out the lines from the input file to the output file
    output.writelines(lines)
    # Close the files
    input.close()
    output.close()

def readFileIntoList(inputFile):
    f = open(inputFile, 'r')
    lines = f.readlines()
    f.close()
    return lines

def writeListToFile(outputFile, list, append):
    if append:
        f = open(outputFile, 'a')
    else:
        f = open(outputFile, 'w')
    f.writelines(list)
    f.close()

def createCrossValidationFiles(n):
    # Make copies of the original positive and negative review files
    copyFile('hotelT-train.txt', 'truetrain-reviews.txt')
    copyFile('hotelF-train.txt', 'falsetrain-reviews.txt')
    
    # Read the positive and negative reviews into two separate lists
    trueReviews = readFileIntoList('truetrain-reviews.txt')
    falseReviews = readFileIntoList('falsetrain-reviews.txt')    
    
    # Use n random reviews for the positive review test set
    # Use the remaining reviews for the positive training set
    testTrueReviews = random.sample(trueReviews, n)
    trainingTrueReviews = [review for review in trueReviews if review not in testTrueReviews]
    
    # Use n random reviews for the negative review test set
    # Use the remaining reviews for the negative training set
    testFalseReviews = random.sample(falseReviews, n)
    trainingFalseReviews = [review for review in falseReviews if review not in testFalseReviews]
    
    # Write the test reviews to the test set file
    writeListToFile('test-reviews.txt', testTrueReviews, False)
    writeListToFile('test-reviews.txt', testFalseReviews, True)
    
    # Write the training reviews to the training set file
    writeListToFile('truetrain-reviews.txt', trainingTrueReviews, False)
    writeListToFile('falsetrain-reviews.txt', trainingFalseReviews, False) 
    
def ScikitClassify():
    # Read in the test and training reviews
    t = gatherReviews('truetrain-reviews.txt')
    f = gatherReviews('falsetrain-reviews.txt')
    test = gatherReviews('test-reviews.txt')
    # Create lists of strings from those reviews instead
    # of lists of words
    testReviews = test.values()
    testIDs = test.keys()
    testIDs = [x.upper() for x in testIDs]
    t = t.values()
    f = f.values()
    tstrings = []
    fstrings = []
    docs_test = []
    for review in t:
        review = ' '.join(review)
        tstrings.append(review)
    for review in f:
        review = ' '.join(review)
        fstrings.append(review)
    for review in testReviews:
        review = ' '.join(review)
        docs_test.append(review)   
    # Encoding T as 1 and F as 0 for each review
    tTargets = len(tstrings)*[1]
    fTargets = len(fstrings)*[0]
    # Creating a giant list of the reviews as strings
    reviews = tstrings+fstrings
    # Creating a giant list of the encoded review labels
    targets = tTargets+fTargets
    
    # Creating vector out of the training and test reviews
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(reviews)
    X_test = vectorizer.transform(docs_test)
    
    # Extracting the features with a chi-squared test
    ch2 = SelectKBest(chi2)
    X_train = ch2.fit_transform(X_train, targets)
    X_test = ch2.transform(X_test)
    
    # Fitting the reviews and features to a classifier
    #clf = LinearSVC()
    #clf = SGDClassifier()  
    #clf = Perceptron() 
    clf = PassiveAggressiveClassifier()
    clf.fit(X_train, targets)

    # Running the classifier on the test set
    # and returning the predicted encoded labels for each 
    # test review
    results = clf.predict(X_test)  
    
    # Output the results
    f = open('werthman-robert-assgn3-out.txt', 'w')
    for id,result in zip(testIDs,results):
        if result == 1:
            f.write('{0}\tT\n'.format(id))
        elif result == 0:
            f.write('{0}\tF\n'.format(id))
    f.close()  

def NaiveBayesClassify():
    # Create a dictionary with all the words in the true review set
    trueWords = wordCount('truetrain-reviews.txt')
    # Create a dictionary with all the words in the false review set
    falseWords = wordCount('falsetrain-reviews.txt')
    # Create a dictionary of all the words in the training set
    vocabulary = trueWords.copy()
    vocabulary.update(falseWords)
    # Create an output file for the sentiment analysis of the reviews
    f = open('werthman-robert-assgn3-out.txt', 'w')
    # Check if the reviews are true or false
    reviews = gatherReviews('test-reviews.txt')
    for review in reviews:
        # Get a list of the log of the probabilities for each word in the review
        # for each sentiment class
        falseProb = probabilityOfClass(falseWords, reviews[review], vocabulary)
        trueProb = probabilityOfClass(trueWords, reviews[review], vocabulary)
        # Add the list of probabilities together for each class
        falseProb = reduce(lambda x,y: x+y, falseProb)
        trueProb = reduce(lambda x,y: x+y, trueProb)
        # Evaluate the sentiment of each review by comparing the probabilities of each class
        # for that review
        if trueProb > falseProb:
            f.write('{0}\tT\n'.format(review.upper()))
        elif falseProb > trueProb:
            f.write('{0}\tF\n'.format(review.upper()))
    f.close()    

def main():
    wrongReviews = 0.0
    n = 10
    x = 100
    for i in range(0,x):
        createCrossValidationFiles(n)
        #ScikitClassify()
        NaiveBayesClassify()
        wrongReviews += checkOutput('werthman-robert-assgn3-out.txt','answers.txt') 
    totalTestReviews = (n+n)*x
    numCorrectReviews = totalTestReviews-wrongReviews
    print '{0} wrongly labeled reviews out of {1} total test reviews.'.format(wrongReviews, totalTestReviews)
    print 'Percent correct {0}'.format((numCorrectReviews/totalTestReviews)*100.0)
    # Close incorrect output file
    inc.close() 

if __name__ == '__main__':
    main()