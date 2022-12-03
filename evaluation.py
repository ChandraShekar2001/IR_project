import json
import numpy
from math import log10, floor


def round_to_1(x):
   return round(x, -int(floor(numpy.log10(x, where=x > 0))))


f = open('similarity_coefficients.json','r')
results = json.load(f)
f.close()

# for key in results.keys():

docs = results["0"]
len = len(docs)

# print(len)


eval = []

print(" Give input as 1 if Relevant doc and 0 if Non-Relevant doc for the retrieved docId's")

total_relevant = 0

for j in range(len):
    i = int(input("docId: " + str(docs[j]) + " - "))
    if i == 1:
        total_relevant += 1
        eval.append(1)
    else: 
        eval.append(0)

print("\n")

relevant = 0
retrieved = 0
for i in eval:
    retrieved += 1
    if i == 1:
        opinion = "R "
        relevant += 1
    else: 
        opinion = "NR"
    print(opinion, "Precision : ", round_to_1(relevant / retrieved), "\t\tRecall : ", round_to_1(relevant / total_relevant))

print("\nRelevant docs retrieved : ", relevant)
print("Total no of relevant docs: ", total_relevant)
print("Total no of documents retrieved : ", retrieved)