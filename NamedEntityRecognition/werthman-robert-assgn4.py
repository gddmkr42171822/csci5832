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
import sys

# Probability of a word occurring with a specific tag
observation_probabilities = {}
# Probability of transitioning from one tag to another
transition_probabilities = {}
# List of the tags in the order they occurred in the training file
tag_sequence = []
# Total number of occurrences for each tag
tag_counts = {}
# Total occurence of a word with a tag 
word_with_tag_counts = {}
# Dictionary of words found in the text
training_vocabulary = {}
# Number of possible states/tags
tags = ['I','O','B']
# List of the order of the words in the text
observation_sequence = []

def GetVocabTraining(txt_file):
	'''
	Create a dictionary of all the words in the text.
	Key is the word, value is not relevant.
	'''
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				training_vocabulary[line[0]] = 0


def GetWordWithTagCountsTraining(txt_file):
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

def GetTagCountsTraining(txt_file):
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

def GetTagSequenceTraining(txt_file):
	'''
	Create a list of the order the tags/states as they appear in the text.
	This is then used to figure out transitions.
	'''
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				tag = line[1]
				tag_sequence.append(tag)

def GetObservationSequenceTest(txt_file):
	'''
	Create a list of the order observations (words) 
	as they appear in the text.
	'''
	with open(txt_file,'r') as f:
		for line in f:
			if line != '\n':
				line = line.strip()
			observation_sequence.append(line)


def CalculateTransitionProbabilities():
	'''
	Finds the probability of a tag coming after another tag.
	'''
	transition_counts = {}
	n = len(tag_sequence)
	print n
	# Find the counts of the transitions in the training data
	for i in range(0,n-1):
		transition = (tag_sequence[i],tag_sequence[i+1])
		if transition in transition_counts:
			transition_counts[transition] += 1
		else:
			transition_counts[transition] = 1
	# Find the probabilities of the transitions by
	# dividing the count of going from tag 1 to tag 2 by
	# the total number of occurrences of tag 1
	for transition in transition_counts:
		if transition[1] in transition_probabilities:
			transition_probabilities[transition[1]][transition[0]] = transition_counts[transition]/(tag_counts[transition[0]]*1.0)
		else:
			transition_probabilities[transition[1]] = {transition[0]:transition_counts[transition]/(tag_counts[transition[0]]*1.0)}

def CalculateObservationProbability():
	'''
	Finds the probability of a word occurring with a tag in the training set.
	'''
	for word in training_vocabulary:
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
				pass
				# The word and tag combination is unknown so we need smoothing???
				# Taken care of in viterbi
		observation_probabilities[word] = probabilities_of_word_given_tag


