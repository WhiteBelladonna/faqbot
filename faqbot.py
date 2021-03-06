import discord
import aiohttp
import filehandler as io
import discordutils as dcf
import parseutils as pu
import scraper as sc
import datetime

import time
import random
import bs4 as bs
from discord.ext import commands

prefixes = ["d!", "f!", "fe!"]
bot = commands.Bot(command_prefix=prefixes)
bot.remove_command("help")


#define the filepaths (#1 for local testing, #2 for server use)

#filepath = 'E:/Coding/Python/faqbot/files/' 
filepath = './files/'

#open the commands xml
root = io.readXML(filepath,'data.xml')

#ids for dreamhack int color code and faq channel, as well as permission denied message
dhorange = 16738079
faqchannel = "<#376765597226106890>"
authfailed = "I\'m sorry Dave, I\'m afraid I can\'t do that."
unknown_de = "Den Befehl kenne ich leider nicht. Schau doch mal in meiner Befehlsübersicht nach:"
unknown_en = "I don't recognize that command. Try checking my commandlist:"
mirnemoji = "DHCactus"
mirnchance = 40
msgchan = 137246928227270656
faqcid = 484264883169525760



#initialize users and emoji
mirn = None
megauser = None
admin = None
manager = None
faqdm = None
faqmsgchan = None
messagechannel = None
dhserv = None



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



#define the different commands
@bot.command(name="shutdown")
async def shutdown(ctx):
    if ctx.prefix == "d!":
        if ctx.author.id == ADMIN:
            await ctx.send("Ja Meister.")
            await bot.close()
        else:
            await ctx.message.channel.send(authfailed)
            print(str(ctx.author) + " tried to access command d!shutdown!")
            return


@bot.command(name="help")
async def help(ctx):
    if ctx.prefix == "f!":
        embed = dcf.helpDE(help_de)
        await ctx.send(" ", embed=embed)
        return
    elif ctx.prefix == "fe!":
        embed = dcf.helpEN(help_en)
        await ctx.send(" ", embed=embed)
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


@bot.command(name="aq")
async def aq(ctx, arg1):
    if ctx.prefix == "f!":
        gmsg = str(arg1)
        gmsg = pu.parseTXT(gmsg)
        ph = pu.checkComm(comm_de, gmsg)
        if ph != False:
            embed = dcf.FAQ(q_de[ph], a_de[ph], dhorange)
            await ctx.send(" ",embed=embed)
            return
        else: 
            # if none is found, return an error and show all available commands
            embed = dcf.helpDE(help_de)
            await ctx.send(unknown_de, embed=embed)
            print(str(ctx.message.author)+ " used an unknown command (" +str(ctx.message.content)+")")
            return
    if ctx.prefix == "fe!":
        emsg = str(arg1)
        emsg = pu.parseTXT(emsg)
        ph = pu.checkComm(comm_en, emsg)
        if ph != False:
            embed = dcf.FAQENG(q_en[ph], a_en[ph], dhorange)
            await ctx.send(" ",embed=embed)
            return
        else: 
            # if none is found, return an error and show all available commands
            embed = dcf.helpEN(help_en)
            await ctx.send(unknown_en, embed=embed)
            print(str(ctx.message.author)+ " used an unknown command (" +str(ctx.message.content)+")")
            return


@bot.command(name="mirn")
async def minn(ctx):
    if ctx.prefix == "d!":
        embed = discord.Embed(color=dhorange)
        dcf.addEmbed(embed, "Mirns im Welcome: ", mc)
        await ctx.message.channel.send(" ", embed=embed)  


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
        if rnd < mirnchance:
            await message.add_reaction(mirn)
        return    
            
               
#this is executed on startup
@bot.event
async def on_ready():
    global mirn, megauser, admin, manager

    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await GameChanger()
    global dhserv, mirn, megauser, admin, manager, faqmsgchan, faqdm
    dhserv = fetchServer(137246928227270656)
    mirn = dcf.fetchEmoji(dhserv, mirnemoji)
    megauser = dcf.fetchRole(dhserv, "LAN.megauser")
    admin = dcf.fetchRole(dhserv, "Certified Admin")
    manager = dcf.fetchRole(dhserv, "Certified Manager")
    faqmsgchan = bot.get_channel(faqcid)
    faqdm = dcf.fetchUser(dhserv, faquid)

bot.run(TOKEN, bot=True, reconnect=True)
