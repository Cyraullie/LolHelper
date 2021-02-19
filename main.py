# main.py

import os


from discord.ext import commands
import discord

TOKEN = 'NzI1NzczMTE0MTg5MDIxMzI0.XvTm4g.txkPRzX2Q6R5J-iPUxBEzermQNs'

bot = commands.Bot(command_prefix = "*", description = "test de merde")

@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou <@&725785724741484585> !")
    
    
@bot.command()
async def serverInfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberofVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le server **{serverName}** countient {numberOfPerson} personnes. \n La description du serveur : {serverDescription}. \n Ce serveur possède {numberOfTextChannels} salons écrits ainsi que {numberofVoiceChannels} vocaux."
    
    await ctx.send(message)

@bot.command()
async def recherche(ctx, NbPersonne, Attente):

    await ctx.send(f"Yo <@&725785724741484585>, je suis avec {int(NbPersonne)} personnes et nous vous attendrons pendant {int(Attente)} minutes votre message alors bougez-vous !")

    
@bot.command()
async def jarrive(ctx, Heure, Minutes):

    await ctx.send(f"Yo <@&725785724741484585>, j'arrive vers {int(Heure)} h {int(Minutes)} !")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)
