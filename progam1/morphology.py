import sys


def checkDictionary(value, dictionary, POS="-"):
    index = []

    for i in range(len(dictionary)):
        isInDic = value.lower() == dictionary[i][0]
        isPOS = POS in [dictionary[i][1], "-"]
        isValid = isInDic and isPOS
        if isValid:
            index.append(i)

    return list(reversed(index))


def tracePOS(path, rules):
    return rules[path[-1]-1][6]


def writeOutput(file, word, pos, root, source, path):
    if path != "-":
        p = str(path)[1:-1]
        p = p.replace(" ", "")
    else:
        p = path
    outputTemplate = "WORD={}\tPOS={}\tROOT={}\tSOURCE={}\tPATH={}\n".format(
        word, pos, root, source, p)
    print(outputTemplate[:-1])
    file.write(outputTemplate)


def applyRule(word, pos, rule):
    newWord = ""
    newPOS = ""
    returnValue = []
    # check prefix or suffix
    if rule[1] == "SUFFIX":
        if (word[len(word)-len(rule[2]):] == rule[2] and pos in ["-", rule[6]]):
            newWord = word[:len(word)-len(rule[2])]
            if(rule[3] != "-"):
                newWord = newWord+rule[3]
            newPOS = rule[4]
    else:
        # prefix
        if (word[:len(rule[2])] == rule[2] and pos in ["-", rule[6]]):
            newWord = word[len(rule[2]):]
            if(rule[3] != "-"):
                newWord = rule[3]+newWord
            newPOS = rule[4]
    if newWord != "":
        returnValue = returnValue + [newWord, newPOS]
    return returnValue


def morph(dit, rule, word, pos='-', path=[]):
    # check if can apply rule
    output = []
    for i in range(len(rule)):
        newValues = applyRule(word, pos, rule[i])
        if newValues:

            v = int(rules[i][0])
            newPath = []
            if path:
                newPath = newPath+path
            newPath.append(v)

            isInDic = checkDictionary(newValues[0], dit, newValues[1])

            if len(isInDic) > 0:
                if len(dit[isInDic[0]]) > 2:
                    newValues[0] = dit[isInDic[0]][3]
                newValues.append(newPath)
                output.append(newValues)
            else:
                output = output + \
                    morph(dit, rule, newValues[0], newValues[1], newPath)
    return output


# build dictionary
dict = []
with open(sys.argv[1]) as f:
    for index, line in enumerate(f):
        entry = line.split()
        dict.append(entry)

# build Rules
rules = []
with open(sys.argv[2]) as f:
    for index, line in enumerate(f):

        entry = line.split()
        rules.append(entry)

# clear trace file
t = open("trace.txt", "w")

# read words to test
with open(sys.argv[3]) as f:
    for index, line in enumerate(f):
        # set variables
        word = line.rstrip()
        # check if in dictionary
        indexValues = checkDictionary(word, dict)
        if (len(indexValues) > 0):
            for j in range(len(indexValues)):
                if len(dict[indexValues[j]]) > 2:
                    root = dict[indexValues[j]][3]
                else:
                    root = dict[indexValues[j]][0]
                writeOutput(t, word, dict[indexValues[j]]
                            [1], root, "dictionary", "-")
        else:
            # check if we can mophology
            morphValues = morph(dict, rules, word, "-", [])

            if (len(morphValues) > 0):
                # print("morph")
                for j in range(len(morphValues)):
                    writeOutput(
                        t, word, tracePOS(list(reversed(morphValues[j][2])), rules), morphValues[j][0], "morphology", list(reversed(morphValues[j][2])))

            else:
                # default value
                writeOutput(t, word, "noun", word, "default", "-")
        print("")
        t.write("\n")


# close trace file
t.close()
