from fuzzywuzzy import fuzz

keywrd = [
        [
            ["009009009", "900900900"],
            ["009009009", "900900900"]
        ],
        [
            ["reservierung", "sitzplatzreservierung", "platzwahl", "seating", "sitzplatz", "sitzplätze", "platzreservierung", "platzauswahl", "platzieren"],
            ["ab", "wann", "beginnt", "eigentlich", "geht", "datum", "los", "startet", "neues", "gibts", "stattfindet", "gibt es", "aussuchen", "auszusuchen"]
        ],
        [
            ["pavillon", "pavillion", "zelt", "überdachung"],
            ["mitbringen","mitnehmen","aufbauen", "darf", "eigentlich", "wie", "sind", "erlaubt"]
        ],
        [
            ["turnier", "turniere", "turnieren"],
            ["infos", "spiele", "welche", "was", "gibt", "wird", "geben", "csgo", "fortnite"]
        ],
        [
            ["zapfanlage", "zapfanlagen"],
            ["mitbringen","mitnehmen","aufbauen", "darf", "eigentlich", "was", "sind", "erlaubt"]
        ],
        [
            ["behindert", "dumm", "bescheuert", "arschloch"],
            ["bot", "du", "bist", "ist", "eigentlich", "doch"]
        ],
        [
            ["kühlschrank", "kühlschränke"],
            ["mitbringen", "platz", "darf", "eigentlich", "wie", "sind", "erlaubt", "zugelassen"]
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