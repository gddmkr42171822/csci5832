'''
Hidden Markov Models:
----------------------
Hidden states: tags I, O, B

Observations: words or vocabulary

Transition probabilities: 
	probability of transitioning between states
	probability of of I given B or B given O
	A = {aij}

Observation likelihoods: 
	probability of word given that the tag is I or O or B

Special initial probability vector
	what is the probability of starting a sequence in a certain state
	pi 

Possible Transitions:
----------------------
b->i i->b o->b b->i i->i o->o b->b i->o o->i
'''
import math

# Probability of a word occurring with a specific tag
observation_probabilities = {}
# Probability of transitioning from one tag to another
transition_probabilities = {}
# List of the tags in the order they occurred in the file
tag_order = []
# Total number of occurrences for each tag
tag_counts = {}
# Total occurence of a word with a tag 
word_with_tag_counts = {}
# Dictionary of words found in the text
words = {}
# Number of possible states/tags
tags = ['I','O','B']
# List of the order of the words in the text
observation_sequence = []

def GetWords(txt_file):
	'''
	Create a dictionary of all the words in the text.
	Key is the word, value is not relevant.
	'''
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				words[line[0]] = 0


def GetWordWithTagCounts(txt_file):
	'''
	Create a dictionary of the count of a word associated with a tag.
	Key is the word and tag as a tuple, value is the number of times it occurred
	'''
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				word_and_tag = (line[0], line[1])
				if word_and_tag in word_with_tag_counts:
					word_with_tag_counts[word_and_tag] += 1
				else:
					word_with_tag_counts[word_and_tag] = 1

def GetTagCounts(txt_file):
	'''
	Create a dictionary of a tag and the number of times
	it occurs in the text.  Key is the tag, value is the number of times
	it occurs.
	'''
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				tag = line[1]
				if tag in tag_counts:
					tag_counts[tag] += 1
				else:
					tag_counts[tag] = 1

def GetTagOrder(txt_file):
	'''
	Create a list of the order the tags appear in the text.
	This is then used to figure out transitions.
	'''
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				tag = line[1]
				tag_order.append(tag)

def GetObservationSequence(txt_file):
	'''
	Create a list of the order observations (words) 
	as they appear in the text.
	'''
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				observation = line[0]
				observation_sequence.append(observation)


def CalculateTransitionProbabilities():
	'''
	Finds the probability of a tag coming after another tag.
	'''
	transition_counts = {}
	n = len(tag_order)
	# Find the counts of the transitions
	for i in range(0,n-2):
		transition = (tag_order[i],tag_order[i+1])
		if transition in transition_counts:
			transition_counts[transition] += 1
		else:
			transition_counts[transition] = 1
	# Find the probabilities of the transitions by
	# dividing the count of going from tag 1 to tag 2 by
	# the total number of occurrences of tag 1
	for transition in transition_counts:
		if transition[0] in transition_probabilities:
			transition_probabilities[transition[1]][transition[0]] = transition_counts[transition]/(tag_counts[transition[0]]*1.0)
		else:
			transition_probabilities[transition[1]] = {transition[0]:transition_counts[transition]/(tag_counts[transition[0]]*1.0)}
	# Add the probabilities of the 'start' and 'end' states???
	transition_probabilities['I']['start'] = 1.0
	transition_probabilities['O']['start'] = 1.0
	transition_probabilities['B']['start'] = 1.0
	transition_probabilities['I']['end'] = 1.0
	transition_probabilities['O']['end'] = 1.0
	transition_probabilities['B']['end'] = 1.0


def CalculateObservationProbability():
	'''
	Finds the probability of a word occurring with a tag.
	'''
	for word in words:
		probabilities_of_word_given_tag = {}
		for tag in tags:
			# Check if we have the word and tag combination in the our training set
			if((word,tag) in word_with_tag_counts):
				word_with_tag_count = word_with_tag_counts[(word,tag)]
				# Get the probability based on the number of times the word occurs with the tag
				# divided by the number of times the tag occurs
				word_prob_with_tag = word_with_tag_count/(tag_counts[tag]*1.0)
				probabilities_of_word_given_tag[tag] = word_prob_with_tag
			else:
				# The word and tag combination is unknown so we need smoothing???
				probabilities_of_word_given_tag[tag] = 1.0
		observation_probabilities[word] = probabilities_of_word_given_tag

def Viterbi(T,N):
	'''
	T is the number of observations/length of sequence (words)
	N is the number of hidden states (tags)
	'''
	# viterbi matrix
	# number of columns is the number of observations (words)
	# number of rows is the number of hidden states (tags)
	# this matrix is referenced by [row][column]
	viterbi_matrix = [[0 for column in range(len(T))] for row in range(len(N))]
	backpointer_matrix = [[0 for column in range(len(T))] for row in range(len(N))]
	# Initialization
	for state in range(len(N)):
		viterbi_matrix[state][0] = math.log(transition_probabilities[N[state]]['start'])+math.log(observation_probabilities[observation_sequence[0]][N[state]])
		backpointer_matrix[state][0] = 0
	# Recursion
	for observation in range(1,len(T)):
		for state in range(len(N)):
			# Look at the previous column and get the max prob
			# and associated tag
			previous_column_probs = []
			for previous_column_state in range(len(N)):
				previous_column_probs.append(viterbi_matrix[previous_column_state][observation-1])
			previous_column_max = max(previous_column_probs)
			previous_column_max_tag = previous_column_probs.index(previous_column_max)
			viterbi_matrix[state][observation] = previous_column_max \
												+math.log(transition_probabilities[N[state]][N[previous_column_max_tag]]) \
												+math.log(observation_probabilities[observation_sequence[observation]][N[state]])

	# Termination
	print viterbi_matrix


def main():
	training_set = 'test_tags.txt'
	GetWordWithTagCounts(training_set)
	GetTagCounts(training_set)
	GetWords(training_set)
	GetTagOrder(training_set)
	GetObservationSequence(training_set)
	CalculateTransitionProbabilities()
	CalculateObservationProbability()
	#Viterbi(observation_sequence,tags)
	#print 'Observation Probabilities',observation_probabilities
	#print 'Order of Tags',tag_order
	print 'Transition Probabilities',transition_probabilities
	#print 'Observation Sequence', observation_sequence

if __name__ == "__main__":
	main()