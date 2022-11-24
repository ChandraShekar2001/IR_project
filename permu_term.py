import json

f = open('positional_index.json','r')
positional_index = json.load(f)
f.close()

index = {}

n = int(input('Enter the value of n : '))

for word in positional_index.keys():

    word = '$'+word+'$'

    if n >= len(word):
        if word not in index.keys():
            index[word] = [word[1:-1]]
        else:
            if word not in index[word]:
                index[word].append(word[1:-1])
    
    else:
        for i in range(len(word)-n+1):
            if word[i:i+n] not in index.keys():
                index[word[i:i+n]] = [word[1:-1]]
            else:
                if word not in index[word[i:i+n]]:
                    index[word[i:i+n]].append(word[1:-1])           
    

with open(str(n)+'-gram-permuterms.json','w',encoding='utf-8') as file:
    json.dump(index,file,indent=4)
    file.close()   

print('No of {0}-grams in the positional_index {1}'.format(n, len(index)))
