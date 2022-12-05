import json

f = open('relevance_feedback.json','r')
relevance_feedback = json.load(f)
f.close()

f = open('similarity_coefficients.json','r')
similarity = json.load(f)
f.close()


for docId in relevance_feedback["0"].keys():
    # print(docId)

    print(0.05 * relevance_feedback['0'][str(docId)])