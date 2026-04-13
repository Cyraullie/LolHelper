# main.py

import os
import datetime
import discord
import json
import requests

from discord.ext import commands, tasks
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv(dotenv_path="config")
bot = commands.Bot(command_prefix="*", description="test de merde", intents=intents)

API_KEY = os.getenv("RIOT_API_KEY")

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # ton salon
ROLE_ID = int(os.getenv("ROLE_ID"))  # ton rôle

NOTIFIED_FILE = "notified_clash.json"

def load_notified():
    if not os.path.exists(NOTIFIED_FILE):
        return set()

    with open(NOTIFIED_FILE, "r") as f:
        return set(json.load(f))


def save_notified(data):
    with open(NOTIFIED_FILE, "w") as f:
        json.dump(list(data), f)


@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou salope !")

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
    await ctx.send(f"Yo <@&{ROLE_ID}>, je suis avec {int(NbPersonne)} personnes et nous vous attendrons pendant {int(Attente)} minutes votre message alors bougez-vous !")

@bot.command()
async def jarrive(ctx, Heure, Minutes):
    await ctx.send(f"Yo <@&{ROLE_ID}>, j'arrive vers {int(Heure)} h {int(Minutes)} !")


# 🧠 mémoire des clash déjà annoncés
notified_clash_ids = load_notified()

# 🔎 récupérer les clashs
def get_clash_tournaments():
    url = f"https://euw1.api.riotgames.com/lol/clash/v1/tournaments"
    headers = {"X-Riot-Token": API_KEY}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("Erreur API:", r.text)
        return []

    data = r.json()

    if not isinstance(data, list):
        return []

    return data


# 🧠 conversion timestamp
def ts_to_date(ts):
    return datetime.fromtimestamp(ts / 1000, tz=UTC)


# 🚀 embed stylé
def build_embed(tournoi, schedule):
    start = ts_to_date(schedule["startTime"])
    reg = ts_to_date(schedule["registrationTime"])

    embed = discord.Embed(
        title="🔥 Clash League of Legends",
        description=f"**Mode : {tournoi.get('nameKey')}**",
        color=0xff0000
    )

    embed.add_field(name="📅 Début", value=start.strftime("%Y-%m-%d %H:%M UTC"), inline=False)
    embed.add_field(name="📝 Inscription", value=reg.strftime("%Y-%m-%d %H:%M UTC"), inline=False)
    embed.add_field(name="🆔 ID Tournoi", value=str(tournoi.get("id")), inline=True)
    embed.add_field(name="🎮 Theme", value=str(tournoi.get("themeId")), inline=True)

    embed.set_footer(text="Riot Games Clash System")

    return embed


# 🔁 loop toutes les 30 minutes
@tasks.loop(minutes=30)
async def clash_checker():
    tournaments = get_clash_tournaments()

    channel = bot.get_channel(CHANNEL_ID)
    role_ping = f"<@&{ROLE_ID}>"

    for tournoi in tournaments:
        for schedule in tournoi.get("schedule", []):

            clash_id = schedule.get("id")

            if clash_id in notified_clash_ids:
                continue

            start_time = ts_to_date(schedule["startTime"])

            if start_time > datetime.now(UTC):
                embed = build_embed(tournoi, schedule)

                if channel:
                    await channel.send(content=role_ping, embed=embed)

                notified_clash_ids.add(clash_id)
                save_notified(notified_clash_ids)


# 📅 commande debug
@bot.command()
async def clash(ctx):
    tournaments = get_clash_tournaments()

    if not tournaments:
        await ctx.send("❌ Aucun Clash trouvé.")
        return

    msg = "📅 Clash disponibles :\n"
    for t in tournaments:
        msg += f"- {t.get('nameKey')} (ID {t.get('id')})\n"

    await ctx.send(msg)


@bot.event
async def on_ready():
    print('Le bot est prêt')
    print('------')
    clash_checker.start()

bot.run(os.getenv("TOKEN"))
