import json
import math
import re
import os
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))

pattern = re.compile(r'''(?x)([A-Z]\.)+|[\$|Rs]?\d+(\.\d+)?%?|\w+''', re.VERBOSE|re.I)


f = open('positional_index.json','r')
positional_index = json.load(f)
f.close()


f = open('query_info.json','r')
query_info = json.load(f)
f.close()


documents_count = (len([name 
for name in os.listdir('.\dataset') 
    if os.path.isfile(os.path.join('.\dataset', name))]))


def get_idf_values():

    idf_vals = dict()

    for key in sorted(positional_index.keys()):
        reference = positional_index[key]
        occurences = reference['document_frequency']
        idf = math.log2(documents_count / occurences)
        idf_vals[key] = idf
    
    with open('idf_values.json', 'w', encoding='utf-8') as file:
        json.dump(idf_vals, file, indent=4)
        file.close()

    return(idf_vals)


def get_tf_values(word):

    word = positional_index[word]
    documents = word["documents"]
    
    tf_values = dict()
    
    for key in documents.keys():
    
        doc_ref = documents[key]
    
        freq = doc_ref["frequency"]
        tf_value = math.log2(freq)
        tf_values[key] = tf_value + 1

    with open('tf_values.json', 'w', encoding='utf-8') as file:
        json.dump(tf_values, file, indent=4)
        file.close()
    
    return tf_values


def get_tf_idf_value(word, doc_id):

    idf_values = get_idf_values()
    tf_values = get_tf_values(word)

    # print(tf_values[doc_id])
    # print(idf_value[word])

    tf_idf = tf_values[doc_id] * idf_values[word]
    
    return tf_idf


def get_doc_info(doc):

        doc_info = list()

        for word in doc:
            word = word.group()
            word = word.lower()
            if word in stopwords:
                continue
            else:
                 if word in positional_index.keys():
                    doc_info.append(word)
        
        return doc_info


def get_doc_vector(doc, doc_id):
    
    doc_info = get_doc_info(doc)

    vector = list()

    for word in sorted(positional_index.keys()):
        if word in doc_info:
            tf_idf = get_tf_idf_value(word, doc_id)
            vector.append(tf_idf)
        else: 
            vector.append(0)
        
    return vector


def get_query_vector(query):

    query_vector = list()
    index = dict()

    for word in query:
        if word in index.keys():
            index[word] += 1 
        else: 
            index[word] = 1

    tf_query = dict()

    for word in query:
        tf_query[word] = math.log2(index[word]) + 1
        

    idf_values = get_idf_values()


    for word in sorted(positional_index.keys()):
        if word in query:
            tf_idf = tf_query[word] * idf_values[word]
            query_vector.append(tf_idf)
        else: 
            query_vector.append(0)

    

    return(query_vector)


def get_query_vector_matrix():

    query_vector_matrix = dict()

    for key in query_info.keys():
        query_vector_matrix[key] = get_query_vector(query_info[key])

    with open('query_vectors.json', 'w', encoding='utf-8') as file:
        json.dump(query_vector_matrix, file, indent=4)
        file.close()
    

def get_doc_vector_matrix():

    os.chdir("dataset")
    files = os.listdir()


    doc_vector_matrix = dict()

    for i in range(0, 10):
        doc_id = files[i].split('.')[0]
        file = open(files[i], 'r', encoding = 'utf8')
        words = pattern.finditer(file.read())

        doc_vector_matrix[str(doc_id)] = get_doc_vector(words, doc_id)

    os.chdir("..")

    with open('doc_vectors.json', 'w', encoding='utf-8') as file:
        json.dump(doc_vector_matrix, file, indent=4)
        file.close()


def cosine_similarity(query_vector, doc_vector):

    query_magnitude = math.sqrt(sum([ value * value for value in query_vector ]))
    doc_magnitude = math.sqrt(sum([ value * value for value in doc_vector ]))

    dot_product = 0

    for i in zip(query_vector, doc_vector):
        q,d = i
        dot_product += (q * d)

        

    return dot_product / ( query_magnitude * doc_magnitude )


def get_similarity_coeff():

    get_doc_vector_matrix()

    # print(get_query_vector(query_info['0']))

    get_query_vector_matrix()

    f = open('doc_vectors.json','r')
    doc_vectors = json.load(f)
    f.close()

    f = open('query_vectors.json','r')
    query_vectors = json.load(f)
    f.close()

    # similarity_coefficients = {}
    similarity_coefficients = dict()
    sim_coeff = dict()
    sim_coeff_array = dict()

    # print(query_vectors["0"])


    # for doc in doc_vectors.keys():
    #     for query in query_vectors.keys():
    #         # similarity_coefficients[doc] = {'query': query, 'similarity': cosine_similarity(query_vectors[query], doc_vectors[doc])}
    #         # similarity_coefficients[doc].append({'query': query, 'similarity': cosine_similarity(query_vectors[query], doc_vectors[doc])})
    #         if doc in similarity_coefficients.keys():
    #             similarity_coefficients[doc]['queries'][query] = cosine_similarity(query_vectors[query], doc_vectors[doc])
    #         else: 
    #             similarity_coefficients[doc] = {
    #                 'queries' : query,
    #                 'similarity': cosine_similarity(query_vectors[query], doc_vectors[doc])
    #             }

# Current code -------------------------------------------------
    if len(query_vectors) == 1:
        for docId in doc_vectors.keys():
            # if str(docId) in doc_vectors.keys():
            similarity_coefficients[str(docId)] = cosine_similarity(query_vectors['0'], doc_vectors[docId])
    
        sim_coeff = sorted(similarity_coefficients.items(), key=lambda x:x[1], reverse=True)
        
        # for query in query_vectors.keys():
        sim_coeff_array['0'] = sim_coeff
    
    
    # else:
    #     for query in query_vectors.keys():

    #         for docId in doc_vectors.keys():


        
    # sim_coeff = []

    # sim_coeff = {}


    # for keys in similarity_coefficients.keys():
    #     # sim_coeff.append((similarity_coefficients[keys], keys))
    #     sim_coeff[keys]

    # sim_coeff = sorted(sim_coeff, reverse=True)

    # print(sim_coeff)

    with open('similarity_coefficients.json', 'w', encoding='utf-8') as file:
        json.dump(sim_coeff_array, file, indent=4)
        # json.dump(similarity_coefficients, file, indent=4)
        file.close()


        
get_similarity_coeff()
