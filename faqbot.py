import discord
import aiohttp
import filehandler as io
import discordutils as dcf
import parseutils as pu
import scraper as sc
import datetime
import subprocess
import sys

import time
import random
import bs4 as bs
from discord.ext import commands

prefixes = ["d!", "f!", "fe!"]
bot = commands.Bot(command_prefix=prefixes)
bot.remove_command("help")

#define the filepath
filepath = './files/'

#open the commands xml
root = io.readXML(filepath,'data.xml')
print("XML file read \n")

#ids for dreamhack int color code and faq channel, as well as permission denied message
dhorange = 16738079
faqchannel = "<#376765597226106890>"
authfailed = "I\'m sorry Dave, I\'m afraid I can\'t do that."
unknown_de = "Den Befehl kenne ich leider nicht. Schau doch mal in meiner Befehlsübersicht nach:"
unknown_en = "I don't recognize that command. Try checking my commandlist:"
mirnemoji = "DHCactus"
mirnchance = 42
msgchan = 137246928227270656
faqcid = 484264883169525760
intid = 183158280216903680
randomuid = 214832573392748544 

#initialize users and emoji
mirn = None
megauser = None
admin = None
manager = None
faqdm = None
faqmsgchan = None
messagechannel = None
dhserv = None
internal = None
membed = None

#antispam variable
last = datetime.datetime.now()
spamdelay = 20


#read faq commands
comm_de = io.fetch(root, 'cde')
comm_en = io.fetch(root, 'ceng')

print("Command lists read.\n")

print("German Commands:"+str(comm_de))
print("English Commands:"+str(comm_en))

#generate uppercase commands from lists
comm_de_upper = [s.upper() for s in comm_de]
comm_en_upper = [s.upper() for s in comm_en]


#read in questions and parse the text (formating and replacing)
q_de = io.fetchTXT(root, 'qde')
q_en = io.fetchTXT(root, 'qeng')
print("Questions read and processed.\n")


#read in answers and parse the text (formating and replacing)
a_de = io.fetchTXT(root, 'ade')
a_en = io.fetchTXT(root, 'aeng')
print("Answers read and processed.\n")


#read a user list for voting
ul = io.getUserList(filepath)
print("Userlist read.\n")

print('------\n')

#generating strings for help commands
help_de = pu.gString(comm_de)
help_en = pu.gString(comm_en)

#open the token file and mirn counter
TOKEN = io.getToken(filepath)
ADMIN = io.getAdmin(filepath)
faquid = io.getFeed(filepath)
mc = io.getVal(filepath, 'mirn.dcbt')

print("Loading Mirns: " + str(mc) +"\n")

print("Logging in...\n")

#returns the server object
def fetchServer(id):
    server = bot.get_guild(id)
    return server

#define the status message of the bot
async def GameChanger():
    await bot.change_presence(game=discord.Game(name="f!help | fe!help"))
    return

#sends an embed message
async def sendEmbed(channelObject, embedObject):
    await channelObject.send(" ", embed=embedObject)
    return

#downtime Check
async def DownTime():
    async for message in internal.history(limit=50):                #find last message by bot (restarting, etc)
        if message.author == bot.user:                              
            timeObject1 = message.created_at                        #create time object of last message
            break
    await internal.send("Bot Online")
    async for message in internal.history(limit=1):                 #create time object of newest bot message (Online)
        timeObject2 = message.created_at
    downtime = pu.dateProcess(timeObject2, timeObject1)             #calculate time difference in minutes
    await internal.send("Downtime: " + downtime)                    #send time difference
    return

@bot.command(name="restart")
async def restart(ctx):
    if ctx.prefix == "d!":
        if ctx.author.id == ADMIN:
           await ctx.message.channel.send("Restarting...")
           subprocess.Popen([sys.executable, "./restart.py"])
           await bot.close()
           return
        for i in range(len(ctx.author.roles)):
             if ctx.author.roles[i] == admin:
                await ctx.message.channel.send("Restarting...")
                subprocess.Popen([sys.executable, "./restart.py"])
                await bot.close()
                return

@bot.command(name="update")
async def update(ctx):
    if ctx.prefix == "d!":
        if ctx.author.id == ADMIN:
           await ctx.message.channel.send("Updating...")
           subprocess.Popen([sys.executable, "./update.py"])
           await bot.close()
           return
        for i in range(len(ctx.author.roles)):
             if ctx.author.roles[i] == admin:
                await ctx.message.channel.send("Updating...")
                subprocess.Popen([sys.executable, "./update.py"])
                await bot.close()
                return

