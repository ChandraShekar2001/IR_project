import os
import re
import json

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()

stopwords = set(stopwords.words('english'))

os.chdir("dataset")

pattern = re.compile(r'''(?x)([A-Z]\.)+|[\$|Rs]?\d+(\.\d+)?%?|\w+''', re.VERBOSE|re.I)

files = os.listdir()
index = dict()

for i in range(0, len(files)):
    docId = files[i].split(".")[0]
    file = open(files[i], 'r', encoding = 'utf8')
    words = pattern.finditer(file.read())
    position = 1
    document = {}

    for word in words:
        word = word.group()
        word = word.lower()

        if word in stopwords:
            continue
        if word in document.keys():
            document[word]['frequency'] +=1
            document[word]['positions'].append(position)    
        else:
            document[word] = {
                'frequency' :1,
                'positions' : [position]
            }
        position+=1

    for word in document.keys():
        
        if word in index.keys():
            index[word]['document_frequency']+=1
            index[word]['documents'][str(docId)] = document[word]
        else:
            index[word] = {
                'document_frequency':1,
                'documents': {str(docId):document[word]}
            }

os.chdir("..")

with open('positional_index.json', 'w', encoding='utf-8') as file:
    json.dump(index, file, indent=4)
    file.close()



print('Number of words in the positional indexing {}'.format(len(index)))