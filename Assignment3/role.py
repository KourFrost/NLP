import spacy

nlp = spacy.load("en_core_web_sm")
def printRole(s):
    doc =nlp(s)
    print(s)
    for token in doc:
        print(token.text, token.pos_)

sentance1 = "A small boy set the local market on fire."
sentance2 = "A small boy set the local market on fire."

printRole(sentance1)
printRole(sentance2)