'''
Created on Sep 9, 2015

@author: Bob

Pseudocode
------------

Part 1
-------

Script should take in two arguments: the path to the word list and the path for the hashtag list
(the absolute path needs to be found, not dependent on the os)

Step 1: Read in list of words (read in a maximum of 75000 words) and hashtags
read in a file line by line and find the first alphanumeric word on each line
store each word in a dictionary

Recursive step?
Step 3: break up hashtag in mulitple words using MaxMatch algorithm
find largest word in hashtag from list of words
append it to a string or write it a file without a newline 
repeat until at the end the hashtag
output to file or add newline and move to next line in output file

'''

import re
import sys
import os



def readWordsFromFile(filePath):
    '''
    '''
    wordset = set()
    #create a regular expression to match the first word in a line of the file
    pattern = re.compile('[a-zA-Z]+')
    #read the file into memory
    with open(filePath, 'r') as f:
        #go through the file line by line and get the first word out of each line
        for line in f:
            match = re.search(pattern, line)
            if match:
                wordset.add(match.group(0))
    return wordset

def maxMatch(hashtag, wordlist, maxmatchedHashtag):
    '''
    '''
    substringList = []
    largestWord = ""
    #go through each word in the wordlist
    for word in wordlist:
        #make a list of the words from the word list that are
        #in the hashtag 
        if word in hashtag[0:len(word)]:
            substringList.append(word)
    #if the list is not empty then get the largest word out of the substring list, remove it from the hashtag,
    #and call the max match algorithm again on the new hashtag 
    if len(substringList) != 0:
        #find largest string in the substring list
        substringList.sort(key=len, reverse=True)
        largestWord = substringList[0]
        #if there are still characters after the largest word is found 
        #look through the word list again for the next largest word
        if len(largestWord) < len(hashtag):
            maxmatchedHashtag = maxmatchedHashtag + largestWord + " "
            #return is necessary otherwise maxmatchedHashtag is discarded
            return maxMatch(hashtag[len(largestWord):len(hashtag)], wordlist, maxmatchedHashtag)
        #if the largest word is at the end of the hashtag
        #write it out to the output file and end MaxMatch for that hashtag
        elif len(largestWord) == len(hashtag):
            return (maxmatchedHashtag + largestWord)
        else:
            #this is for the largest word being longer than the hashtag
            #which should never happen
            print("Error: this maxMatch function statement should never be reached")
    else:
        #if the list is empty then there are no more words in the word list that fit into the hashtag
        #take the rest of the hash tag and add it to the maxmatchHashtag and return it
        return (maxmatchedHashtag + hashtag)
 

def checkCommandLineArgs(): 
    '''
    ''' 
    #check the user gave the right number of arguments
    #if not print what the user should have given and then exit  
    if len(sys.argv) < 3:
        print("Usage: werthman-assgn1.py <absolute path to file of word list> <absolute path to file of hashtags>")
        sys.exit()
    else:
        #check if the user gave the absolute path for both files otherwise print script usage and exit
        if os.path.isabs(sys.argv[1]) == False and os.path.isabs(sys.argv[2]) == False:
            print("Usage: werthman-assgn1.py <absolute path to file of word list> <absolute path to file of hashtags>")
            sys.exit()
        else:
            #if the user gave the right number of arguments and both absolute paths return them
            return (sys.argv[1], sys.argv[2])     

      
def assertion(boolean, testName):
    if boolean:
        print(testName + " PASSED")
    else:
        print(testName + " FAILED")

def testSetContents(setOfStrings, testList):   
    for string in testList:  
        assertion(string in setOfStrings, "Set contains {0}.".format(string))
    
def testMaxMatchAlgo(hashtagSet, wordlistSet):
    for hashtag in hashtagSet:
        maxmatchedHashtag = ""
        if hashtag == "manoverthemoon":
            #test for the hashtag being made up of entirely of words in the word list
            maxmatchedHashtag = maxMatch("manoverthemoon", wordlistSet, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "man over the moon", "manoverthemoon should be changed to man over the moon.")
        elif hashtag == "helpmeoverthere":
            #test for the hashtag being made up of some words from the word list
            maxmatchedHashtag = maxMatch("helpmeoverthere", wordlistSet, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "help me over the re", "helpmeoverthere should be changed to help me over the re.")
        elif hashtag == "whaaaaat":
            #test for the hashtag being made up of none of the words in the wordlist
            maxmatchedHashtag = maxMatch("whaaaaat", wordlistSet, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "whaaaaat", "whaaaaat should be changed to whaaaaat.")
        elif hashtag == "findmefood":
            #test for the hashtag being made up of none of the words in the wordlist
            maxmatchedHashtag = maxMatch("findmefood", wordlistSet, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "fi ndmefood", "findmefood should be changed to fi ndmefood.")
def main():

    #check that the user gave the right number of arguments and absolute paths
    (wordlistPath, hashtaglistPath) = checkCommandLineArgs()
    print("Path to the word list: " + wordlistPath)
    print("Path to the hashtag list: " + hashtaglistPath)
            
    #test that the hashtag list has the right words in it
    hashtagSet = readWordsFromFile(hashtaglistPath)
    testhashtags = ["manoverthemoon", "helpmeoverthere"]
    testSetContents(hashtagSet, testhashtags)
        
    #test that the wordlist has the right words in it
    wordlistSet =  readWordsFromFile(wordlistPath)
    testwords = ["moon", "man", "over", "the", "help", "me"]
    testSetContents(wordlistSet, testwords)
    
    #test that the maxmatch algo is working with the tests values
    testMaxMatchAlgo(hashtagSet, wordlistSet)

if __name__ == '__main__':
    main()