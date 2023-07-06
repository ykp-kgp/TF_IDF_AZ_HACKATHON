import math
import codecs
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

def load_vocab():
    vocab = {}
    with open('vocab.txt', 'r', encoding = 'latin-1') as f:
        vocab_terms = f.readlines()
    with open('idf-values.txt', 'r', encoding = 'latin-1') as f:
        idf_values = f.readlines()
    
    for (term, idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    
    return vocab

def load_documents():
    documents = []
    with open('documents.txt', 'r', encoding = 'latin-1') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    print('Number of documents:', len(documents))
    print('Sample document:', documents[0])
    return documents

def load_inverted_index():
    inverted_index = {}
    with open('inverted-index.txt', 'r', encoding = 'latin-1') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0, len(inverted_index_terms), 2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    
    print('Size of inverted index:', len(inverted_index))
    return inverted_index

def load_link_of_qs():
    with open("Qindex.txt", 'r', encoding = 'latin-1') as f:
        links = f.readlines()

    return links


def find_index(l1, l2):
    for i in range(len(l2)):
        if isinstance(l2[i], float):
            continue
        if all(word in l2[i] for word in l1):
            return i
    return -1






# l1 = ["apple", "banana", "cherry"]
# l2 = [["apple", "banana"], ["cherry", "orange"], ["apple", "banana", "cherry"]]



vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()
Qlink = load_link_of_qs()

def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
                
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])
    
    return tf_values

def get_idf_value(term):
    return math.log(len(documents)/vocab_idf_values[term])


filename = 'index.txt'

# Read the content of the file
with open(filename, 'r', encoding = 'latin-1') as f:
    lines = f.readlines()

# Convert all lines to lowercase
lines = [line.lower() for line in lines]
lines2 = [string.split() for string in lines]

for i in range(len(lines2)):
    for j in range(len(lines2[i])):
        lines2[i][j] = lines2[i][j].replace('.', '')

def calculate_sorted_order_of_documents(query_terms):
    potential_documents = {}
    results = []
    for term in query_terms:
        if vocab_idf_values[term] == 0:
            continue
        tf_values_by_document = get_tf_dictionary(term)
        idf_value = get_idf_value(term)
        print(term,tf_values_by_document,idf_value)
        for document in tf_values_by_document:
            if document not in potential_documents:
                potential_documents[document] = tf_values_by_document[document] * idf_value
            potential_documents[document] += tf_values_by_document[document] * idf_value

    print(potential_documents)
    # divite by the length of the query terms
    for document in potential_documents:
        potential_documents[document] /= len(query_terms)

    potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True)[:20])


   

    for doc_index in potential_documents:
        index = find_index(documents[int(doc_index)], lines2)
        if 0 <= index < len(lines2):
            number_text = lines2[index][0].replace('.', '')
            number = int(number_text)
            results.append({"Question Link": Qlink[int(index)], "Score": potential_documents[doc_index]})
            

    return results


# query_string = input('Enter your query: ')
# query_terms = [term.lower() for term in query_string.strip().split()]

# print(query_terms)
# ans_results = calculate_sorted_order_of_documents(query_terms)
# print(ans_results)

app = Flask(__name__, static_folder='static')
app.template_folder = 'Templates'

app.config['SECRET_KEY'] = 'Ammy_p'



# app = Flask(__name__)
# # @app.route('/')
# def hello_world():
#     return 'Hello World'

class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')


@app.route("/<query>")
def return_links(query):
    q_terms = [term.lower() for term in query.strip().split()]
    return jsonify(calculate_sorted_order_of_documents(q_terms))


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search.data
        q_terms = [term.lower() for term in query.strip().split()]
        results = calculate_sorted_order_of_documents(q_terms)
    return render_template('index.html', form=form, results=results)
