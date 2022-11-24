import json

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()

stopwords = set(stopwords.words('english'))

f = open('positional_index.json', 'r')
index = json.load(f)
f.close()

n = int(input('Enter the Previously entered value of n: '))

f = open(str(n)+'-gram-permuterms.json', 'r')
permuterms = json.load(f)
f.close

print('System allows use of wildcard queries with *')

query = input('Enter the query:').split(' ')


# Functions

def merge(n1, n2):
    s1 = set(n1)
    s2 = set(n2)
    return list(s1.intersection(s2))

def processing(word): 
    if n >= len(word): 
        return permuterms[word]
    else: 
        output = []
        for i in range(0, len(word)-n+1):
            if i == 0:
                output = permuterms[word[i:i+n]]
            else: 
                output = merge(output, permuterms[word[i:i+n]])
        return output
    

def permuterm_of_wildcard(word): 
    if word[-1] == '*':
        w = '$' + word[0:-1]
        return processing(w)
    elif word[0] == '*':
        w = word[1:-1]+'$'
        return processing(w)
    else: 
        i = word.find('*')
        w1 = '$' + word[0:i]
        w2 = word[i+1:-1] + '$'
        return merge(processing(w1), processing(w2))
    

def get_query_info(posting_keys, query):

    query_info = list()

    for word in query:
        if word in stopwords:
            continue
        else:
            word = ps.stem(word)
            if word in posting_keys:
                query_info.append(word)

    return query_info
    

# Query vectorization

query_vector = []

for word in query:
    if word in stopwords:
        print('{} word is stopword'.format(word))
        continue

    if '*' in word:
        words = permuterm_of_wildcard(word)
        words.sort()
        for word in words:
            query_vector.append(word)

    else: 
        # word = ps.stem(word)
        if word in index.keys():
            query_vector.append(word)

with open('query_vector.json', 'w', encoding='utf-8') as file: 
    json.dump(query_vector,file,indent=2)
    file.close()

print("Query Vector :", query_vector)