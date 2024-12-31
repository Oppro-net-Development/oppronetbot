# #################################################################################################################### #
# Creator:
# Last updated: 28.12.2024 (12/28/2024)
# Info: This is an admin system
# This message must not be deleted!
# #################################################################################################################### #

import discord
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup
import json



class AdminSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warns_file = "warns.json"

    moderation = SlashCommandGroup("moderation", "Verwaltungsbefehle")
    # Helper: Lade Warnungen aus der Datei
    def load_warns(self, guild_id):
        try:
            with open(self.warns_file, "r") as f:
                data = json.load(f)
                return data.get(str(guild_id), {})
        except FileNotFoundError:
            return {}

    # Helper: Speichern der Warnungen
    def save_warns(self, guild_id, warns):
        try:
            with open(self.warns_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data[str(guild_id)] = warns

        with open(self.warns_file, "w") as f:
            json.dump(data, f, indent=4)

    # Ban Befehl
    @moderation.command(description="Bannt einen Benutzer.")
    @discord.default_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, reason: str = "Kein Grund angegeben"):
        """Bannt einen Benutzer vom Server."""
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        await user.ban(reason=reason)

        embed = discord.Embed(
            title="🔨 Benutzer gebannt",
            description=f"{user.mention} wurde aus dem Server gebannt. Grund: {reason}",
            color=discord.Color.red()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

        try:
            dm_embed = discord.Embed(
                title="🔨 Du wurdest gebannt",
                description=f"Du wurdest von {ctx.author.mention} gebannt. Grund: {reason}",
                color=discord.Color.red()
            )
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            await ctx.respond(f"Ich kann {user.name} keine DM senden.")

    # Kick Befehl
    @moderation.command(description="Kickt einen Benutzer aus dem Server.")
    @discord.default_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, reason: str = "Kein Grund angegeben"):
        """Kickt einen Benutzer vom Server."""
        if not ctx.author.guild_permissions.kick_members:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        await user.kick(reason=reason)

        embed = discord.Embed(
            title="👢 Benutzer gekickt",
            description=f"{user.mention} wurde aus dem Server gekickt. Grund: {reason}",
            color=discord.Color.orange()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

        try:
            dm_embed = discord.Embed(
                title="👢 Du wurdest gekickt",
                description=f"Du wurdest von {ctx.author.mention} gekickt. Grund: {reason}",
                color=discord.Color.orange()
            )
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            await ctx.respond(f"Ich kann {user.name} keine DM senden.")

    # Warn Befehl
    @moderation.command(description="Warnt einen Benutzer.")
    @discord.default_permissions(manage_messages=True)
    async def warn(self, ctx, user: discord.Member, reason: str = "Kein Grund angegeben"):
        """Warnt einen Benutzer."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        warns = self.load_warns(ctx.guild.id)
        user_id = str(user.id)

        if user_id not in warns:
            warns[user_id] = []
        warns[user_id].append(reason)

        self.save_warns(ctx.guild.id, warns)

        embed = discord.Embed(
            title="⚠️ Benutzer gewarnt",
            description=f"{user.mention} wurde gewarnt. Grund: {reason}",
            color=discord.Color.yellow()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

        try:
            dm_embed = discord.Embed(
                title="⚠️ Du wurdest gewarnt",
                description=f"Du wurdest von {ctx.author.mention} gewarnt. Grund: {reason}",
                color=discord.Color.yellow()
            )
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            await ctx.respond(f"Ich kann {user.name} keine DM senden.")

    # Warn-List Befehl
    @moderation.command(description="Zeigt eine Liste der Warnungen eines Benutzers.")
    @discord.default_permissions(manage_messages=True)
    async def warn_list(self, ctx, user: discord.Member):
        """Zeigt die Liste der Warnungen eines Benutzers an."""
        warns = self.load_warns(ctx.guild.id)
        user_id = str(user.id)
        if user_id not in warns or len(warns[user_id]) == 0:
            embed = discord.Embed(
                title="⚠️ Warnungen",
                description=f"{user.mention} hat keine Warnungen.",
                color=discord.Color.green()
            )
            embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
            return await ctx.respond(embed=embed)

        warn_list = "\n".join(warns[user_id])
        embed = discord.Embed(
            title="⚠️ Warnungen",
            description=f"{user.mention} hat folgende Warnungen:\n{warn_list}",
            color=discord.Color.yellow()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

    # Unwarn Befehl
    @moderation.command(description="Entfernt eine Warnung von einem Benutzer.")
    @discord.default_permissions(manage_messages=True)
    async def unwarn(self, ctx, user: discord.Member, index: int):
        """Entfernt eine Warnung von einem Benutzer."""
        warns = self.load_warns(ctx.guild.id)
        user_id = str(user.id)
        if user_id in warns and len(warns[user_id]) > index:
            del warns[user_id][index]
            self.save_warns(ctx.guild.id, warns)

            embed = discord.Embed(
                title="⚠️ Warnung entfernt",
                description=f"Die Warnung von {user.mention} wurde entfernt.",
                color=discord.Color.green()
            )
            embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
            await ctx.respond(embed=embed)

            try:
                dm_embed = discord.Embed(
                    title="⚠️ Deine Warnung wurde entfernt",
                    description=f"Eine deiner Warnungen wurde von {ctx.author.mention} entfernt.",
                    color=discord.Color.green()
                )
                await user.send(embed=dm_embed)
            except discord.Forbidden:
                await ctx.respond(f"Ich kann {user.name} keine DM senden.")
        else:
            await ctx.respond("Dieser Benutzer hat keine Warnung an dieser Position.")

    # Clear Befehl
    @moderation.command(description="Löscht eine bestimmte Anzahl von Nachrichten.")
    @discord.default_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Löscht eine angegebene Anzahl von Nachrichten."""
        deleted = await ctx.channel.purge(limit=amount)

        embed = discord.Embed(
            title="🧹 Nachrichten gelöscht",
            description=f"Es wurden {len(deleted)} Nachrichten gelöscht.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

    # Mute Befehl
    @moderation.command(description="Muted einen Benutzer.")
    @discord.default_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, reason: str = "Kein Grund angegeben"):
        """Muted einen Benutzer."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        await user.edit(mute=True, reason=reason)

        embed = discord.Embed(
            title="🔇 Benutzer gemuted",
            description=f"{user.mention} wurde gemuted. Grund: {reason}",
            color=discord.Color.red()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

        try:
            dm_embed = discord.Embed(
                title="🔇 Du wurdest gemuted",
                description=f"Du wurdest von {ctx.author.mention} gemuted. Grund: {reason}",
                color=discord.Color.red()
            )
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            await ctx.respond(f"Ich kann {user.name} keine DM senden.")

    # Unmute Befehl
    @moderation.command(description="Entmuted einen Benutzer.")
    @discord.default_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        """Entmuted einen Benutzer."""
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        await user.edit(mute=False)

        embed = discord.Embed(
            title="🔊 Benutzer entmuted",
            description=f"{user.mention} wurde entmuted.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

        try:
            dm_embed = discord.Embed(
                title="🔊 Du wurdest entmuted",
                description=f"Du wurdest von {ctx.author.mention} entmuted.",
                color=discord.Color.green()
            )
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            await ctx.respond(f"Ich kann {user.name} keine DM senden.")

    # Unban Befehl
    @moderation.command(description="Entbannt einen Benutzer.")
    @discord.default_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, reason: str = "Kein Grund angegeben"):
        """Entbannt einen Benutzer."""
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        await ctx.guild.unban(user, reason=reason)

        embed = discord.Embed(
            title="🔓 Benutzer entbannt",
            description=f"{user.mention} wurde entbannt. Grund: {reason}",
            color=discord.Color.green()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

        try:
            dm_embed = discord.Embed(
                title="🔓 Du wurdest entbannt",
                description=f"Du wurdest von {ctx.author.mention} entbannt. Grund: {reason}",
                color=discord.Color.green()
            )
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            await ctx.respond(f"Ich kann {user.name} keine DM senden.")

    # Lock Befehl
    @moderation.command(description="Sperrt einen Kanal.")
    @discord.default_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel):
        """Sperrt einen Kanal."""
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        embed = discord.Embed(
            title="🔒 Kanal gesperrt",
            description=f"{channel.mention} wurde gesperrt.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

    # Unlock Befehl
    @moderation.command(description="Entsperrt einen Kanal.")
    @discord.default_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel):
        """Entsperrt einen Kanal."""
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        await channel.set_permissions(ctx.guild.default_role, send_messages=True)

        embed = discord.Embed(
            title="🔓 Kanal entsperrt",
            description=f"{channel.mention} wurde entsperrt.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

    # Lockdown Befehl
    @moderation.command(description="Sperrt alle Kanäle.")
    @discord.default_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        """Sperrt alle Kanäle."""
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        embed = discord.Embed(
            title="🔒 Lockdown",
            description="Alle Kanäle wurden gesperrt.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

    # Unlockdown Befehl
    @moderation.command(description="Entsperrt alle Kanäle.")
    @discord.default_permissions(manage_channels=True)
    async def unlockdown(self, ctx):
        """Entsperrt alle Kanäle."""
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)

        embed = discord.Embed(
            title="🔓 Unlockdown",
            description="Alle Kanäle wurden entsperrt.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

    # Slowmode
    @moderation.command(description="Setzt den Slowmode für einen Kanal.")
    @discord.default_permissions(manage_channels=True)
    async def slowmode(self, ctx, channel: discord.TextChannel, seconds: int):
        """Setzt den Slowmode für einen Kanal."""
        if not ctx.author.guild_permissions.manage_channels:
            return await ctx.respond("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

        await channel.edit(slowmode_delay=seconds)

        embed = discord.Embed(
            title="🕐 Slowmode gesetzt",
            description=f"Der Slowmode für {channel.mention} wurde auf {seconds} Sekunden gesetzt.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Projekt des OPPRO.NET Development | Admin System | Powered by Discord")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(AdminSystem(bot))
