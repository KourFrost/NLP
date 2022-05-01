import sys
import csv
from typing_extensions import final

def isABBR(word):
    #(1) Must end with a .
    if word[-1] != ".":
        return 0
    #(2) Must be char [a-z][A-Z] or [.]
    cleanedWord = word.replace(".","")
    isOnlyLetters = cleanedWord.isalpha() 
    if not isOnlyLetters:
        return 0
    #(3) Must be <= len(4)
    isLessThan4 = len(word) <= 4
    if not isLessThan4:
        return 0
    return 1

def isCAP(word):
    if not word[0].isupper():
        return 0
    return 1

def isLOC(word, locData):
    if not word in locData:
        return 0
    return 1 

def isPREF(preWord, prefData):
    if not preWord in prefData:
        return 0
    return 1 

def isSUFF(suffWord, suffData):
    if not suffWord in suffData:
        return 0
    return 1 

def isGLOBCAP(word, preWord,prepData, wordData):
    filteredList = [item.lower() for item in wordData]
    index = filteredList.index(word.lower())
    isHit = index > 0 
    if not isHit:
        return 0
    

    #(1) is only alphabetic 
    isAlpha = wordData[index].isalpha()
    #(2) lowercase is not preposition
    isNotPrep = not wordData[index].lower() in prepData
    #(3) not starting sentence
    isNotStartSentace = preWord != "PHI"
    #(4)Caplized 
    isCap =  wordData[index][0].isupper()
    if isAlpha and isNotPrep and isNotStartSentace and isCap:
        return 1
    return 0

def isGLOBPREF(word, wholeDataSet, wordData):
    filteredList = [item.lower() for item in wordData]
    index = filteredList.index(word.lower())
    isHit = index > 0 
    if not isHit:
        return 0
    
    # print(word, index)
    #(1) is only alphabetic 
    isAlpha = wordData[index].isalpha()
    #(2) not starting sentence
    
    isNotStartSentace = wholeDataSet[index][14] != "PHI"
    #(3)w-1 in prefix 
    hasPrefix =  wholeDataSet[index][10] == 1

    if isAlpha and isNotStartSentace and hasPrefix:
        return 1
    return 0

def isGLOBSUFF(word, wholeDataSet, wordData):
    filteredList = [item.lower() for item in wordData]
    index = filteredList.index(word.lower())
    isHit = index > 0 
    
    if not isHit:
        return 0
    
    #(1) is only alphabetic 
    isAlpha = wordData[index].isalpha()
    #(2) not starting sentence
    isNotStartSentace = wholeDataSet[index][14] != "PHI"
    #(3)w-1 in suffix 
    hasSuffix =  wholeDataSet[index][11] == 1

    if isAlpha and isNotStartSentace and hasSuffix:
        return 1
    return 0
# build csv
trainData = dict()

totalCount = 0
totalDistict =0
feilds = ["LABEL","ABBR","CAP","GLOBCAP","GLOBPREF","GLOBSUFF","LOC","POS","POS+1","POS-1","PREF","SUFF","WORD","WORD+1","WORD-1"]
#  0    1   2   3       4           5       6   7   8   9     10    11   12   13      14
testfile = []

#get location Data
LocDataLocation = "official-data/lists/locations.csv"
LocData = []
with open(LocDataLocation, newline='') as f:
    reader = csv.reader(f)
    headings = next(reader)
    for row in reader:
        LocData = LocData + row

#get Prefix data
PrefDataLocation = "official-data/lists/prefixes.txt"
PrefData = []
with open(PrefDataLocation) as f:
    for index, line in enumerate(f):
        entry = line.split()
        PrefData.append(entry[0])

#get Suffix data
SuffDataLocation = "official-data/lists/suffixes.txt"
SuffData = []
with open(SuffDataLocation) as f:
    for index, line in enumerate(f):
        entry = line.split()
        SuffData.append(entry[0])

#get prep data
PrepDataLocation = "official-data/lists/prepositions.txt"
PrepData = []
with open(PrepDataLocation) as f:
    for index, line in enumerate(f):
        entry = line.split()
        PrepData.append(entry[0])


# handel multiple documents 
files = [sys.argv[1], sys.argv[2]]
 
for item in files:

    FinalRow= [None] * 15  
    FinalSet = []
    documentWords=[]
    preWord = "PHI"
    prePOS = "PHIPOS"

    with open(item) as f:
        for index, line in enumerate(f):
            entry = line.split()
            if (len(entry) < 3):
                preWord = "PHI"
                prePOS = "PHIPOS"
                FinalSet[-1][8] = "OMEGAPOS"
                FinalSet[-1][13] = "OMEGA"
            else:
                documentWords.append(entry[2])
                #print(entry[0], isABBR(entry[2]), isCAP(entry[2]),"GLOBCAP", "GLOBPREF","GLOBSUFF", isLOC(entry[2],LocData), entry[1], prePOS, "POS-1", entry[2],preWord, "word-1")
                nextPOS= "POS+1"
                nextWord= "Word+1"
                if entry[2]== ".": 
                    nextPOS= "OMEGAPOS"
                    nextWord= "OMEGA"

                FinalRow=[entry[0], isABBR(entry[2]), isCAP(entry[2]),"GLOBCAP", "GLOBPREF","GLOBSUFF", isLOC(entry[2],LocData), entry[1], nextPOS, prePOS, isPREF(preWord, PrefData), "SUFF",entry[2],nextWord, preWord ]
                FinalSet.append(FinalRow)
                preWord = entry[2]
                prePOS = entry[1]

    # name of csv file 
    size = len(item)
    filename = item[:size-4]+"_ft.csv"
        
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(feilds) 
        
    
        #********** Global Cap Second pass*************
        for index in range(len(FinalSet)):
            needsNextPOS = FinalSet[index][8] == 'POS+1'
            if needsNextPOS:
                FinalSet[index][8] = FinalSet[index+1][7]
                FinalSet[index][13] = FinalSet[index+1][12]
            FinalSet[index][11] = isSUFF(FinalSet[index][13], SuffData)

            #GlobalCap
            FinalSet[index][3] = isGLOBCAP(FinalSet[index][12],FinalSet[index][14], PrepData, documentWords)
            #GLOBPREF
            FinalSet[index][4] = isGLOBPREF(FinalSet[index][12],FinalSet, documentWords)
            #GLOBSUFF
            FinalSet[index][5] = isGLOBSUFF(FinalSet[index][12],FinalSet, documentWords)
           
        # writing the data rows 
        csvwriter.writerows(FinalSet)