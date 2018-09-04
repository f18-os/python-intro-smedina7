#!/usr/bin/python

import re
import sys
import string

#set input and output files
inputName = sys.argv[1]
outputName = sys.argv[2]

#open input text file
file = open(inputName, 'r')
text = file.read()

#methods for tokenizing text file
def tokenize():
    if text is not None:
        words = text.lower().split()
#       text = text.strip()
#       word = re.split('[ \t]', text)
#       words = nltk.word_tokenize(text)
        return words
    else:
        return None
        

def map_text(tokens):
    hash_map = {}

    if tokens is not None:
        for element in tokens:
            word = element.replace(",","")
            word = word.replace(".","")
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
fileOut = open(outputName, 'w')

# Tokenize
words = tokenize()

# Create a Hash Map (Dictionary)
map = map_text(words)

# Show Word Information
for word in sorted(map):
    fileOut.write(word+ " " + str(map[word]) + "\n")
    
    
fileOut.close()