@bot.command(name="ban")
async def ban(ctx):
    if ctx.prefix == "d!":
        if ctx.author.id == ADMIN:
           banid = dcf.fetchUser(dhserv, ctx)
           await banid.ban(banid, reason=None, delete_message_days=0)
           await ctx.message.channel.send(str(banid) + " was banned from the server.")
           return

#define the different commands
@bot.command(name="shutdown")
async def shutdown(ctx):
    if ctx.prefix == "d!":
        if ctx.author.id == ADMIN:
            await ctx.send("Shutting down...")
            await bot.close()
        else:
            await ctx.message.channel.send(authfailed)
            print(str(ctx.author) + " tried to access command d!shutdown!")
            return


@bot.command(name="help")
async def help(ctx):
    if ctx.prefix == "f!":
        await sendEmbed(ctx.message.channel, dcf.helpDE(help_de))
        return
    elif ctx.prefix == "fe!":
        await sendEmbed(ctx.message.channel, dcf.helpEN(help_en))
        return

@bot.command(name="remaining")
async def remaining(ctx):
    if ctx.prefix == "f!":
        remaining, sold = sc.crawlTickets()
        remst = str(sold) + " / 1800"
        verst = str(remaining)
        embed = discord.Embed(color=dhorange)
        embed.add_field(name="Verkaufte Tickets:", value=remst, inline=False)
        embed.add_field(name="Verbleibende Tickets:", value=verst, inline=False)
        await ctx.send(" ", embed=embed)
    else:
        return

@bot.command(name="aber")
async def aber(ctx):
    if ctx.prefix == "d!":
        for i in range(len(ctx.author.roles)):
            if ctx.author.roles[i] == megauser or ctx.author.roles[i] == admin or ctx.author.roles[i] == manager:
                embed = discord.Embed(color=dhorange)
                string = ctx.message.content[7:]
                embed.add_field(name="Aber ...", value = "...was ist mit " + str(string)+"?")
                embed.set_image(url="https://media.giphy.com/media/xT0xeA1Eq7jidwWBoc/giphy.gif")
                await ctx.message.channel.send(" ", embed=embed)
                return
            else:
                await ctx.message.channel.send(authfailed)
                print(ctx.message.author + " tried to access command d!aber!")
                return

@bot.command(name="embed")
async def embed(ctx):
    if ctx.prefix == "d!":
        if ctx.author.id == ADMIN:
            global msgchan
            embed = discord.Embed(color=dhorange)
            embed.add_field(name="...", value = str(ctx.message.content))
            await msgchan.send("", embed=embed)
            return
        else:
            await ctx.message.channel.send(authfailed)
            print(ctx.message.author + " tried to access command d!embed!")
            return

#FAQ Command
@bot.command(name="aq")
async def aq(ctx, arg1):
    if ctx.prefix == "f!":                                              #check for german prefix
        gmsg = pu.faqParse(arg1)                                        #parse the message (unleet, upper, fancy stuff)
        ph = pu.checkCommN(comm_de_upper, gmsg)                         #check for existing command
        if ph is not False:                                             #generate and send a reply to the faq command
            await sendEmbed(ctx.message.channel, dcf.FAQ(q_de[ph], a_de[ph], dhorange))            
            return
        else:                                                           #generate and send a help embed if the command is not found
            await ctx.send(unknown_de, embed=dcf.helpDE(help_de))
            print(str(ctx.message.author)+ " used an unknown command (" +str(ctx.message.content)+")")
            return

    if ctx.prefix == "fe!":                                             #check for english prefix
        emsg = pu.faqParse(arg1)                                        #parse the message (unleet, upper, etc)
        ph = pu.checkCommN(comm_en_upper, emsg)                         #check for existing command
        if ph is not False:                                             #generate and send a reply to the faq command
            await sendEmbed(ctx.message.channel, dcf.FAQENG(q_en[ph], a_en[ph], dhorange))
            return
        else:                                                           #generate and send a help embed if the command is not found
            await ctx.send(unknown_en, embed=dcf.helpEN(help_en))
            print(str(ctx.message.author)+ " used an unknown command (" +str(ctx.message.content)+")")
            return

