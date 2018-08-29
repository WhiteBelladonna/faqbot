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

def getFeed(filepath):
    with open(filepath+'FEED.dcbt', 'r') as f:
        Feed = f.read()
    Feed = int(Feed)
    return Feed
