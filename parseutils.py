import datetime
from datetime import timedelta

#functions to parse text and time.

#function to replace leetspeak with proper text
def unLeet(strIn):
    txt = strIn
    txt = txt.replace("!","i")
    txt = txt.replace("1","i")
    txt = txt.replace("$","s")
    txt = txt.replace("5","s")
    txt = txt.replace("7","t")
    txt = txt.replace("4","a")
    txt = txt.replace("3","e")
    txt = txt.replace("@","a")
    return txt

#function to format the embed text
def embFormat(strIn):
    txt = strIn
    txt = txt.replace("\\n","\n \u200B")
    txt = txt.replace("#faqchannel", "<#376765597226106890>")
    return txt

#function to parse a faq message
def faqParse(arg1):
    txt = str(arg1)
    txt = unLeet(txt)
    txt = txt.upper()
    return txt

def cparse(tx):
    tx = tx.replace("\\n","\n \u200B")
    return tx

def parseTXT(arg1):
    parg1 = unLeet(arg1)
    parg1 = parg1.upper()
    return parg1

def checkComm(commlist, comm):
    for i in range(len(commlist)):
            command = commlist[i]
            command = command.upper()
            if comm == command:
                index = i
                return index
    return False

#checking if a command is in the list and returning the index
def checkCommN(commlist, comm):
    # Quatsch das jedes mal zu machen, habe im faqbot rumgewerkelt ...
    # commlistUpper = [s.upper() for s in commlist]
    try:
        #index = commlistUpper.index(comm)
        index = commlist.index(comm)
        return index
    except ValueError:
        return False

#new function that generates that string
def gString(lst):
    string = ' | '.join(lst)
    return string

#function that generates a feedback text
def feedString(msg):
    string = msg[9:]
    return string 

def parseNum(int):
    if int < 10:
        string = "0" + str(int)
    else:
        string = str(int)
    return string

def createDate(dtobj):
    string = parseNum(int(dtobj.day))+"."
    string = string + parseNum(int(dtobj.month))+"."
    string = string + str(dtobj.year)+" um "
    string = string + parseNum(int(dtobj.hour))+":"
    string = string + parseNum(int(dtobj.minute))
    return string

def dateProcess(dtobj, dtobj2):
    ph = (dtobj-dtobj2)
    print(str(ph))
    ph = ph.seconds
    print(str(ph))
    ph = ph/60
    print(str(ph))
    ph = str(ph)
    ph = ph[:4] + " minutes"
    return ph

