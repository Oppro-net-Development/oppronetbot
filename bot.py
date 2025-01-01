import discord
from discord.ext.commands import Cog
from discord.commands import slash_command
import platform

radio_invite_url = "https://discord.com/oauth2/authorize?client_id=1249695881494794301&permissions=40136535442176&integration_type=0&scope=bot"
github = "https://github.com/Oppro-net-Development"
website = "https://oppronet.netlify.app/"
class BotInfo(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Zeigt Informationen über den Bot.")
    async def botinfo(self, ctx):
        # Bot-Details
        bot_name = self.bot.user.name
        bot_id = self.bot.user.id
        bot_creator = "OPPRO.NET Development, LennyPegauOfficial"  # Dein Name oder Benutzername
        bot_guilds = len(self.bot.guilds)
        bot_members = sum(guild.member_count for guild in self.bot.guilds)
        bot_commands = len(self.bot.application_commands)

        # Systeminformationen
        python_version = platform.python_version()
        discord_version = discord.__version__
        os_info = platform.system() + " " + platform.release()

        # Text-, Sprachkanäle und Rollen zählen
        total_text_channels = sum(len(guild.text_channels) for guild in self.bot.guilds)
        total_voice_channels = sum(len(guild.voice_channels) for guild in self.bot.guilds)
        total_roles = sum(len(guild.roles) for guild in self.bot.guilds)
        total_emojis = sum(len(guild.emojis) for guild in self.bot.guilds)
        total_categories = sum(len(guild.categories) for guild in self.bot.guilds)

        # Embed erstellen
        embed = discord.Embed(
            title=f"{bot_name} - Informationen",
            color=discord.Color.blue(),
            description="Hier findest du alle wichtigen Infos zu diesem Bot."
        )

        # Bot-Informationen mit Emojis
        embed.add_field(name="🤖 Bot-Name", value=f"{bot_name}", inline=False)
        embed.add_field(name="🆔 Bot-ID", value=f"{bot_id}", inline=True)
        embed.add_field(name="👨‍💻 Ersteller", value=f"{bot_creator}", inline=False)
        embed.add_field(name="🌍 Server", value=f"{bot_guilds}", inline=True)
        embed.add_field(name="👥 Nutzer (geschätzt)", value=f"{bot_members:,}", inline=False)
        embed.add_field(name="🔧 Befehle", value=f"{bot_commands}", inline=True)
        embed.add_field(name="📅 Beschreibung", value="mit")

        # Systeminformationen mit Emojis
        embed.add_field(name="🐍 Python-Version", value=f"{python_version}", inline=False)
        embed.add_field(name="💬 Py-cord-Version", value=f"{discord_version}", inline=True)
        embed.add_field(name="🖥️ Betriebssystem", value=f"{os_info}", inline=True)

        # Serverweite Statistiken
        embed.add_field(name="📡 Textkanäle", value=f"{total_text_channels}", inline=True)
        embed.add_field(name="🔊 Sprachkanäle", value=f"{total_voice_channels}", inline=True)
        embed.add_field(name="📊 Rollen", value=f"{total_roles}", inline=True)
        embed.add_field(name="😀 Emojis", value=f"{total_emojis}", inline=True)
        embed.add_field(name="📂 Kategorien", value=f"{total_categories}", inline=True)

        # BESCHREIBUNG
        embed.add_field(name="📝 **Beschreibung**",
                        value=  "\n"
                              "<:info:1323251278586970166> **Über mich**\n\n"
                              "<:robot:123456789012345678> Hi, ich bin der **ManagerBot**, dein zuverlässiger Helfer für den Server!\n"
                              "<:sparkles:123456789012345678> Ich sorge für Ordnung, moderate Aktivitäten und biete nützliche Funktionen!\n\n"
                              "<:gear:123456789012345678> Was ich kann:\n"
                              "- <:moderator:1323245317713297448> **Moderation**: Spamschutz, Kick/Ban-Optionen, und mehr!\n"
                              "- <:Stats:1323660840804683816> **Stats**: Server-Statistiken auf einen Blick!\n"
                              "- <:slashcommands:1323243094954475561> **Interaktive Befehle**: Nutze mich für coole Server-Features!\n\n"
                              "<:tada:123456789012345678> Ich freue mich, dir zu helfen!\n",
                        inline=False)

        # Embed Fußzeile und Bild
        embed.set_footer(text="Projekt von OPPRO.NET Development | Powered by Discord")
        embed.set_thumbnail(url=self.bot.user.avatar.url)  # Setzt das Profilbild des Bots als Thumbnail

        # Antwort senden
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(BotInfo(bot))
