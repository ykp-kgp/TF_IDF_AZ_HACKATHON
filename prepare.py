import chardet

def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc

filename = 'index.txt'

# Read the content of the file
with open(filename, 'r', errors ="ignore") as f:
    lines = f.readlines()

# Convert all lines to lowercase
lines = [line.lower() for line in lines]
lines2 = [string.split() for string in lines]
print((lines2[3]))

for i in range(len(lines2)):
    for j in range(len(lines2[i])):
        lines2[i][j] = lines2[i][j].replace('.', '')

print(lines2)

# for j in range(len(lines2[3])):
#     print(type(lines2[3][j]))
#     print((lines2[3][j]))

# ls2 = ['linked', 'list', 'random', 'node']
# for i in range(len(ls2)):
#     print(ls2[i])
#     print(type(ls2[i]))

number_text = lines[4].strip()
number = int(float(number_text.split()[0]))
print(number)

# Write the modified content back to the file
with open(filename, 'w', encoding = 'latin-1', errors ="ignore") as f:
    f.writelines(lines)

my_encoding = find_encoding(filename)

with open(filename, 'r', encoding=my_encoding, errors ="ignore") as f:
    lines = f.readlines()

def preprocess(document_text):
    # remove the leading numbers from the string, remove not alpha numeric characters, make everything lowercase
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms

vocab = {}
documents = []
for index, line in enumerate(lines):
    # read statement and add it to the line and then preprocess
    tokens = preprocess(line)
    documents.append(tokens)
    tokens = set(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1

# reverse sort the vocab by the values
vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

print('Number of documents: ', len(documents))
print('Size of vocab: ', len(vocab))
print('Sample document: ', documents[0])

# save the vocab in a text file
filename = 'vocab.txt'

# Open the file in write mode and truncate its content
with open(filename, 'w', encoding = find_encoding(filename),errors ="ignore") as f:
    f.truncate()

with open('vocab.txt', 'w', encoding = 'latin-1',errors ="ignore") as f:
    for key in vocab.keys():
        f.write("%s\n" % key)

# save the idf values in a text file
filename = 'idf-values.txt'

# Open the file in write mode and truncate its content
with open(filename, 'w', encoding = 'latin-1',errors ="ignore") as f:
    f.truncate()

with open('idf-values.txt', 'w', encoding = 'latin-1',errors ="ignore") as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

# save the documents in a text file
filename = 'documents.txt'

# Open the file in write mode and truncate its content
with open(filename, 'w', encoding = 'latin-1',errors ="ignore") as f:
    f.truncate()

with open('documents.txt', 'w', encoding = 'latin-1',errors ="ignore") as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))


inverted_index = {}
for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

# save the inverted index in a text file
filename = 'inverted-index.txt'

# Open the file in write mode and truncate its content
with open(filename, 'w', encoding = 'latin-1',errors ="ignore") as f:
    f.truncate()

with open('inverted-index.txt', 'w', encoding = 'latin-1',errors ="ignore") as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))
