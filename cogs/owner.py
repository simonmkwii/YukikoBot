import discord
from discord.ext import commands
from yuki import color as ykColor

import sys
from io import StringIO
import traceback
import platform

import logging
import asyncio

import lupa
from lupa import LuaRuntime

import time

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True, aliases = ["python", u"\U0001f40d"])
    async def py(self, ctx, *, code: str = "print(\"Hello, World!\")"):
        """Executes Python 3 code."""

        allowedUsers = (
            self.bot.owner_id,
            357641367507435531, # Slick9000#7159
            314885561552994305  # SimonMKWii#1234
        )
        if ctx.author.id not in allowedUsers:
            await ctx.send("You don't have access to this command.")
        else:
            async with ctx.typing():
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = redir_stdout = StringIO()
                sys.stderr = redir_stderr = StringIO()

                try:
                    exec("".join(code))

                    # If the code was successful, it would set exc to "".
                    # If not, it would do except anyway.
                    exc = ""
                except:
                    exc = traceback.format_exc()

                out = redir_stdout.getvalue()
                err = redir_stderr.getvalue()

                out = f"```{out}```" if out != "" else "No standard output."
                err = f"```{err}```" if err != "" else "No error output."
                exc = f"```{exc}```" if exc != "" else "No exception."

                embed = discord.Embed(title = "", color = ykColor)
                embed.set_author(name = "Python " + platform.python_version(), icon_url = "https://cdn.discordapp.com/emojis/447523942949715969.png?v=1")
                embed.add_field(name = "Executed", value = "```py\n" + code + "```", inline = False)
                embed.add_field(name = "Standard Output", value = out, inline = False)
                embed.add_field(name = "Error Output", value = err, inline = False)
                embed.add_field(name = "Exception", value = exc, inline = False)
                embed.set_thumbnail(url = "https://cdn.discordapp.com/emojis/447523942949715969.png?v=1")
                # embed.set_footer(text = "Python " + platform.python_version(), icon_url = "https://cdn.discordapp.com/emojis/447523942949715969.png?v=1")

                sys.stdout = old_stdout
                sys.stderr = old_stderr

                await ctx.send(embed = embed)

    @commands.command(hidden = True)
    @commands.is_owner()
    async def lua(self, ctx, *, code: str = "print(\"Hello, World!\")"):
        """Executes Lua code."""

        async with ctx.typing():
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = redir_stdout = StringIO()
            sys.stderr = redir_stderr = StringIO()

            lua = LuaRuntime(unpack_returned_tuples = True)
            try:
                lua.execute("".join(code))

                # If the code was successful, it would set exc to "".
                # If not, it would do except anyway.
                exc = ""
            except:
                exc = traceback.format_exc()

            out = redir_stdout.getvalue()
            err = redir_stderr.getvalue()

            out = f"```{out}```" if out != "" else "No standard output."
            err = f"```{err}```" if err != "" else "No error output."
            exc = f"```{exc}```" if exc != "" else "No exception."

            luaLogo = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Lua-logo-nolabel.svg/480px-Lua-logo-nolabel.svg.png"

            embed = discord.Embed(title = "", color = 0x000080)
            embed.set_author(name = lua.eval("_VERSION"), icon_url = luaLogo)
            embed.add_field(name = "Executed", value="```lua\n" + code + "```", inline = False)
            embed.add_field(name = "Standard Output", value = out, inline = False)
            embed.add_field(name = "Error Output", value = err, inline = False)
            embed.add_field(name = "Exception", value = exc, inline = False)
            embed.set_thumbnail(url = luaLogo)

            sys.stdout = old_stdout
            sys.stderr = old_stderr

            await ctx.send(embed = embed)

    @commands.command(name = "load", hidden = True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
                Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            # await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.message.add_reaction(self.bot.get_emoji(465215264439664650))
            logging.error(f'Load Cog Error: {type(e).__name__} - {e}')
        else:
            # await ctx.send('**`SUCCESS`**')
            await ctx.message.add_reaction(u"\u2705")

    @commands.command(name = "unload", hidden = True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            # await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.message.add_reaction(self.bot.get_emoji(465215264439664650))
            logging.error(f'Unload Cog Error: {type(e).__name__} - {e}')
        else:
            # await ctx.send('**`SUCCESS`**')
            await ctx.message.add_reaction(u"\u2705")

    @commands.command(name = "reload", hidden = True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            # await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.message.add_reaction(self.bot.get_emoji(465215264439664650))
            logging.error(f'Reload Cog Error: {type(e).__name__} - {e}')
        else:
            # await ctx.send('**`SUCCESS`**')
            await ctx.message.add_reaction(u"\u2705")

    @commands.command(hidden = True)
    @commands.is_owner()
    async def test(self, ctx):
        """<:drip:477596602899496970> __**Test**__ *command*."""

        # await ctx.send("<a:loading:462365810891948043>")
        """if ctx.me.permissions_in(ctx.channel).embed_links:
            await ctx.send("You have EMBED_LINKS enabled.")
        else:
            await ctx.send("You have EMBED_LINKS disabled.")"""

        """embed = discord.Embed(description = u"\U000026a0 **Minecraft user doesn't exist!**", color = ykColor)
        await ctx.send(embed = embed)"""

        """await ctx.author.send_friend_request()"""

        """rules = (
            "Hate speech, Harassment of a user is not allowed.",
            "Respect everyone. No matter what gender, age, religion, status. We are trying to make a positive community where people feel welcome.",
            "You may promote yourself in <#447502809634701312>.",
            "Don't express your opinion as a fact. Everyone thinks differently!",
            "Keep discussion on point in certain chats.",
            "Please, no spamming the chats except <#447502305751859211>.",
            "Comply with [the Discord TOS](https://discordapp.com/terms)."
        )
        
        gld = ctx.guild

        embed = discord.Embed(title = "Rules", color = ykColor)
        embed.set_author(name = gld.name, icon_url = gld.icon_url)
        for i, rule in zip(range(7), rules):
            embed.add_field(name = f"Rule {i + 1}", value = rule, inline = False)
        embed.set_thumbnail(url = gld.icon_url)
        embed.set_footer(text = "Have fun!")

        await ctx.send(embed = embed)"""

        # await ctx.send("<a:succ_nsfw:480755220926693376> :relaxed:")

        """pins = await ctx.channel.pins()
        await ctx.send("\\" + pins[0].author.mention)"""

        pass

def setup(bot):
    bot.add_cog(Owner(bot))