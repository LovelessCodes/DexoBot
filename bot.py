import discord
import os
import json
from colorama import Fore, Style
from discord.ext import commands
    
intents = discord.Intents.default()
intents.members = True
config = json.load(open('config.json','r+'))
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"[{Fore.LIGHTGREEN_EX}+{Style.RESET_ALL}] Bot is ready as {bot.user.name}#{bot.user.discriminator}")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"[{Fore.LIGHTGREEN_EX}+{Style.RESET_ALL}] {filename[:-3].title()} Commands have been loaded")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(colour=0xFF0000, title=":warning: Permission Error", description=f"{error}")
        embed.set_image(url="https://i.imgur.com/EtdtB66.gif")
        await ctx.send(embed=embed, delete_after=15)
        return
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=0xFF0000, title=":warning: Bad Argument Error", description=f"{error}")
        embed.add_field(name="Usage:", value=f"`{bot.command_prefix}{ctx.command} {ctx.command.usage}`")
        embed.set_image(url="https://i.imgur.com/RYdftFp.gif")
        await ctx.send(embed=embed, delete_after=15)
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=0xFF0000, title=":warning: Required Argument Error", description=f"{error}")
        embed.add_field(name="Usage:", value=f"`{bot.command_prefix}{ctx.command} {ctx.command.usage}`")
        await ctx.send(embed=embed, delete_after=15)
        return
    raise error

@bot.command(pass_context=True, name="help", description="Shows this message")
async def help(ctx):
    embed = discord.Embed(colour=0x00FF00, title=':wrench: Dexo :robot: Help')
    cc = {}
    for command in bot.commands:
        if command.cog:
            cmod = command.cog.qualified_name
        else:
            cmod = ":speech_balloon: Misc"
        if cmod not in cc:
            cc[cmod] = []
        ins = f"> `{bot.command_prefix}{command}"
        if command.usage:
            ins += f" {command.usage}"
        ins += "`"
        if command.aliases:
            aliases = [f'`{al}`' for al in command.aliases]
            ins += f"\n> **Aliases**: {', '.join(aliases)}"
        if command.description:
            ins += f"\n> {command.description}\n"
        cc[cmod].append(ins)
    for cog in sorted(cc):
        embed.add_field(name=f"{cog}", value="\n".join(cc[cog]), inline=False)
    embed.set_footer(text='[] - Required, () - Optional')
    await ctx.send(embed=embed)
    return

os.system('cls')
bot.run(config['token'])