from fuzzywuzzy import fuzz

keywrd = [
        [],
        ["reservierung", "sitzplatzreservierung", "platzwahl", "seating", "sitzplatz", "sitzplätze", "platzreservierung"],
        ["pavillon", "pavillion", "zelt", "überdachung"],
        ["turnier", "turniere", "turnieren"],
        ["zapfanlage", "zapfanlagen"],
        ["behindert", "dumm", "bescheuert"],
        ["kühlschrank", "kühlschränke"],
    ]

topics = ["Nicht Erkannt","Platzreservierung","Pavillon","Turniere", "Zapfanlage", "Dumm", "Kühlschrank"]


def process(message):
    qweight = 1
    qscore = 0
    qperc = 0.0
    if "?" in message:
        qscore = qscore + qweight
    message = message.replace("?", "")
    keywords = message.split(" ")
    qscore = qscore + isQuestion(keywords)
    qperc = (qscore / len(keywords)) * 100
    qperc = float("{0:.2f}".format(qperc))
    print(qperc)
    if qperc > 100:
        qperc = 100
    topic, topicid = findTopic(keywords)
    return qperc, topic, topicid

def isQuestion(splitstring):
    qscores = ["wer", "wo", "wie", "wann", "warum", "was", "wieso", "weshalb", "eigentlich", "kann", "darf", "erlaubt", "zugelassen", "weiß", "weiss", "schon"]
    subscore = 0
    for word in splitstring:
        for match in qscores:
            if fuzz.ratio(word.upper(), match.upper()) >= 90:
                subscore = subscore + 1
    return subscore

def findTopic(splitstring):
    global topics
    global keywrd
    topic = 0
    for word in splitstring:
        for i in range(len(keywrd)):
            for j in range(len(keywrd[i])):
                if fuzz.ratio(word.upper(), keywrd[i][j].upper()) >= 80:
                    topic = i
                    break
    return topics[topic], topic