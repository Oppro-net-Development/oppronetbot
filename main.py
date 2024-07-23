import discord
from dotenv import load_dotenv
import datetime
import platform
from discord import slash_command, Option
from discord.ext import commands, tasks
import psutil
import ezcord
import logging
import yaml
import os
from ownimport import modul as m
# #################################################################################################################### #

intents = discord.Intents.default()
intents.members = True  # Stelle sicher, dass du die richtigen Intents für mitgliederbezogene Ereignisse hast'
intents.messages = True
intents.guilds = True  # Für den Zugriff auf Server-Informationen
intents.guild_messages = True  # Für Zugriff auf Kanal-Informationen
load_dotenv()
# #################################################################################################################### #
with open("de.yaml", encoding="utf-8") as file:
    de = yaml.safe_load(file)

with open("en.yaml", encoding="utf-8") as file:
    en = yaml.safe_load(file)

ezcord.set_log(
    log_level=logging.DEBUG,
    discord_log_level=logging.WARNING,
    webhook_url=(os.getenv("LOGWEBHOCK"))
)
# #################################################################################################################### #
bot = ezcord.Bot(
    intents=intents,
    language="de" "en",
    error_webhook_url=(os.getenv("ERRORWEBHOCK")),
    debug_guilds=[1097205376740499466, 1256172504020684894, 1260715725451038833]
)
# #################################################################################################################### #
USER_ID = 1093555256689959005
last_message_id = None
start_time = datetime.datetime.utcnow()


@bot.event
async def on_ready():
    global last_message_id
    user = bot.get_user(USER_ID)

    if user is not None:
        uptime = datetime.datetime.utcnow() - start_time

        embed = discord.Embed(title="Bot Informationen", color=0x00ff00)
        embed.add_field(name="Name", value=bot.user.name, inline=False)
        embed.add_field(name="ID", value=bot.user.id, inline=False)
        embed.add_field(name="Status", value=str(bot.status).title(), inline=True)
        embed.add_field(name="Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Members", value=len(set(bot.get_all_members())), inline=True)
        embed.add_field(name="Channels", value=sum(len(guild.channels) for guild in bot.guilds), inline=True)
        embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
        embed.add_field(name="Coder", value="LennyPegauOfficial", inline=True)  # Deinen Namen hier einfügen
        embed.add_field(name="Bot-Version", value="1.0.0", inline=True)  # Deine Bot-Version hier einfügen
        embed.add_field(name="Beschreibung", value="Ein multifunktionaler Bot für Discord.",
                        inline=False)  # Beschreibung des Bots hier einfügen
        embed.add_field(name="Erstellt am", value=bot.user.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
        embed.add_field(name="Python-Version", value=platform.python_version(),
                        inline=True)  # Zeigt die Python-Version an
        embed.add_field(name="Aktuelle Zeit", value=datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S UTC"),
                        inline=True)  # Zeigt die aktuelle UTC-Zeit an

        # Hole den DM-Kanal des Nutzers
        dm_channel = await user.create_dm()

        if last_message_id:
            try:
                # Versuche, die bestehende Nachricht zu bearbeiten
                message = await dm_channel.fetch_message(last_message_id)
                await message.edit(embed=embed)
                print("Nachricht erfolgreich aktualisiert.")
            except discord.NotFound:
                # Nachricht wurde nicht gefunden, sende eine neue Nachricht
                sent_message = await dm_channel.send(embed=embed)
                last_message_id = sent_message.id
                print(f"Neue Nachricht gesendet. ID: {last_message_id}")
            except discord.Forbidden:
                print("Der Bot hat keine Berechtigung, die Nachricht zu bearbeiten.")
            except discord.HTTPException as e:
                print(f"HTTPException: {e}")
        else:
            try:
                # Sende eine neue Nachricht
                sent_message = await dm_channel.send(embed=embed)
                last_message_id = sent_message.id
                print(f"Nachricht erfolgreich gesendet. ID: {last_message_id}")
            except discord.Forbidden:
                print("Der Bot hat keine Berechtigung, Nachrichten an diesen Benutzer zu senden.")
            except discord.HTTPException as e:
                print(f"HTTPException: {e}")
# #################################################################################################################### #
YOUR_SERVER_ID = 1097205376740499466

YOUR_CHANNEL_ID = 1265387822521516062

@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    if owner:
        embed = discord.Embed(
            title=f'Ich bin dem Server __{guild.name}__ beigetreten',
            color=discord.Color.red()
        )
        embed.add_field(name='Inhaber', value=owner.name, inline=False)
        embed.add_field(name='Mitglieder', value=guild.member_count, inline=False)
        embed.add_field(name='Bots', value=len([member for member in guild.members if member.bot]), inline=False)
        embed.add_field(name='Rollenanzahl', value=len(guild.roles), inline=False)
        embed.add_field(name='Channelsanzahl', value=len(guild.channels), inline=False)
        embed.set_footer(text='Weitere Informationen folgen...')

        try:
            await owner.send(embed=embed)
        except discord.Forbidden:
            print(f'Konnte keine DM an den Besitzer {owner.name} senden.')

    my_server = bot.get_guild(YOUR_SERVER_ID)
    if my_server:
        my_channel = my_server.get_channel(YOUR_CHANNEL_ID)
        if my_channel:
            server = discord.Embed(
                title=f'Neuer Serverbeitritt: {guild.name}',
                color=discord.Color.blue()
            )
            server.add_field(name='Inhaber', value=owner.name, inline=False)
            server.add_field(name='Mitglieder', value=guild.member_count, inline=False)
            server.add_field(name='Bots', value=len([member for member in guild.members if member.bot]), inline=False)
            server.add_field(name='Rollenanzahl', value=len(guild.roles), inline=False)
            server.add_field(name='Channelsanzahl', value=len(guild.channels), inline=False)
            await my_channel.send(embed=server)
# #################################################################################################################### #
bot.add_help_command()

if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


    bot.localize_commands(de, en)

# #################################################################################################################### #

Authors = "LennyPegauOffical", "OPPRO.NET Team", "OPPRO.NET Development"
print(f"[Authors]  {Authors}")
bot.run(os.getenv("TOKEN"))
