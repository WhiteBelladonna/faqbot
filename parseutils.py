import datetime

#function to remove any leetspeak from command strings (anti troll measure)
def unLeet(strIn):
    ph = strIn
    ph = ph.replace("!","i")
    ph = ph.replace("1","i")
    ph = ph.replace("$","s")
    ph = ph.replace("5","s")
    ph = ph.replace("7","t")
    ph = ph.replace("4","a")
    ph = ph.replace("3","e")
    ph = ph.replace("@","a")
    return ph

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
    a = lst.pop(0)
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

def dateProcess(dtobj):
    ph = (datetime.datetime.now()-dtobj).total_seconds()
    ph = str(ph/60)
    ph = ph[4:] + " minutes"
    return ph
