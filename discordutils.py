import discord

#initialize the client
client = discord.Client()
dhorange = 16738079

#returns a specific emoji object from a server
def fetchEmoji(server, name):
    emoji = discord.utils.get(server.emojis, name=name)
    print(str(emoji.name)+"-Emoji loaded from server: " +str(server.name))
    return emoji

#returns a specific role object from a server
def fetchRole(server, name):
    role = discord.utils.get(server.roles, name=name)
    print(str(role.name) + "-Role loaded from server: " + str(server.name))
    return role

def fetchUser(server, uid):
    user = discord.utils.get(server.members, id=uid)
    print(str(user) + "-Loaded from Server: " + str(server.name)+" as FAQ Target")
    return user

#adds a field to a given embed
def addEmbed(embed, name, value):
    embed.add_field(name=name, value=value, inline=False)
    return embed

#generates a footer for a given embed
def footerGen(embed):
    embed.set_footer(text="FAQBot created by Demolite®")
    return embed

#creates a German FAQ embed object
def FAQ(question, answer, color):
    embed = discord.Embed(color=color)
    embed.add_field(name="Frage:", value=question, inline=False)
    embed.add_field(name="Antwort:", value=answer, inline=False)
    return embed

#creates an English FAQ embed object
def FAQENG(question, answer, color):
    embed = discord.Embed(color=color)
    embed.add_field(name="Question:", value=question, inline=False)
    embed.add_field(name="Answer:", value=answer, inline=False)
    return embed

#generate help messages
def helpDE(help_de):
    embed = discord.Embed(color=dhorange)
    embed.add_field(name="FAQ Befehl:", value="f!aq + Suchwort", inline=False)
    embed.add_field(name="Suchworte:", value=help_de, inline=False)
    embed.add_field(name="Feedback Einreichen:", value="f!eedback + _kompletter_ feedback Text", inline=False)
    embed.add_field(name="English Commands:", value="Type fe!help", inline=False)
    footerGen(embed)
    return embed

def helpEN(help_en):
    embed = discord.Embed(color=dhorange)
    embed.add_field(name="FAQ Command:", value="fe!aq + Keyword", inline=False)
    embed.add_field(name="Keywords:", value=help_en, inline=False)
    embed.add_field(name="Leave some Feedback:", value="f!eedback + _complete_ feedback text", inline=False)
    footerGen(embed)
    return embed