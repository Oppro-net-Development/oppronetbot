from discord.commands import SlashCommandGroup
from discord.ext import commands
import discord


class Button(discord.ui.View):
    @discord.ui.button(label="Links", style=discord.ButtonStyle.primary)
    async def button_callback(self, ctx: discord.ApplicationContext, interactions):
        embed = discord.Embed(
            title="Hier sind die Links",
            color=discord.Color.red()
        )
        embed.set_author(name="Oppro.net GmbH")
        embed.add_field(
            name="Links:",
            value="https://discord.gg/codingkeks\n"
                  "https://discord.gg/3rbVWaRTpD"
        )
        embed.set_footer(text="Projekt des Oppro.net Development")

        await interactions.response.send_message(embed=embed)


class Infos(commands.Cog):
    allgemein = SlashCommandGroup("allgemein")

    def __init__(self, bot):
        self.bot = bot

    @allgemein.command(description="Informationen")
    async def infos(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Informationen für den Bot",
            color=discord.Color.red()
        )
        embed.set_author(name="OPPRO.NET GmbH")
        embed.add_field(name="Coder", value="Coder: LennyPegauOfficial und Oppro.net Development")
        embed.add_field(name="Name: OPPRO.NET Manage", value="", inline=False)
        embed.add_field(
            name="Codes:",
            value="Admin Tools - from CodingKeks\n"
                  "ucreatepassword - from CodingKeks\n"
                  "Feedback - From Oppro.net Development\n"
                  "infos - From Oppro.net Development\n"
                  "news - From Oppro.net Development\n"
                  "status - From Oppro.net Development\n"
                  "timeout - From Codingkeks\nuserinfo - from Codingkeks"
        )
        embed.add_field(name="Rechte: ", value="Admin", inline=False)
        embed.set_footer(text="Projekt des Oppro.net Development")

        await ctx.respond(embed=embed, view=Button())

    @allgemein.command(description="Erhalte einen link zum Support Server!")
    async def support(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Unser Support Server",
            color=discord.Color.red()
        )
        embed.set_author(name="Oppro.net GmbH")
        embed.add_field(name="Link: https://discord.gg/k38huukRcB", value="")
        embed.set_footer(text="Projekt des Oppro.net Development")

        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Infos(bot))
