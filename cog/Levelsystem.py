import discord
from discord.ext import commands
from discord import slash_command, Option
import ezcord
import aiosqlite
from discord.ext.pages import Paginator

class LevelSystem(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("level_system.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS level_system (
                    user_id INTEGER,
                    guild_id INTEGER,
                    level INTEGER DEFAULT 1,
                    xp INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, guild_id)
                )
            """)
            await db.commit()

    @slash_command(description="Zeigt das Leaderboard für den Server oder global an.")
    async def leaderboard(self, ctx, leaderboard_type: Option(str, "Wähle das Leaderboard", choices=["Global", "Server"])):
        if leaderboard_type == "Server":
            await self.show_server_leaderboard(ctx)
        else:
            await self.show_global_leaderboard(ctx)

    async def show_server_leaderboard(self, ctx):
        async with aiosqlite.connect("level_system.db") as db:
            async with db.execute("""
                SELECT user_id, level, xp FROM level_system WHERE guild_id = ?
                ORDER BY xp DESC
            """, (ctx.guild.id,)) as cursor:
                rows = await cursor.fetchall()

        if not rows:
            await ctx.respond("Das Server Leaderboard ist noch leer.")
            return

        pages = []
        for i in range(0, len(rows), 10):  # 10 Einträge pro Seite
            embed = discord.Embed(title=f"🏆 Server Leaderboard für {ctx.guild.name}", color=discord.Color.blue())
            for idx, row in enumerate(rows[i:i + 10], start=i + 1):
                user_id, level, xp = row
                user = await self.bot.fetch_user(user_id)
                embed.add_field(name=f"{idx}. {user.name}", value=f"Level: {level} - XP: {xp}", inline=False)
            pages.append(embed)

        paginator = Paginator(pages=pages, show_disabled=True, show_indicator=True, timeout=120)
        await paginator.respond(ctx.interaction, ephemeral=False)

    async def show_global_leaderboard(self, ctx):
        async with aiosqlite.connect("level_system.db") as db:
            async with db.execute("""
                SELECT user_id, level, xp FROM level_system
                ORDER BY xp DESC
            """) as cursor:
                rows = await cursor.fetchall()

        if not rows:
            await ctx.respond("Das globale Leaderboard ist noch leer.")
            return

        pages = []
        for i in range(0, len(rows), 10):  # 10 Einträge pro Seite
            embed = discord.Embed(title="🏆 Globales Leaderboard", color=discord.Color.green())
            for idx, row in enumerate(rows[i:i + 10], start=i + 1):
                user_id, level, xp = row
                user = await self.bot.fetch_user(user_id)
                embed.add_field(name=f"{idx}. {user.name}", value=f"Level: {level} - XP: {xp}", inline=False)
            pages.append(embed)

        paginator = Paginator(pages=pages, show_disabled=True, show_indicator=True)
        await paginator.respond(ctx.interaction, ephemeral=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        async with aiosqlite.connect("level_system.db") as db:
            async with db.execute("""
                SELECT user_id, xp FROM level_system WHERE user_id = ? AND guild_id = ?
            """, (message.author.id, message.guild.id)) as cursor:
                result = await cursor.fetchone()

                if result:
                    user_id, xp = result
                    xp += 10
                    level = xp // 100
                    await db.execute("""
                        UPDATE level_system SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?
                    """, (xp, level, message.author.id, message.guild.id))
                else:
                    await db.execute("""
                        INSERT INTO level_system (user_id, guild_id, level, xp) VALUES (?, ?, ?, ?)
                    """, (message.author.id, message.guild.id, 1, 10))
                await db.commit()

def setup(bot):
    bot.add_cog(LevelSystem(bot))
