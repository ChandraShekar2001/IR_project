import json

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()

stopwords = set(stopwords.words('english'))

f = open('positional_index.json', 'r')
positional_index = json.load(f)
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
        w2 = word[i+1:] + '$'
        return merge(processing(w1), processing(w2))
        

# Query term vectorization

query_vector = []

permu_query_vector = dict()

permuterm_vector = list()

for word in query:
    
    word = word.lower()

    if word in stopwords:
        continue

    if '*' in word:
        words = permuterm_of_wildcard(word)
        words.sort()
        permuterm_vector = words
        query_vector.append('#')

    else: 
        # word = ps.stem(word)
        if word in positional_index.keys():
            query_vector.append(word)

print(permuterm_vector)

try: 
    i = query_vector.index('#')
except:
    i = -1       

if i != -1:
    for word in permuterm_vector:
        query_vector[i] = word
                
        permu_query_vector[word] = (query_vector[:])

else: 
    permu_query_vector[0] = (query_vector)
            


with open('query_info.json', 'w', encoding='utf-8') as file: 
    json.dump(permu_query_vector,file,indent=2)
    file.close()

