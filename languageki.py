from fuzzywuzzy import fuzz

keywrd = [
        [
            ["009009009", "900900900"],
            ["009009009", "900900900"]
        ],
        [
            ["reservierung", "sitzplatzreservierung", "platzwahl", "seating", "sitzplatz", "sitzplätze", "platzreservierung"],
            ["wann", "beginnt", "eigentlich", "geht", "datum"]
        ],
        [
            ["pavillon", "pavillion", "zelt", "überdachung"],
            ["mitbringen","mitnehmen","aufbauen", "darf", "eigentlich", "wie"]
        ],
        [
            ["turnier", "turniere", "turnieren"],
            ["infos", "spiele", "welche", "was", "gibt"]
        ],
        [
            ["zapfanlage", "zapfanlagen"],
            ["mitbringen","mitnehmen","aufbauen", "darf", "eigentlich", "was"]
        ],
        [
            ["behindert", "dumm", "bescheuert"],
            ["bot", "du", "bist"]
        ],
        [
            ["kühlschrank", "kühlschränke"],
            ["mitbringen", "platz", "darf", "eigentlich", "wie"]
        ]
    ]

topics = ["Nicht Erkannt","Platzreservierung","Pavillon","Turniere", "Zapfanlage", "Dumm", "Kühlschrank"]

def nProcess(message):
    global topics
    message = message.replace("?", "")
    msgwords = message.split(" ")
    subscore, topicid = sentenceTree(msgwords)
    return subscore, topics[topicid], topicid


def sentenceTree(wordlist):
    global keywrd
    subscore = 0
    topic = 0

    for word in wordlist:
        for i in range(len(keywrd)):
            for j in range(len(keywrd[i][0])):
                if fuzz.ratio(word.upper(), keywrd[i][0][j].upper()) >= 80:
                    topic = i
                    break
    for word in wordlist:                
        for k in range(len(keywrd[topic][1])):
            if fuzz.ratio(word.upper(), keywrd[topic][1][k].upper()) >= 80:
                subscore = subscore + 1
    return subscore, topic