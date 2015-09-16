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
output maxmatched hashtags to a file

Part 2
---------

Create a working Word Error Rate that takes two files as input: 
    the hashtags outputted by the maxmatch and what the hashtag should really look like based on the english language
    
Change min edit algo to make it work
Compute WER from result of minimum edit distance divided by length of gold standard list

Part 3
-------
change maxmatch to get a better word error rate
possible changes:

Changes to MaxMatch strategy
    1) instead of taking the largest word that fits take the smallest word greater >= 2 characters *this was not an improvement*
    2) maxmatch backwards instead of forwards * improved WER from .60 to .35*
    3) don't add spaces after characters not found in corpus *improved WER from .39 to .35*
    4) run maxmatch both ways and take output with fewer words, if same number take reverse maxmatch
    5) check for the largest string in any part of the hashtag instead of just at the front or end
    
Changes to gready nature
    1) if there is a single letter at the end of the string combine it with the previous word *greedy nature changed, improved WER from .66 to .60* 

Changes to lexicon
    1) do not take single characters to be words in the word list/lexicon *this did not improve anything*
    2) clean up lexicon/corpus/wordlist to not include typos

    
    


'''

import re
import sys
import os



def readWordsFromFile(filePath, limitNumWords, numWordsLimit):
    '''
    TODO: docstring
    '''
    wordlist = []
    #create a regular expression to match the first word in a line of the file
    pattern = re.compile('\w+')
    #read the file into memory
    with open(filePath, 'r') as f:
        #go through the file line by line and get the first word out of each line
        #if we aren't limited by the number of words extract a word out of every line
        if not limitNumWords:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    wordlist.append(match.group(0))
        else:
            counter = 0
            for line in f:
                #make sure the number of words in the set is under the number of word limit keep
                #adding them to the set
                if counter < numWordsLimit:
                    match = re.search(pattern, line)
                    if match:
                        wordlist.append(match.group(0))
                else:
                    break
                counter += 1
    return wordlist

def maxMatch(hashtag, wordlist, maxmatchedHashtag):
    '''
    TODO: docstring
    '''
    substringList = []
    largestWord = ""
    for word in wordlist:
        #make a list of the words that start at the beginning of the hashtag
        if hashtag.startswith(word):
            substringList.append(word)
    #if words were found in the wordlist that fit into the hashtag 
    if len(substringList) != 0:
        #find largest string in the substring list
        largestWord = max(substringList, key=len)
        #if there are still characters after the largest word is found 
        #look through the word list again for the next largest word
        if len(largestWord) < len(hashtag):
            maxmatchedHashtag = maxmatchedHashtag + largestWord + " "
            #return is necessary otherwise maxmatchedHashtag is discarded
            return maxMatch(hashtag[len(largestWord):], wordlist, maxmatchedHashtag)
        #if the largest word goes to the end the hashtag add it to the maxmatchHashtag
        elif len(largestWord) == len(hashtag):
            return (maxmatchedHashtag + largestWord)
        else:
            #this is for the largest word being longer than the hashtag
            #which should never happen
            print("Error: this maxMatch function statement should never be reached")
    else:
        #if no more words in the word list fit into the hashtag move over a character and try again
        #if the remaining hashtag is greater than a single character send it back to maxmatch
        if len(hashtag) > 1:
            maxmatchedHashtag = maxmatchedHashtag + hashtag[0] + " "
            return maxMatch(hashtag[1:], wordlist, maxmatchedHashtag)
        else:
            #otherwise just add the single character as a new word to the maxmatchedHashtag
            return (maxmatchedHashtag + hashtag)

def backwardsMaxMatch(hashtag, wordlist, maxmatchedHashtag):
    '''
    TODO: docstring
    '''
    substringList = []
    largestWord = ""
    for word in wordlist:
        #make a list of the words that start at the end hashtag
        #IMPROVEMENT: RUN MAXMATCH BACK TO FRONT
        if hashtag.endswith(word):
            substringList.append(word)
    #if words were found in the wordlist that fit into the hashtag
    if len(substringList) != 0:
        #find largest string in the substring list
        largestWord = max(substringList, key=len)
        #if there are still characters after the largest word is found 
        #look through the word list again for the next largest word
        if len(largestWord) < len(hashtag):
            #make sure single characters aren't alone so don't put a space between them
            if len(largestWord) > 1:
                maxmatchedHashtag = " " + largestWord + maxmatchedHashtag
            else:
                maxmatchedHashtag = largestWord + maxmatchedHashtag
            return backwardsMaxMatch(hashtag[:-len(largestWord)], wordlist, maxmatchedHashtag)
        #if the largest word takes up the entire hashtag
        elif len(largestWord) == len(hashtag):
            #if the largestWord is greater than a single character create a new word
            if len(largestWord) > 1:
                #return (maxmatchedHashtag + largestWord)
                return (largestWord + maxmatchedHashtag)
            else:
                #otherwise add the single character to the previous word
                #IMPROVEMENT: DON'T LET SINGLE CHARACTERS START THE WORD
                return (largestWord + maxmatchedHashtag.lstrip())
        else:
            #this is for the largest word being longer than the hashtag
            #which should never happen
            print("Error: this maxMatch function statement should never be reached")
    else:
        #if no more words in the word list fit into the hashtag move over a character and try again
        #if the remaining hashtag is greater than a single character send it back to maxmatch
        if len(hashtag) > 1:
            #IMPROVEMENT: don't add spaces after characters not found in wordlist
            maxmatchedHashtag = hashtag[-1] + maxmatchedHashtag
            return backwardsMaxMatch(hashtag[:-1], wordlist, maxmatchedHashtag)
        else:
            #if the remaining hashtags is a single character just append it to the previous word
            #IMPROVMENT: DON'T LET SINGLE CHARACTErS BE BY THEMSELVES AT THE BEGINNING OF A WORD
            return (hashtag + maxmatchedHashtag.lstrip())    
        
def anyMaxMatch(hashtag, wordlist, maxmatchedHashtag):
    '''
    TODO: docstring
    '''
    #if the hashtag is empty then don't do anything
    if not hashtag:
        return maxmatchedHashtag
    
    substringList = []
    largestWord = ""
    for word in wordlist:
        #make a list of the words that start anywhere in the hashtag
        if word in hashtag:
            substringList.append(word)
    #if words were found in the wordlist that fit into the hashtag
    if len(substringList) > 0:
        #find largest string in the substring list
        largestWord = max(substringList, key=len)
        #split the string in half based on the largest word
        splitSides = hashtag.split(largestWord, 1)
        if len(splitSides[0]) < 2:
            maxmatchedHashtag = splitSides[0] + largestWord
        else:
            maxmatchedHashtag = anyMaxMatch(splitSides[0], wordlist, maxmatchedHashtag) + " " + largestWord
        if len(splitSides[1]) < 2:
            maxmatchedHashtag = maxmatchedHashtag + splitSides[1]
        else:
            maxmatchedHashtag = maxmatchedHashtag + " " + anyMaxMatch(splitSides[1], wordlist, maxmatchedHashtag)
        return maxmatchedHashtag
    else:
        return hashtag
        
def checkCommandLineArgs(): 
    '''
    TODO: docstring
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

