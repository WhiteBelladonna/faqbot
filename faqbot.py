import discord
import aiohttp
import filehandler as io
import discordutils as dcf

import time
import random
import bs4 as bs
from discord.ext import commands


#define the filepaths (#1 for local testing, #2 for server use)

filepath = 'E:/Coding/Python/06_FAQBot/files/' 
#filepath = './files'

#open the commands xml
root = io.readXML(filepath,'data.xml')

#ids for dreamhack int color code and faq channel, as well as permission denied message
dhorange = 16738079
faqchannel = "<#376765597226106890>"
authfailed = "I\'m sorry Dave, I\'m afraid I can\'t do that."
mirnemoji = "DHCactus"


#initialize users and emoji
mirn = None
megauser = None
admin = None
manager = None

#read in comm_des
comm_de = io.fetch(root, 'cde')
comm_en = io.fetch(root, 'ceng')
print("Command lists read.\n")


#read in questions
q_de = io.fetch(root, 'qde')
q_en = io.fetch(root, 'qeng')
print("Questions read.\n")


#read in answers
a_de = io.fetch(root, 'ade')
a_en = io.fetch(root, 'aeng')
print("Answers read.\n")


#replace instances of faqchannel in text with the channel id
a_de = io.process(a_de, "#faqchannel", faqchannel)
a_en = io.process(a_de, "#faqchannel", faqchannel)
print("Answers processed.\n")
print('------\n')


#generating strings for help commands
help_de = io.gString(comm_de)
help_en = io.gString(comm_en)


#open the token file and mirn counter
TOKEN = io.getToken(filepath)
mc = io.getVal(filepath, 'mirn.dcbt')

print("Loading Mirns: " + str(mc) +"\n")

#initialize the client
client = discord.Client()
session = aiohttp.ClientSession(loop=client.loop)

print("Logging in...\n")

#returns the server object
def fetchServer(id):
    server = client.get_guild(id)
    return server

#define the status message of the bot
async def GameChanger():
    await client.change_presence(game=discord.Game(name="f!help"))


# message sending and stuff
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #help deutsch
    if message.content.startswith(comm_de[0]):
        embed = discord.Embed(color=dhorange)
        embed.add_field(name="Befehle:", value=help_de)
        embed.add_field(name="English Commands:", value="Type f!hENG")
        dcf.Footer(embed)
        await message.channel.send(" ",embed=embed)
        return

    #help englisch
    if message.content.startswith(comm_en[0]):
        embed = discord.Embed(color=dhorange)
        embed.add_field(name="Commands:", value=help_en)
        dcf.Footer(embed)
        await message.channel.send(" ",embed=embed)
        return

    #befehle
    if message.content.startswith("f!"):
        index = 0
        german = 0
        for i in range(len(comm_de)):
            if message.content == comm_de[i]:
                index = i
                german = 1
        if german == 0:
            for i in range(len(comm_en)):
                if message.content == comm_en[i]:
                    index = i
                else:
                    return
        if german == 1:
            embed = dcf.FAQ(q_de[index], a_de[index], dhorange)
        elif german == 0:
            embed = dcf.FAQENG(q_en[index], a_en[index], dhorange)
        await message.channel.send(" ",embed=embed)
        return

    if message.content.startswith("d!aber"):
        for i in range(len(message.author.roles)):
            if message.author.roles[i] == megauser or admin or manager:
                embed = discord.Embed(color=dhorange)
                string = message.content[7:]
                embed.add_field(name="Aber ...", value = "...was ist mit " + str(string)+"?")
                embed.set_image(url="https://media.giphy.com/media/xT0xeA1Eq7jidwWBoc/giphy.gif")
                await message.channel.send(" ", embed=embed)
                return
            else:
                await message.channel.send(authfailed) 
                return

    #mirn
    if message.content.startswith("mirn" or "Mirn" or "MIRN" or "mirgen" or "Mirgen"):
        global mc
        mc+=1
        io.writeVal(filepath, 'mirn.dcbt', mc)
        rnd = random.randint(1,100)
        print(str(rnd))
        if rnd < 25:
            await message.add_reaction(mirn)
        return

    #mirn counter
    if message.content.startswith("d!mirn"):
        embed = discord.Embed(color=dhorange)
        dcf.addEmbed(embed, "Mirns im Welcome: ", mc)
        await message.channel.send(" ", embed=embed)

    #shutdown command
    if message.content.startswith('d!shutdown'):
        if message.author.id == 137114422626877440:
            await message.channel.send("Shutting Down.")
            await client.close()
        else:
            await message.channel.send(authfailed)
        return
    
    #set channel
    if message.content.startswith('d!setchannel'):
        if message.author.id == 137114422626877440:
            global msgchan
            msgchan = client.get_channel(int(message.content[13:]))
            print("Channel set to: " + str(msgchan))

    #send messages
    if message.content.startswith('d!msg'):
        if message.author.id == 137114422626877440:
            botstring = str(message.content[6:])
            await msgchan.send(botstring)
            return
        
    #read number of mirns from the beginning of time (WARNING, SLOW!)
    # if message.content.startswith('d!mupdate'):
    #     if message.author.id == 137114422626877440:
    #         mc = 0
    #         chann = client.get_channel(137246928227270656)
    #         dhserv = fetchServer(137246928227270656)
    #         async for message in chann.history(limit=99999999999999999999):
    #             if message.content.startswith("mirn" or "Mirn" or "MIRN" or "mirgen" or "Mirgen"):
    #                 mc +=1
    #                 print(str(mc), end="\r")
    #         print("Total Number of Mirns: "+str(mc))
                
#this is executed on startup
@client.event
async def on_ready():
    global mirn, megauser, admin, manager

    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await GameChanger()
    dhserv = fetchServer(137246928227270656)
    mirn = dcf.fetchEmoji(dhserv, mirnemoji)
    megauser = dcf.fetchRole(dhserv, "LAN.megauser")
    admin = dcf.fetchRole(dhserv, "Certified Admin")
    manager = dcf.fetchRole(dhserv, "Certified Manager")
client.run(TOKEN)
