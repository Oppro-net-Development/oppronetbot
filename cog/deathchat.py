import discord
from discord.ext import commands
from discord import slash_command, Option

class deathchat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @discord.default_permissions(administrator=True)
    async def deathchat(self, ctx):

        embed = discord.Embed(
            title="DeathChat",
            description="DeathChat Schreibe bitte mehr fas würde uns freuen\n Vielen Dank",
            color=discord.Color.red()
        )
        await ctx.respond("<@&1256974368450281564>", embed=embed)
        await ctx.respond("DeathChat wurde gesendet", ephemeral=True)
def setup(bot):
    bot.add_cog(deathchat(bot))