import discord

#initialize the client
client = discord.Client()


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

#adds a field to a given embed
def addEmbed(embed, name, value):
    embed.add_field(name=name, value=value, inline=False)
    return embed

#generates a footer for a given embed
def Footer(embed):
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