def  minEditDist(target, source):
    ''' Computes the min edit distance from target to source. Figure 3.25 in the book. Assume that
    insertions, deletions and (actual) substitutions all cost 1 for this HW. Note the indexes are a
    little different from the text. There we are assuming the source and target indexing starts a 1.
    Here we are using 0-based indexing.'''
    
    #number of rows of the matrix/table
    n = len(target)
    #number of columns of the matrix/table
    m = len(source)

    #create the n by m matrix 
    distance = [[0 for i in range(m+1)] for j in range(n+1)]
    
    #create the base cases of the matrix 
    #which ends up being the length of each substring
    #1 2 3 4... down the rows
    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + 1
    
    #1 2 3 4... across the columns
    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + 1
    
    #fill in the rest of the matrix with costs
    #insertions = 1, delete = 1, substitution = 0 if the words are equal, 2 if they are not
    for i in range(1,n+1):
        for j in range(1,m+1):
            distance[i][j] = min(distance[i-1][j] + 1,
                                 distance[i][j-1] + 1,
                                 distance[i-1][j-1]+substCost(source[j-1],target[i-1]))
    return float(distance[n][m])

def substCost(source, target):
    '''
    TODO: docstring
    '''
    if source == target:
        return 0
    else:
        return 1

def runMaxMatchMinEdit(maxmatchFunction, wordlist, hashtaglist):
    #use the maxmatch algo and change the hashtags and add them to a list
    print("Calculating the maxmatch of the hashtags.")
    maxmatchHashtags = []
    for hashtag in hashtaglist:
        maxmatchHashtags.append(maxmatchFunction(hashtag, wordlist, ""))
    
    #write the maxmatched hashtags to a file
    print("Writing the maxmatched hashtags to the file myMaxMatchHashtagList.txt.")
    with open('myMaxMatchHashtagList.txt', 'w') as f:
        for maxmatchHashtag in maxmatchHashtags:
            f.write("{0}\n".format(maxmatchHashtag))
    
    #caculcate the minimum edit distance between the hashtags I created and what
    #they really should be
    #load created hashtags into a set
    maxmatchHashtags = []
    with open('myMaxMatchHashtagList.txt', 'r') as f:
        for line in f:
            maxmatchHashtags.append(line.strip())
            
    #load correct hashtags into a set
    correctHashtags = []
    with open('hashtags-train-reference.txt', 'r') as f:
        for line in f:
            correctHashtags.append(line.strip())
    
    #go through each list and compare the strings
    print("Calculating the average WER across the test set.")
    totalWER = 0.0
    for maxmatchHashtag, correctHashtag in zip(maxmatchHashtags, correctHashtags):
        #convert each string to a list of the words in the string
        maxmatchHashtagAsList = maxmatchHashtag.split()
        correctHashtagAsList = correctHashtag.split()
        #call min edit and add up wer for each string and then divide that by total number of lines in the hashtag file
        totalWER += minEditDist(correctHashtagAsList, maxmatchHashtagAsList)/len(correctHashtagAsList)
        
    #to get the average word error rate across the entire test set
    print("Average WER across test set is {0}".format(totalWER/len(correctHashtags)))

def main():

    #check that the user gave the right number of arguments and absolute paths
    (wordlistPath, hashtaglistPath) = checkCommandLineArgs()
    print("Path to the word list: " + wordlistPath)
    print("Path to the hashtag list: " + hashtaglistPath)
    
    wordlist = readWordsFromFile(wordlistPath, True, 75000)
    hashtaglist = readWordsFromFile(hashtaglistPath, False, 0)
    
    '''
    print("----Running normal maxmatch function.----")
    runMaxMatchMinEdit(maxMatch, wordlist, hashtaglist)
    print("----Running backwards maxmatch function----")
    runMaxMatchMinEdit(backwardsMaxMatch, wordlist, hashtaglist)
    '''
    print("----Running any maxmatch function----")
    runMaxMatchMinEdit(anyMaxMatch, wordlist, hashtaglist)
    
    
if __name__ == '__main__':
    main()