import discord
import aiohttp
import filehandler as io
import discordutils as dcf

import time
import random
import bs4 as bs
from discord.ext import commands


#define the filepaths (#1 for local testing, #2 for server use)

#filepath = 'E:/Coding/Python/faqbot/files/' 
filepath = './files/'

#open the commands xml
root = io.readXML(filepath,'data.xml')

#ids for dreamhack int color code and faq channel, as well as permission denied message
dhorange = 16738079
faqchannel = "<#376765597226106890>"
authfailed = "I\'m sorry Dave, I\'m afraid I can\'t do that."
mirnemoji = "DHCactus"
mirnchance = 40


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
a_en = io.process(a_en, "#faqchannel", faqchannel)
print("Answers processed.\n")
print('------\n')


#generating strings for help commands
help_de = io.gString(comm_de)
help_en = io.eString(comm_en)


#open the token file and mirn counter
TOKEN = io.getToken(filepath)
ADMIN = io.getAdmin(filepath)
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
    await client.change_presence(game=discord.Game(name="f!help | fe!help"))


# message sending and stuff
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #help deutsch
    if message.content.startswith(comm_de[0]):
        embed = discord.Embed(color=dhorange)
        embed.add_field(name="Befehle:", value=help_de)
        embed.add_field(name="English Commands:", value="Type fe!help")
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

    #german commands
    if message.content.startswith("f!"):

        # grab the message content and convert it into a string, then cut off the command prefix
        gmsg = message.content
        str(gmsg)
        gmsg = gmsg[2:]

        # check if there is an actual command or just mention of the command string
        if gmsg[0] == " ":
            return

        #remove any leetspeak and convert to uppercase
        gmsg = io.unLeet(gmsg)
        gmsg = gmsg.upper()

        # check for match of any known command in the xml file, then post help
        for i in range(len(comm_de)):
            command = comm_de[i]
            command = command.upper()
            if gmsg == command:
                index = i
                embed = dcf.FAQ(q_de[index], a_de[index], dhorange)
                await message.channel.send(" ",embed=embed)
                return

        # check for match of certain length (spellchecker)
        for i in range(1,len(comm_de)):
            command = comm_de[i]
            commandu = command.upper()
            for j in range (0,len(gmsg)-1):
                k = len(gmsg) - j
                ph1 = gmsg[:k]
                ph2 = commandu[:k]
                if ph1 == ph2:
                    await message.channel.send("Meinten sie: f!" + command + "?")
                    return    
        
        # if none is found, return an error
        await message.channel.send(authfailed)
        print(str(message.author)+ " used an unknown command (" +str(message.content)+")")
        return
    

    #english commands - work the same way as german commands
    if message.content.startswith("fe!"):
        emsg = message.content
        str(emsg)
        emsg = emsg[3:]
        
        if emsg[0] == " ":
            return

        emsg = io.unLeet(emsg)
        emsg = emsg.upper()

        for i in range(len(comm_en)):
            command = comm_en[i]
            command = command.upper()
            if emsg == command:
                index = i
                embed = dcf.FAQENG(q_en[index], a_en[index], dhorange)
                await message.channel.send(" ",embed=embed)
                return

        # check for match of certain length (spellchecker)
        for i in range(1,len(comm_en)):
            command = comm_en[i]
            commandu = command.upper()
            for j in range (0,len(emsg)-1):
                k = len(emsg) - j
                ph1 = emsg[:k]
                ph2 = commandu[:k]
                if ph1 == ph2:
                    await message.channel.send("Did you mean: fe!" + command + "?")
                    return
        
        await message.channel.send(authfailed)
        print(str(message.author)+ " used an unknown command (" +str(message.content)+")")
        return


    if message.content.startswith("d!aber"):
        for i in range(len(message.author.roles)):
            if message.author.roles[i] == megauser or message.author.roles[i] == admin or message.author.roles[i] == manager:
                embed = discord.Embed(color=dhorange)
                string = message.content[7:]
                embed.add_field(name="Aber ...", value = "...was ist mit " + str(string)+"?")
                embed.set_image(url="https://media.giphy.com/media/xT0xeA1Eq7jidwWBoc/giphy.gif")
                await message.channel.send(" ", embed=embed)
                return
            else:
                await message.channel.send(authfailed)
                print(message.author + " tried to access command d!aber!")
                return

    #mirn v2
    msg = message.content
    str(msg[:6])
    msg = msg.upper()
    if msg[:4] == "MIRN" or msg[:6] == "MIRGEN":
        global mc
        mc+=1
        io.writeVal(filepath, 'mirn.dcbt', mc)
        rnd = random.randint(1,100)
        print(str(message.author) + " rolled: " + str(rnd))
        if rnd < mirnchance:
            await message.add_reaction(mirn)
        return    


    #mirn counter
    if message.content.startswith("d!mirn"):
        embed = discord.Embed(color=dhorange)
        dcf.addEmbed(embed, "Mirns im Welcome: ", mc)
        await message.channel.send(" ", embed=embed)

    #shutdown command
    if message.content.startswith('d!shutdown'):
        if message.author.id == ADMIN:
            await message.channel.send("Shutting Down.")
            await client.close()
        else:
            await message.channel.send(authfailed)
            print(str(message.author) + " tried to access command d!shutdown!")
        return
    
    #set channel
    if message.content.startswith('d!setchannel'):
        if message.author.id == ADMIN:
            global msgchan
            msgchan = client.get_channel(int(message.content[13:]))
            print("Channel set to: " + str(msgchan))
        else:
            await message.channel.send(authfailed)
            print(str(message.author) + " tried to access command d!setchannel!")

    #send messages
    if message.content.startswith('d!msg'):
        if message.author.id == ADMIN:
            botstring = str(message.content[6:])
            await msgchan.send(botstring)
            return
        else: 
            await message.channel.send(authfailed)
            print(str(message.author) + " tried to access command d!msg!")
        
    #read number of mirns from the beginning of time (WARNING, SLOW!)
    if message.content.startswith('d!mupdate'):
        if message.author.id == ADMIN:
            mc = 0
            chann = client.get_channel(137246928227270656)
            dhserv = fetchServer(137246928227270656)
            async for message in chann.history(limit=99999999999999999999):
                msg = message.content
                str(msg[:6])
                msg = msg.upper()
                if msg[:4] == "MIRN" or msg[:6] == "MIRGEN":
                    mc +=1
                    print(str(mc), end="\r")
            print("Total Number of Mirns: "+str(mc))
            io.writeVal(filepath, 'mirn.dcbt', mc)
        else:
            await message.channel.send(authfailed)
            print(str(message.author) + " tried to access command d!mupdate!")

                
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
