
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
		# Return the tag with the highest probability

def main():
	training_set = 'gene.train.txt'
	GetWordWithTagCounts(training_set)
	GetTagCounts(training_set)
	CalculateObservationProbability('the')

if __name__ == "__main__":
	main()