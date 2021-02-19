# main.py

import os
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")
bot = commands.Bot(command_prefix = "*", description = "test de merde")

@bot.event
async def on_ready():
    print('Le bot est prêt')
    print('------')



@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou <@&725785724741484585> !")

async def serverInfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberofVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le server **{serverName}** countient {numberOfPerson} personnes. \n La description du serveur : {serverDescription}. \n Ce serveur possède {numberOfTextChannels} salons écrits ainsi que {numberofVoiceChannels} vocaux."
    
    await ctx.send(message)

async def recherche(ctx, NbPersonne, Attente):

    await ctx.send(f"Yo <@&725785724741484585>, je suis avec {int(NbPersonne)} personnes et nous vous attendrons pendant {int(Attente)} minutes votre message alors bougez-vous !")

async def jarrive(ctx, Heure, Minutes):

    await ctx.send(f"Yo <@&725785724741484585>, j'arrive vers {int(Heure)} h {int(Minutes)} !")




bot.run(os.getenv("TOKEN"))
