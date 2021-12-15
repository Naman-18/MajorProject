import csv
def extractInfo(s):
    words = s.split(' ')
    for i in range(0,len(words)):
        words[i] = words[i].lower()
    pos = 0.0
    neg = 0.0
    with open("NEGATIVE.csv","r") as file:
        csvReader = csv.reader(file)
        fields = next(csvReader)
        for row in csvReader:
            if row[1] in words:
                pos = pos+1
    with open("POSITIVE.csv","r") as file:
        csvReader = csv.reader(file)
        fields = next(csvReader)
        for row in csvReader:
            if row[1] in words:
                neg = neg+1
    
    pos = pos / len(words)
    neg = neg / len(words)
    if pos > neg:
        pos = pos + 1.5
        neg = neg + 0.5
    elif neg > pos:
        pos = pos + 0.5
        neg = neg+1.5
    else:
        pos = pos+1
        neg = neg+1
    return [pos,neg]