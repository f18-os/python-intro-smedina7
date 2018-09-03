file = open('declaration.txt', 'r')
book = file.read()


def tokenize():
    if book is not None:
        words = book.split()
        return words
    else:
        return None
        

def map_book(tokens):
    hash_map = {}

    if tokens is not None:
        for element in tokens:
            # Remove Punctuation
            word = element.replace(",","")
            word = word.replace(".","")

            # Word Exist?
            if word in hash_map:
                hash_map[word] = hash_map[word] + 1
            else:
                hash_map[word] = 1

        return hash_map
    else:
        return None


# Tokenize the Book
words = tokenize()
#word_list = ['HE','Multitude']

# Create a Hash Map (Dictionary)
map = map_book(words)

# Show Word Information
#for word in word_list:
#    print('Word: [' + word + '] Frequency: ' + str(map[word]))