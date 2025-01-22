import discord
from discord.ext import commands
from discord import slash_command, Option, SlashCommandGroup
import ezcord
import aiosqlite

class Notizen(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Sicherstellen, dass die Datenbank beim Start des Bots eingerichtet wird
        self.bot.loop.create_task(self.setup_database())

    # Datenbank Vervindung und erstellen aufbauen
    async def setup_database(self):
        try:
            self.db = await aiosqlite.connect("notizen.db")
            await self.db.execute("""
                CREATE TABLE IF NOT EXISTS notizen (
                    user_id INTEGER,
                    guild_id INTEGER,
                    notiz TEXT,
                    PRIMARY KEY (user_id, guild_id)
                )
            """)
            await self.db.commit()
            print("Datenbank und Tabelle wurden erfolgreich eingerichtet.")
        except Exception as e:
            print(f"Fehler bei der Einrichtung der Datenbank: {e}")

    notizen = SlashCommandGroup("notizen", "Gebe einen User Notizen")

    # Slash Command für Erstellen von Notizen für User
    @notizen.command(description="Erstelle eine Notiz für einen User")
    @discord.default_permissions(manage_messages=True)
    async def create(self, ctx, user: discord.Member, notiz: str):
        await ctx.respond(f"Die Notiz für {user.mention} wurde erstellt.", ephemeral=True)
        async with aiosqlite.connect("notizen.db") as db:
            await db.execute("""
                INSERT INTO notizen (user_id, guild_id, notiz)
                VALUES (?, ?, ?)
            """, (user.id, ctx.guild.id, notiz))
            await db.commit()

    # View
    @notizen.command(description="Zeige alle Notizen für einen User")
    @discord.default_permissions(manage_messages=True)
    async def view(self, ctx, user: discord.Member):
        async with aiosqlite.connect("notizen.db") as db:
            async with db.execute("""
                SELECT notiz FROM notizen WHERE user_id = ? AND guild_id = ?
            """, (user.id, ctx.guild.id)) as cursor:
                row = await cursor.fetchone()

        if not row:
            await ctx.respond("Es gibt keine Notizen für diesen User.", ephemeral=True)
            return

        await ctx.respond(f"Notizen für {user.mention}:\n{row[0]}")

    # Löschen
    @notizen.command(description="Lösche alle Notizen für einen User")
    @discord.default_permissions(manage_messages=True)
    async def delete(self, ctx, user: discord.Member):
        await ctx.respond(f"Die Notizen für {user.mention} wurden gelöscht.", ephemeral=True)
        async with aiosqlite.connect("notizen.db") as db:
            await db.execute("""
                DELETE FROM notizen WHERE user_id = ? AND guild_id = ?
            """, (user.id, ctx.guild.id))
            await db.commit()

def setup(bot):
    bot.add_cog(Notizen(bot))
