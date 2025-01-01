import discord
from discord.ext import commands
from discord import slash_command, Option
import ezcord

class ServerInfo(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def serverinfo(self, ctx):
        # Serverinformationen mit Embed darstellen
        guild = ctx.guild  # Der Server (Guild), in dem der Befehl ausgeführt wurde
        embed = discord.Embed(
            title=f"Server Infos für {guild.name}",  # Nutze den Servernamen
            color=discord.Color.red()
        )
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=False)
        embed.add_field(name="👤 Mitgliederzahl", value=guild.member_count, inline=False)
        embed.add_field(name="📅 Erstellt am", value=guild.created_at.strftime("%d.%m.%Y"), inline=False)
        embed.add_field(name="👑 Besitzer", value=guild.owner, inline=False)
        embed.add_field(name="🔒 Verifizierungsstufe", value=guild.verification_level, inline=False)
        embed.add_field(name="🔊 Anzahl der Textkanäle", value=len(guild.text_channels), inline=False)
        embed.add_field(name="🔊 Anzahl der Sprachkanäle", value=len(guild.voice_channels), inline=False)
        embed.add_field(name="📊 Anzahl der Rollen", value=len(guild.roles), inline=False)
        embed.add_field(name="📊 Anzahl der Emojis", value=len(guild.emojis), inline=False)
        embed.set_footer(text="Projekt des OPPRO.NET Development")

        # Sende das Embed
        await ctx.respond(embed=embed)


    @slash_command()
    async def userinfo(self, ctx, user: discord.Member):
        # Userinformationen mit Embed darstellen
        embed = discord.Embed(
            title=f"User Infos für {user.name}",  # Nutze den Usernamen
            color=discord.Color.red()
        )
        embed.add_field(name="🆔 User ID", value=user.id, inline=False)
        # Beitreten des Servers
        embed.add_field(name="📅 Beigetreten am", value=user.joined_at.strftime("%d.%m.%Y"), inline=False)
        # Accounterstellung
        embed.add_field(name="📅 Account erstellt am", value=user.created_at.strftime("%d.%m.%Y"), inline=False)
        # Rollen
        # Status
        embed.add_field(name="🟢 Status", value=user.status, inline=False)
        # Aktivität
        embed.add_field(name="🎮 Aktivität", value=user.activity, inline=False)
        embed.set_footer(text="Projekt des OPPRO.NET Development")

        await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(ServerInfo(bot))