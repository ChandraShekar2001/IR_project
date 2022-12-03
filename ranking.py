import json
import math
import itertools

f = open('positional_index.json','r')
positional_index = json.load(f)
f.close()

f = open('query_info.json','r')
query_info = json.load(f)
f.close()

f = open('idf_values.json','r')
idf_values = json.load(f)
f.close()


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
    

def cosine_similarity(query_vector, doc_vector):

    query_magnitude = math.sqrt(sum([ value * value for value in query_vector ]))
    doc_magnitude = math.sqrt(sum([ value * value for value in doc_vector ]))

    dot_product = 0

    for i in zip(query_vector, doc_vector):
        q,d = i
        dot_product += (q * d)

        

    return dot_product / ( query_magnitude * doc_magnitude )


def get_similarity_coeff():

    # get_doc_vector_matrix()

    # print(get_query_vector(query_info['0']))

    # get_query_vector_matrix()

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
    ranking = dict()

    # print(query_vectors["0"])

# Current code -------------------------------------------------
    if len(query_vectors) == 1:
        for docId in doc_vectors.keys():
            # if str(docId) in doc_vectors.keys():
            similarity_coefficients[str(docId)] = cosine_similarity(query_vectors['0'], doc_vectors[docId])
    
        sim_coeff = sorted(similarity_coefficients.items(), key=lambda x:x[1], reverse=True)
        
        # for query in query_vectors.keys():
        sim_coeff_array['0'] = sim_coeff
    
        ranking["0"] = list(sim_coeff_array["0"][i][0] for i in range(10))[:10]  #Working code for getting 1st 10 relevent docs. -----------------------------------
    
    else:
        for query in query_vectors.keys():

            for docId in doc_vectors.keys():
                similarity_coefficients[str(docId)] = cosine_similarity(query_vectors[query], doc_vectors[docId])
            
            sim_coeff = sorted(similarity_coefficients.items(), key=lambda x:x[1], reverse=True)
        
            sim_coeff_array[query] = sim_coeff[:]

            # ranking[query] = list(sim_coeff_array[query].keys())[0:10]
            # ranking[query] = {k: sim_coeff_array[k] for k in list(sim_coeff_array[query])[:10]}
            # ranking[query] = {sim_coeff_array[query][i][0] for i in range(10)}

            ranking[str(query)] = list(sim_coeff_array[str(query)])[:10]




    # sim_coeff_array = dict(list(sim_coeff_array.items())[0:10])

    # ranking = dict(list(sim_coeff_array.items())[0:10])

    # ranking = {sim_coeff_array["0"][i] for i in range(10)}

    # print(ranking[i] for i in query_vectors.keys())

    print(ranking['0'])

    with open('similarity_coefficients.json', 'w', encoding='utf-8') as file:
        # json.dump(sim_coeff_array, file, indent=4)
        json.dump(ranking, file, indent=4)
        # json.dump(similarity_coefficients, file, indent=4)
        file.close()


        
get_similarity_coeff()
