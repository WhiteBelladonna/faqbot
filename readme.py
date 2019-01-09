import xml.etree.ElementTree as ET
import discord

#define the filepath
filepath = './files/'
dhorange = 16738079

#generate empty post
post = []
titles = []

#function to open and parse the XML file
def read(filepath, filename):
    tree = ET.parse(filepath + filename)
    root = tree.getroot()
    return root

#function to generate a post
def generatePost():
    root = read(filepath,'faq.xml')
    for i in range(len(root)):
        title = generateTitle(root[i][0].text)
        titles.append(title)
        ph1 = []
        ph2 = []
        ph3 = []
        for j in range(1,len(root[i])):
            if root[i][j].tag == "heading":
                ph1.append(root[i][j].text)
            if root[i][j].tag == "text":
                ph2.append(root[i][j].text)
        ph3.append(ph1)
        ph3.append(ph2)
        post.append(generateEmbed(ph3))
    return post, titles

def generateTitle(stuff):
    title = "**=================================\n" + stuff + "\n" + "=================================**"

def generateEmbed(liststuff):
    embed = discord.Embed(color=dhorange)
    for i in range(len(liststuff[0])):
        embed.add_field(name=str(liststuff[0][i]), value=liststuff[1][i], inline=False)
    return embed


#function that returns a list of XML elements with a given name from the etree root
def get(root, name):
    lst = []
    for command in root:
        ph = command.find(name)
        if ph is None or ph.text is None:
            lst.append(" ")
        else:
            lst.append(ph.text)        
    return lst

generatePost()