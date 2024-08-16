from discord import slash_command
from discord.ext import commands
import discord


class DeadChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="dead-chat")
    @discord.default_permissions(administrator=True)
    async def dead_chat(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="DeathChat",
            description="Schreibt bitte mehr, dass würde uns freuen.\nVielen Dank!",
            color=discord.Color.red()
        )

        await ctx.respond("@everyone", embed=embed, allowed_mentions=discord.AllowedMentions.all())
        await ctx.respond("Dead-Chat wurde gesendet", ephemeral=True)


def setup(bot):
    bot.add_cog(DeadChat(bot))
