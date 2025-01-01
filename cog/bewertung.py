import discord
from discord.ext import commands
from discord import Option, slash_command
import ezcord
import sqlite3

emoji = "<:terra_yes:1260178411792633967>"
channel_id = 1312488122784813157  # Zielkanal-ID
channel_server_id = 1312845604279550082  # Serverbewertung-Kanal-ID

class BewertungsSystem(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "server_config.db"
        self.create_database()
    @slash_command(description="Bewerte unsere Bots")
    async def bewertung_bots(
        self,
        ctx,
        bot: Option(choices=["Manager Bot", "RadioBot", "OPPRO.NET Development Bot"]),
        bewertung: Option(str),
        sterne: Option(choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]),
    ):
        embed_user = discord.Embed(
            title="✅ | Deine Bewertung wurde gesendet",
            color=discord.Color.green(),
        )
        embed_user.add_field(name="🤖 | Für", value=f"{bot}", inline=False)
        embed_user.add_field(name="🤵 | Von wem", value=f"{ctx.author}", inline=False)
        embed_user.add_field(
            name="⭐ | Bewertung", value=f"{bewertung}\nSterne: {sterne}", inline=False
        )
        await ctx.respond(embed=embed_user, ephemeral=True)
        embed_channel = discord.Embed(
            title="Neue Bewertung",
            color=discord.Color.blue(),
        )
        embed_channel.add_field(name="🤖 | Für", value=f"{bot}", inline=False)
        embed_channel.add_field(name="🤵 | Bewertung von", value=f"{ctx.author}", inline=False)
        embed_channel.add_field(
            name="⭐ | Bewertung", value=f"{bewertung}\nSterne: {sterne}", inline=False
        )

        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed_channel)
        else:
            print("Kanal nicht gefunden")

    def create_database(self):
        # Datenbank initialisieren
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS server_config (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def set_channel(self, guild_id, channel_id):
        # Kanal in der Datenbank setzen
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO server_config (guild_id, channel_id)
            VALUES (?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET channel_id = excluded.channel_id
        """, (guild_id, channel_id))
        conn.commit()
        conn.close()

    def get_channel(self, guild_id):
        # Kanal aus der Datenbank abrufen
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT channel_id FROM server_config WHERE guild_id = ?", (guild_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    @slash_command(description="Konfiguriere den Kanal für Serverbewertungen.")
    async def config(
            self,
            ctx,
            channel: Option(discord.TextChannel, "Wähle den Kanal aus, in dem Bewertungen gepostet werden.")
    ):
        self.set_channel(ctx.guild.id, channel.id)
        await ctx.respond(
            f"Der Kanal für Bewertungen wurde erfolgreich auf {channel.mention} gesetzt!",
            ephemeral=True
        )

    @slash_command(description="Bewerte unseren Server")
    async def bewertung_server(
            self,
            ctx,
            bewertung: Option(str, "Gib deine Bewertung ab"),
            sterne: Option(str, "Bewerte mit Sternen", choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]),
            user: Option(str, "Möchtest du angezeigt werden?", choices=["Yes", "No"], default="No")
    ):
        # Embed für den User
        user_embed = discord.Embed(
            title="Deine Bewertung ist raus!",
            color=discord.Color.red(),
        )
        user_embed.set_footer(text="Projekt des OPPRO.NET Development")
        await ctx.respond(embed=user_embed, ephemeral=True)

        # Bewertungssender Information
        user_info = f"**Bewertet von:** {ctx.author.name}" if user == "Yes" else "**Bewertet von:** Anonym"

        # Embed für den Bewertungs-Kanal
        channel_embed = discord.Embed(
            title="Neue Server Bewertung!",
            color=discord.Color.red(),
        )
        channel_embed.add_field(name="Von wem:", value=f"{user_info}", inline=False)
        channel_embed.add_field(name="Bewertung:", value=f"{bewertung}", inline=False)
        channel_embed.add_field(name="Sterne:", value=f"{sterne}", inline=False)
        channel_embed.set_footer(text="Projekt des OPPRO.NET Development | Powered by OPPRO.NET")

        # Kanal-ID aus der Datenbank abrufen
        channel_id = self.get_channel(ctx.guild.id)

        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.send(embed=channel_embed)
            else:
                await ctx.respond(
                    "Der konfigurierte Kanal konnte nicht gefunden werden. Bitte überprüfe die Einstellungen.",
                    ephemeral=True
                )
        else:
            await ctx.respond(
                "Es wurde kein Kanal für Bewertungen konfiguriert. Bitte nutze `/config`, um einen Kanal festzulegen.",
                ephemeral=True
            )

def setup(bot):
    bot.add_cog(BewertungsSystem(bot))