#check how many mirns were posted in the welcome
@bot.command(name="mirn")
async def mirnn(ctx):
    if ctx.prefix == "d!":
        embed = discord.Embed(color=dhorange)
        dcf.addEmbed(embed, "Mirns im Welcome: ", mc)
        await ctx.message.channel.send(" ", embed=embed)  

#set a channel for the bot to communicate in 
@bot.command(name="setchannel")
async def setchannel(ctx, arg):
    if ctx.prefix == "d!":
        if ctx.message.author.id == ADMIN:
            global msgchan
            msgchan = bot.get_channel(int(arg))
            print("Channel set to: " + str(msgchan))
        else:
            await ctx.message.channel.send(authfailed)
            print(str(ctx.message.author) + " tried to access admin restricted command d!setchannel!")


@bot.command(name="msg")
async def sendmsg(ctx):
    if ctx.prefix == "d!":
        if ctx.message.author.id == ADMIN:
            botstring = str(ctx.message.content)
            botstring = botstring[5:]
            await msgchan.send(botstring)
            return
        else: 
            await ctx.channel.send(authfailed)
            print(str(ctx.message.author) + " tried to access admin restricted command d!msg!")


@bot.command(name="mupdate")
async def mirnupdate(ctx):
    if ctx.prefix == "d!":
        if ctx.message.author.id == ADMIN:
            mc = 0
            chann = bot.get_channel(137246928227270656)
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
            await ctx.message.channel.send(authfailed)
            print(str(ctx.message.author) + " tried to access admin restricted command d!mupdate!")

@bot.command(name="eedback")
async def feedback(ctx):
    if ctx.prefix == "f!":
        author = "<@"+str(ctx.message.author.id)+">"
        creation = pu.createDate(ctx.message.created_at)
        header = "Neues Feedback vom " + creation
        message = pu.feedString(str(ctx.message.content))
        feedback = "Feedback von User: {} \n\n".format(author)
        feedback = feedback + message
        print("Der User "+str(ctx.message.author)+"hat Feedback hinterlassen!")
        embed = discord.Embed(color=dhorange)
        dcf.addEmbed(embed, header, feedback)
        await faqdm.send(" ", embed = embed)
        await faqmsgchan.send(" ", embed = embed)

@bot.command(name="onnerstag")
async def donnerstag(ctx):
    if ctx.prefix == "d!":
        global ul
        for user in ul:
            if ctx.message.author.id == user:
                await ctx.message.channel.send("Du hast bereits abgestimmt!") 
                return

        ul.append(ctx.message.author.id)
        io.writeUserList(filepath, ul)
        await ctx.message.channel.send("Stimme registriert!") 
        return

@bot.command(name="checkvote")
async def checkvote(ctx):
    if ctx.prefix == "d!":
        embed = discord.Embed(color=dhorange)
        dcf.addEmbed(embed, "Anzahl der User, die sich den Donnerstag wünschen: ", str(len(ul)))
        await ctx.message.channel.send(" ", embed = embed)

# message sending and stuff
@bot.event
async def on_message(message):
    global last, spamdelay
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

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
        if message.author.id == randomuid:
            await message.add_reaction(mirn)
        elif rnd < mirnchance:
            await message.add_reaction(mirn)
        return   
    if msg[:4] == "MOIN":
        if (datetime.datetime.now()-last).seconds > spamdelay:
            print(str(message.author) + " said moin! OH NO!")
            await message.channel.send("Meinten sie: __mirn__?")
            last = datetime.datetime.now()
            return
    if msg[:6] == "MORGEN":
        if (datetime.datetime.now()-last).seconds > spamdelay:
            print(str(message.author) + " said morgen! OH NO!")
            await message.channel.send("Meinten sie: __mirgen__?")
            last = datetime.datetime.now()
            return
        
#this is executed on startup
@bot.event
async def on_ready():
    global mirn, megauser, admin, manager, faqmsgchan, faqdm, internal

    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await GameChanger()
    dhserv = fetchServer(137246928227270656)
    mirn = dcf.fetchEmoji(dhserv, mirnemoji)
    megauser = dcf.fetchRole(dhserv, "LAN.megauser")
    admin = dcf.fetchRole(dhserv, "Certified Admin")
    manager = dcf.fetchRole(dhserv, "Certified Manager")
    faqmsgchan = bot.get_channel(faqcid)
    internal = bot.get_channel(intid)
    faqdm = dcf.fetchUser(dhserv, faquid)
    await DownTime()

bot.run(TOKEN, bot=True, reconnect=True)
