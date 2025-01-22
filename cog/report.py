import discord
from discord.ext import commands
from discord import slash_command, Option
import ezcord
import json


class ReportSystem(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns_file = "report_channels.json"

        # Lade bestehende Daten oder erstelle eine leere Struktur
        try:
            with open(self.warns_file, 'r') as f:
                self.report_channels = json.load(f)
        except FileNotFoundError:
            self.report_channels = {}

    async def save_report_channels(self):
        # Speichert die Report-Kanäle in einer JSON-Datei
        with open(self.warns_file, 'w') as f:
            json.dump(self.report_channels, f, indent=4)

    @slash_command(name="report_channel", description="Setzt einen Channel für Reports")
    async def set_report_channel(self, ctx, channel: Option(discord.TextChannel, "Wähle den Channel für Reports")):
        guild_id = str(ctx.guild.id)

        # Falls der Server noch nicht in der Datenbank ist, füge ihn hinzu
        if guild_id not in self.report_channels:
            self.report_channels[guild_id] = {}

        # Setze den Report-Channel
        self.report_channels[guild_id]["channel"] = channel.id
        await self.save_report_channels()

        # Bestätigung
        await ctx.send(f"Der Report-Kanal wurde auf {channel.mention} gesetzt.")

    @slash_command(name="get_report_channel", description="Zeigt den aktuell gesetzten Report-Channel")
    async def get_report_channel(self, ctx):
        guild_id = str(ctx.guild.id)

        # Überprüfen, ob der Report-Channel existiert
        if guild_id in self.report_channels and "channel" in self.report_channels[guild_id]:
            channel_id = self.report_channels[guild_id]["channel"]
            channel = self.bot.get_channel(channel_id)
            await ctx.send(f"Der aktuelle Report-Channel ist: {channel.mention}")
        else:
            await ctx.send("Es wurde noch kein Report-Channel gesetzt.")

    @slash_command(name="report", description="Melde einen Vorfall in einem Report-Channel")
    async def report(self, ctx, reason: Option(str), user: Option(discord.Member)):
        guild_id = str(ctx.guild.id)

        # Überprüfen, ob der Report-Channel existiert
        if guild_id in self.report_channels and "channel" in self.report_channels[guild_id]:
            channel_id = self.report_channels[guild_id]["channel"]
            channel = self.bot.get_channel(channel_id)

            # Sicherstellen, dass der Kanal existiert
            if channel:
                await channel.send(f"**Neuer Report**\n\nUser: {user}\nGrund: {reason}")
                await ctx.send("Dein Report wurde erfolgreich eingereicht.")
            else:
                await ctx.send("Der Report-Channel konnte nicht gefunden werden.")
        else:
            await ctx.send("Es wurde kein Report-Channel gesetzt. Bitte setze einen mit `/report_channel`.")


def setup(bot):
    bot.add_cog(ReportSystem(bot))
