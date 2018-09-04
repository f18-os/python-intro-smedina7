#!/usr/bin/python

import re
import sys

#set input and output files
inputName = sys.argv[1]
outputName = sys.argv[2]

#open input text file
file = open(inputName, 'r')
text = file.read()

#open output text file
fileOut = open(outputName, 'w')

#methods for tokenizing text file
def tokenize():
    if text is not None:
        words = text.lower().split()
        return words
    else:
        return None
        

def map_text(tokens):
    hash_map = {}

    if tokens is not None:
        for element in tokens:
            # Remove Punctuation
            word = element.replace(",","")
            word = word.replace(".","")
            word = word.replace(",","")
            word = word.replace(";","")
            word = word.replace(":","")
            word = word.replace("-", " ")
            

            # Word Exist?
            if word in hash_map:
                hash_map[word] = hash_map[word] + 1
            else:
                hash_map[word] = 1

        return hash_map
    else:
        return None

#Open output file
fileOut = open('outputCount.txt', 'w')

# Tokenize the Book
words = tokenize()
#word_list = ['HE','Multitude']

# Create a Hash Map (Dictionary)
map = map_text(words)

# Show Word Information
for word in sorted(map):
    fileOut.write(word+ " " + str(map[word]) + "\n")
    
    
fileOut.close()


#    print('Word: [' + word + '] Frequency: ' + str(map[word]))