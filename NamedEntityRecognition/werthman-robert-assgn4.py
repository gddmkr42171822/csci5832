'''
Possible Transitions:
b->i i->b(missing) o->b b->i i->i o->o b->b(missing) i->o o->i(can't happen)
'''

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
	# the count of tag 1
	for transition in transition_counts:
		transition_probabilities[transition] = transition_counts[transition]/(tag_counts[transition[0]]*1.0)

def CalculateObservationProbability():
	'''
	Finds the probability of a word occurring with a tag.
	'''
	tags = ['I','O','B']
	for word in words:
		probabilities_of_word_given_tag = []
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
		observation_probabilities[word] = probabilities_of_word_given_tag

def main():
	training_set = 'test_tags.txt'
	GetWordWithTagCounts(training_set)
	GetTagCounts(training_set)
	GetWords(training_set)
	GetTagOrder(training_set)
	CalculateTransitionProbabilities()
	CalculateObservationProbability()
	print observation_probabilities
	print tag_order
	print transition_probabilities

if __name__ == "__main__":
	main()