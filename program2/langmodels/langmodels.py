
import sys
import math
import random

def calcUni(count, total):
    proablity = count/total
    return math.log2(proablity)

def generateSentance(seedValue, count, data):
    search_key = seedValue+" "
    totalInstances = 0
    bigramKeys = []
    weights = []
    for key in data.keys():
        isMatch = search_key.lower() == key[0:len(search_key)]
        if (isMatch):
            bigramKeys.append(key)
            weights.append(data[key])
            totalInstances = totalInstances + data[key]
    
    if not bigramKeys:
        return ""
    nextValues = random.choices(bigramKeys, weights)
    chosenWord = nextValues[0][len(search_key):]
    isSentanceEnd = chosenWord in [".","!","?"] 
    isMaxWordCount = count >=10
    isTerminated = isSentanceEnd or isMaxWordCount
    if isTerminated:
        return chosenWord
    else:
        return chosenWord + " " + generateSentance(chosenWord, count+1, data)

def displayValue(file, word, uni, big, bigflag, bigsmooth):
    roundValue = 4
    formatValue = '.'+str(roundValue)+'f'
    template = "S = "+word[0]+"\n\nUnsmoothed Unigrams, logprob(S) = "+format(round(uni,roundValue), formatValue)+"\n"
    if (bigflag):
        template=template+"Unsmoothed Bigrams, logprob(S) = undefined\n"
    else:
        template=template+"Unsmoothed Bigrams, logprob(S) = "+format(round(big,roundValue), formatValue)+"\n"
    template=template+"Smoothed Bigrams, logprob(S) = "+format(round(bigsmooth,roundValue), formatValue)+"\n"
    print(template)
    file.write(template)


# build train values
trainData = dict()

totalCount = 0
totalDistict =0
with open(sys.argv[1]) as f:
    for index, line in enumerate(f):
        entry = line.split()
        previousWord = "/phi"
        if (previousWord in trainData.keys()):
            trainData[previousWord] = trainData[previousWord]+1
        else:
            trainData[previousWord] = 1
        for i in range(len(entry)):
            totalCount=totalCount+1
            key = entry[i].lower()
            if (key in trainData.keys()):
                trainData[key] = trainData[key]+1
            else:
                totalDistict =totalDistict+1
                trainData[key] = 1
            bigKey = previousWord+" "+ key
            if (bigKey in trainData.keys()):
                trainData[bigKey] = trainData[bigKey]+1
            else:
                trainData[bigKey] = 1
            previousWord = key
# print(trainData)
# print(totalCount)

if sys.argv[2] == "-test":
    # clear trace file
    t = open("langmodels-output.txt", "w")

    with open(sys.argv[3]) as f:
        for index, line in enumerate(f):
            entry = line.split()
            #calcuate uniValue
            uniValue =0.0
            for i in range(len(entry)):
                key = entry[i].lower()
                uniValue =uniValue + calcUni(trainData[key],totalCount)


            #calcuate bigram 
            bigramValue =0.0
            previousWord ="/phi"
            isUndefined = False
            for i in range(len(entry)):
                key = entry[i].lower()
                bigKey = previousWord+" "+ key
                if (bigKey in trainData.keys()):
                    bigramValue =bigramValue + calcUni(trainData[bigKey], trainData[previousWord])
                else:
                    isUndefined = True
                previousWord = key


            #calcuate bigram smooth
            bigramSmoothValue =0.0
            previousWord ="/phi"
            
            for i in range(len(entry)):
                key = entry[i].lower()
                bigKey = previousWord+" "+ key
                if (bigKey in trainData.keys()):
                    bigramSmoothValue =bigramSmoothValue + calcUni(trainData[bigKey]+1, trainData[previousWord]+totalDistict)
                else:
                    bigramSmoothValue =bigramSmoothValue + calcUni(1, trainData[previousWord]+totalDistict)

                previousWord = key

            displayValue(t, entry, uniValue, bigramValue,isUndefined, bigramSmoothValue)
            t.write("\n")

if sys.argv[2] == "-gen":
    t = open("langmodels-gen.txt", "w")
    with open(sys.argv[3]) as f:
        for index, line in enumerate(f):
            entry = line.split()
            seed = entry[0]
            print("Seed = ", seed)
            t.write("Seed = "+seed)
            print()
            t.write("\n")
            for i in range(10):
                t.write("\n")
                gen = generateSentance(seed, 0, trainData)
                print ("Sentence ",i+1,":",seed,gen)
                t.write("Sentence "+str(i+1)+":"+seed+" "+gen)
            print()
            t.write("\n\n")


