# Open input text file
file = open('declaration.txt', 'r')
readFile = file.read()

# Open output text file
fileOut = open('outputCount.txt', 'w')


# Method to tokenize words in the text file
def tokenize():
    if book is not None:
        words = book.lower().split()
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

            # Does the word appear in list?
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

# Close files
file.close()
fileOut.close()
