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

#function that generates a string from a list without the first element
def gString(lst):
    string = ""
    for i in range(1,len(lst)-2):
        string = string + (lst[i]) + "  |  "
    string = string + lst[len(lst)-1]
    return string
