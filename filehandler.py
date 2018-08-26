import xml.etree.ElementTree as ET

#function to open and parse the XML file
def readXML(filepath, filename):
    tree = ET.parse(filepath + filename)
    root = tree.getroot()
    return root

#function that returns a list of XML elements with a given name from the etree root
def fetch(root, name):
    lst = []

    for command in root:
        ph = command.find(name)
        if ph is not None:
            lst.append(ph.text)
        else:
            lst.append("")
    return lst

#function that replaces a substring in a list element with another substring
def process(lst, st1, st2):
    for item in lst:
        ph = item
        ph = ph.replace(st1, st2)
        item = ph
    return lst

#function that generates a string from a list without the first element
def gString(lst):
    string = ""
    for i in range(1,len(lst)-2):
        string = string + ("f!"+lst[i]) + "  |  "
    string = string + lst[len(lst)-1]
    return string

def eString(lst):
    string = ""
    for i in range(1,len(lst)-2):
        string = string + ("fe!"+lst[i]) + "  |  "
    string = string + lst[len(lst)-1]
    return string

#get an integer value from a file
def getVal(filepath, filename):
    with open(filepath+filename, 'r') as f:
        val = f.read()
        val = int(val)
    return val

#write a value to a file
def writeVal(filepath, filename, val):
    with open(filepath+filename, 'w') as f:
        f.write(str(val))
    return

#get the bot token
def getToken(filepath):
    with open(filepath+'TOKEN.dcbt', 'r') as f:
        TOKEN = f.read()
    return TOKEN

def getAdmin(filepath):
    with open(filepath+'ADMIN.dcbt', 'r') as f:
        ADMIN = f.read()
    ADMIN = int(ADMIN)
    return ADMIN

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