def Viterbi(T,N):
	'''
	T is a list of observations/length of sequence (words)
	N is a list of of hidden states (tags)
	'''
	transition_prob = 0.0
	observation_prob = 0.0
	# viterbi matrix
	# number of columns is the number of observations (words)
	# number of rows is the number of hidden states (tags)
	# this matrix is referenced by [row][column]
	# ---create a path probability matrix viterbi[N+2,T]---
	viterbi_matrix = [[0 for column in range(len(T))] for row in range(len(N))]
	backpointer_matrix = [[0 for column in range(len(T))] for row in range(len(N))]
	# Initialization Step
	# ---for each state s from 1 to N do---
	for state in range(len(N)):
		# Smoothing
		# Check if we have seen the word
		if T[0] in observation_probabilities:
			# If we have seen this word with this tag
			if N[state] in observation_probabilities[T[0]]:
				observation_prob = observation_probabilities[T[0]][N[state]]
			else:
				# If we have seen this word but not with this tag/state
				observation_prob = 1.0*(10**(-15))
		else:
			# If we have not seen this word at all
			observation_prob = 1.0*(10**(-15))
		transition_prob = 1.0
		# ---viterbi[s,1] = a0,s*bs(o1)---
		viterbi_matrix[state][0] = math.log(transition_prob)+math.log(observation_prob)
		# ---backpointer[s,1] = 0--
		backpointer_matrix[state][0] = 0.0
	# Recursion Step
	# ---for each time step t from 2 to T do---
	for observation in range(1,len(T)):
		# ---for each state s from 1 to N do---
		for state in range(len(N)):
			previous_column_probs = []
			previous_column_transition_probs = []
			# Go through the previous column and states and get the previous viterbi and transitions probabilities
			for previous_column_state in range(len(N)):
				# Iterate through each row in the prevoius column and get the probabilities
				previous_column_probs.append(viterbi_matrix[previous_column_state][observation-1])
				# Also get the transition probabilites of the previous state/tag to the current state/tag
				if N[state] in transition_probabilities:
					# If we have a transition probability from the previous state/tag to the current state/tag
					if N[previous_column_state] in transition_probabilities[N[state]]:
						transition_prob = transition_probabilities[N[state]][N[previous_column_state]]
					else:
						transition_prob = 1.0*(10**(-15))
				else:
					transition_prob = 1.0*(10**(-15))
				previous_column_transition_probs.append(transition_prob)
			# Check if we have an observation probability for the observation (smoothing)
			# If we have seen the word in the training set
			if T[observation] in observation_probabilities:
				# If we have seen the word with this tag in the training set
				if N[state] in observation_probabilities[T[observation]]:
					observation_prob = observation_probabilities[T[observation]][N[state]]
				else:
					# If we have seen this word but not with this tag/state
					observation_prob = 1.0*(10**(-15))
			else:
				# If we have not seen the word at all
				observation_prob = 1.0*(10**(-15))
			# Find probability of the current state = previous_viterbi_prob*transition_prob*observation_prob
			# In this case we use log so we do addition instead of multiplication
			# ---viterbi[s,t]=max(viterbi[s0,t-1]*as0,s*bs(ot))---
			previous_column_state_probs = [x+math.log(y)+math.log(observation_prob) for x,y in zip(previous_column_probs,previous_column_transition_probs)]
			current_column_max = max(previous_column_state_probs)
			viterbi_matrix[state][observation] = current_column_max
			# ---backpointer[s,t]=argmax(viterbi[s0,t-1]*as0,s*bs(ot))---
			backpointer_matrix[state][observation] = current_column_max
	# Termination Step
	# Go back through the backpointer matrix and find the best tag for each observation/column/word
	# This will give us the best tag/state sequence for the sequence that came in
	backtrace = []
	# For each column/observation/word
	for observation in range(0,len(T)):
		prob_observation_per_state = []
		# For each row/state/tag
		for state in range(len(N)):
			prob_observation_per_state.append(backpointer_matrix[state][observation])
		max_prob = max(prob_observation_per_state)
		max_prob_tag = prob_observation_per_state.index(max_prob)
		backtrace.append(N[max_prob_tag])
	return backtrace

def WriteOutput(words,backtrace):
	output_file = 'werthman-assgn4-out.txt'
	f = open(output_file,'a')
	for word, tag in zip(words,backtrace):
		# if the word is a space or newline don't put a tag there
		if word=='\n':
			f.write('{0}'.format(word))
		else:
			f.write('{0}\t{1}\n'.format(word,tag))
	f.close()

def main():
	sequence = []
	training_set = 'gene.train.txt'
	test_set = 'test_tags.txt'
	GetWordWithTagCountsTraining(training_set)
	GetTagCountsTraining(training_set)
	GetVocabTraining(training_set)
	GetTagSequenceTraining(training_set)
	GetObservationSequenceTest(test_set)
	CalculateTransitionProbabilities()
	CalculateObservationProbability()
	for word in observation_sequence:
		sequence.append(word)
		# If the end of a sentence most of the time
		if sequence[-1] == '.':
			#backtrace.extend(Viterbi(sequence,tags))
			backtrace = Viterbi(sequence,tags)
			WriteOutput(sequence,backtrace)
			sequence = []
	#backtrace = Viterbi(observation_sequence,tags)
	#WriteOutput(observation_sequence,backtrace)

	#print 'Observation Probabilities',observation_probabilities
	#print 'Tag/state sequence',tag_sequence
	#print 'Observation Sequence', observation_sequence
	#print 'Transition Probabilities',transition_probabilities
	#print 'Backtrace', backtrace


if __name__ == "__main__":
	main()