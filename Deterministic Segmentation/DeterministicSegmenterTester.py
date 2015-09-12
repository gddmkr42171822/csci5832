'''
Created on Sep 11, 2015

@author: Bob
'''
import DeterministicSegmenter

def assertion(boolean, testName):
    if boolean:
        print(testName + " PASSED")
    else:
        print(testName + " FAILED")
        
def createWordAndHashtagFiles():
    wordlist = ['moon 5678', 'man 1234', 'over 345', 'the 5678', 'help 777777', 'me 9999',
                 't 7777', 'fi 9999']
    hashtaglist = ['#manoverthemoon', '#helpmeoverthere', '#findmefood', '#whaaaaat']
    
    #create the file with the test words
    with open('testwordlist.txt', 'w') as f:
        for word in wordlist:
            f.write('{0}\n'.format(word))
    
    #create the file with the test hashtags     
    with open('testhashtaglist.txt', 'w') as f:
        for hashtag in hashtaglist:
            f.write('{0}\n'.format(hashtag))
              
def testReadWordsFromFile():
    testwordlist = ['moon', 'man', 'over', 'the', 'help', 'me',
                 't', 'fi']
    testhashtaglist = ['manoverthemoon', 'helpmeoverthere', 'findmefood', 'whaaaaat']
    createWordAndHashtagFiles()
    hashtaglist = DeterministicSegmenter.readWordsFromFile('testhashtaglist.txt', False, 20)
    wordlist =  DeterministicSegmenter.readWordsFromFile('testwordlist.txt', True, 20)
    
    #tests that the right words and hashtags are in the lists
    for word in wordlist:  
        assertion(word in testwordlist, "Set contains {0}.".format(word))
        
    for hashtag in hashtaglist:  
        assertion(hashtag in testhashtaglist, "Set contains {0}.".format(hashtag))
    
    #test that the word list is limited by a certain size
    wordlist = DeterministicSegmenter.readWordsFromFile('testwordlist.txt', True, 2)
    assertion(len(wordlist) == 2, "Word list should be size 2.")
    
def initialTestMaxMatchAlgo():
    testwordlist = ['moon', 'man', 'over', 'the', 'help', 'me',
                 't', 'fi']
    testhashtaglist = ['manoverthemoon', 'helpmeoverthere', 'findmefood', 'whaaaaat']
    for hashtag in testhashtaglist:
        maxmatchedHashtag = ""
        if hashtag == "manoverthemoon":
            #test for the hashtag being made up of entirely of words in the word list
            maxmatchedHashtag = DeterministicSegmenter.maxMatch("manoverthemoon", testwordlist, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "man over the moon", "manoverthemoon should be changed to man over the moon.")
        elif hashtag == "helpmeoverthere":
            #test for the hashtag being made up of some words from the word list
            maxmatchedHashtag = DeterministicSegmenter.maxMatch("helpmeoverthere", testwordlist, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "help me over the r e", "helpmeoverthere should be changed to help me over the r e.")
        elif hashtag == "whaaaaat":
            #test for the hashtag being made up of none of the words in the wordlist
            maxmatchedHashtag = DeterministicSegmenter.maxMatch("whaaaaat", testwordlist, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "w h a a a a a t", "whaaaaat should be changed to w h a a a a a t.")
        elif hashtag == "findmefood":
            #test for the hashtag being made up of none of the words in the wordlist
            maxmatchedHashtag = DeterministicSegmenter.maxMatch("findmefood", testwordlist, maxmatchedHashtag)
            assertion(maxmatchedHashtag == "fi n d me f o o d", "findmefood should be changed to fi n d me f o o d.")
            
def finalTestMaxMatchAlgo():
    #retrieve the wordlist and hashtag list form the file system
    wordlist = DeterministicSegmenter.readWordsFromFile('bigwordlist.txt', True, 75000)
    hashtags = DeterministicSegmenter.readWordsFromFile('hashtags-train.txt', False, 0)
    
    #use the maxmatch algo and change the hashtags and add them to a list
    maxmatchHashtags = []
    for hashtag in hashtags:
        maxmatchHashtags.append(DeterministicSegmenter.maxMatch(hashtag, wordlist, ""))
        
    #get the hashtags of the expected output of the maxmatch algo from professor's provided file
    expectedHashtags = []
    with open('hashtags-train-maxmatch.txt', 'r') as f:
        for line in f:
            #strip off whitespace characters like newlines
            expectedHashtags.append(line.strip())
    
    #compare the hashtags created by the maxmatch algo to those provided by the professor
    for maxmatchHashtag, expectedmaxmatchHashtag in zip(maxmatchHashtags, expectedHashtags):
        assertion(maxmatchHashtag == expectedmaxmatchHashtag, "My maxmatch algo hashtag: {0} should be the same as the professor's maxmatch algo: {1}.".format(maxmatchHashtag, expectedmaxmatchHashtag))
            
def testMinEditDistanceAlgo():
    #retrieve the wordlist and hashtag list form the file system
    wordlist = DeterministicSegmenter.readWordsFromFile("testwordlist.txt", True, 75000)
    hashtags = DeterministicSegmenter.readWordsFromFile("testhashtaglist.txt", False, 0)
    
    #use the maxmatch algo and change the hashtags and add them to a list
    maxmatchHashtags = []
    for hashtag in hashtags:
        maxmatchHashtags.append(DeterministicSegmenter.maxMatch(hashtag, wordlist, ""))
    
    #read in the list of what the hashtags should really look like
    correctHashtags = []
    with open("realtesthashtags.txt", "r") as f:
        for line in f:
            correctHashtags.append(line.strip())
    
    #compare each maxmatchHashtag to each correctHashtag word by word
    totalWER = 0.0
    for maxmatchHashtag, correctHashtag in zip(maxmatchHashtags, correctHashtags):
        #convert each string to a list of the words in the string
        maxmatchHashtagAsList = maxmatchHashtag.split()
        correctHashtagAsList = correctHashtag.split()
        
        #test WER for the the hashtags created by maxmatch
        if correctHashtag == "man over the moon" :
            #maxmatchHashtag is the same as the correctHashtag so no changes need to be made
            assertion(DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList) == 0, "Man over the moon should have a min edit distance of 0")
            assertion(DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList)/len(correctHashtagAsList) == 0, "Man over the moon should have a WER of 0")
            totalWER += DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList)/len(correctHashtagAsList)
        elif correctHashtag == "find me food":
            #maxmatchHashtag:fi ndmefood requires two substitutions fi -> find and ndmefood -> me and an insertion of food
            assertion(DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList) == 7, "Find me food should have a min edit distance of 7")
            assertion(DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList)/len(correctHashtagAsList) == 7.0/3, "Find me food should have a should have a WER of 7/3")
            totalWER += DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList)/len(correctHashtagAsList)
        elif correctHashtag == "help me over there":
            #masmatchHashtag:help me over the re requires a substitution the->there and a deletion of re
            assertion(DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList) == 3, "help me over there should have a min edit distance of 3")
            assertion(DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList)/len(correctHashtagAsList) == 3.0/4, "help me over there should have a WER of 3/4")
            totalWER += DeterministicSegmenter.minEditDist(correctHashtagAsList, maxmatchHashtagAsList)/len(correctHashtagAsList)

    #average the WER across of the hashtags
    assertion(totalWER/len(correctHashtags) == ((7.0/3 + 3.0/4)/3.0), "Average WER across test set should be .58")
    
def main():
    testReadWordsFromFile()
    initialTestMaxMatchAlgo()
    finalTestMaxMatchAlgo()
    testMinEditDistanceAlgo()
    
if __name__ == '__main__':
    main()