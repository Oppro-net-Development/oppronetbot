import discord
from discord.ext import commands
from discord import slash_command, Option, SlashCommandGroup
import ezcord

class FModeration(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot

    fun = SlashCommandGroup("fun", "Fun commands")

    @fun.command()
    async def f_ban(self, ctx, user: Option(discord.Member, "User"), reason: Option(str, "Reason")):
        await ctx.respond(f"User {user} was banned for {reason}")

    @fun.command()
    async def f_kick(self, ctx, user: Option(discord.Member, "User"), reason: Option(str, "Reason")):
        await ctx.respond(f"User {user} was kicked for {reason}")

    @fun.command()
    async def f_mute(self, ctx, user: Option(discord.Member, "User"), reason: Option(str, "Reason")):
        await ctx.respond(f"User {user} was muted for {reason}")

    @fun.command()
    async def f_unmute(self, ctx, user: Option(discord.Member, "User"), reason: Option(str, "Reason")):
        await ctx.respond(f"User {user} was unmuted for {reason}")

    @fun.command()
    async def f_warn(self, ctx, user: Option(discord.Member, "User"), reason: Option(str, "Reason")):
        await ctx.respond(f"User {user} was warned for {reason}")

def setup(bot):
    bot.add_cog(FModeration(bot))