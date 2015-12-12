'''
Possible Transitions:
b->i i->b(missing) o->b b->i i->i o->o b->b(missing) i->o o->i(can't happen)
'''


words = {}
def GetWords(txt_file):
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				words[line[0]] = 0

word_with_tag_counts = {}
def GetWordWithTagCounts(txt_file):
	with open(txt_file,'r') as f:
		# Create a dictionary of a word associated with a tag
		# Key is the word and tag as a tuple, value is the number of times it occurred
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				word_and_tag = (line[0], line[1])
				if word_and_tag in word_with_tag_counts:
					word_with_tag_counts[word_and_tag] += 1
				else:
					word_with_tag_counts[word_and_tag] = 1

tag_counts = {}
def GetTagCounts(txt_file):
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				tag = line[1]
				if tag in tag_counts:
					tag_counts[tag] += 1
				else:
					tag_counts[tag] = 1
tag_order = []
def GetTagOrder(txt_file):
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				tag = line[1]
				tag_order.append(tag)

transitions = []
def GetTransitions(txt_file):
	with open(txt_file,'r') as f:
		for line in f:
			line = line.strip().split('\t')
			if(len(line)>1):
				tag = line[1]
				transitions.append(tag)

transition_probabilities = {}
def CalculateTransitionProbabilities():
	transition_counts = {}
	n = len(transitions)
	# Find the counts of the transitions
	for i in range(0,n-2):
		transition = (transitions[i],transitions[i+1])
		if transition in transition_counts:
			transition_counts[transition] += 1
		else:
			transition_counts[transition] = 1
	# Find the probabilities of the transitions by
	# dividing the count of going from tag 1 to tag 2 by
	# the count of tag 1
	for transition in transition_counts:
		transition_probabilities[transition] = transition_counts[transition]/(tag_counts[transition[0]]*1.0)

def CalculateObservationProbability(word):
	probabilities_of_word_given_tag = []
	tags = ['I','O','B']
	for tag in tags:
		# Check if we have the word and tag combination in the our training set
		if((word,tag) in word_with_tag_counts):
			word_with_tag_count = word_with_tag_counts[(word,tag)]
			# Get the probability based on the number of times the word occurs with the tag
			# divided by the number of times the tag occurs
			word_prob_with_tag = word_with_tag_count/(tag_counts[tag]*1.0)
			probabilities_of_word_given_tag.append((tag,word_prob_with_tag))
		else:
			# The word is unknown so we need smoothing
			pass
	# Return the tag with the highest probability??
	return probabilities_of_word_given_tag

def main():
	observation_probabilities = {}
	training_set = 'gene.train.txt'
	GetWordWithTagCounts(training_set)
	GetTagCounts(training_set)
	GetWords(training_set)
	GetTransitions(training_set)
	CalculateTransitionProbabilities()
	# Get the observation probabilities for each word
	for word in words:
		observation_probabilities[word] = CalculateObservationProbability(word)
	#print observation_probabilities
	#print transitions
	#print transition_probabilities
if __name__ == "__main__":
	main()