import discord
import json
import datetime
import time
from datetime import datetime


def load_json(filename):
    with open(filename, encoding="utf-8") as infile:
        return json.load(infile)

def write_json(filename, contents):
    with open(filename, 'w') as outfile:
        json.dump(contents, outfile, ensure_ascii=True, indent=4)

def get_local_time(self):
    now = datetime.utcnow()
    local_time = now.strftime(self.bot.displayed_strftime)
    return local_time

def get_relative_time(self):
    relative_time = f"<t:{int(time.time())}:f>"
    return relative_time

def get_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        get_ordinal(0)   => '0th'
        get_ordinal(3)   => '3rd'
        get_ordinal(122) => '122nd'
        get_ordinal(213) => '213th'
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

async def not_interaction_embed(self, ctx):
    embed = discord.Embed(description="Please use this command as a slash command.", color=self.bot.color)
    await ctx.send(embed=embed)

def get_readable_number(number):
    number_with_commas = f'{number:,}'
    return number_with_commas

def invalid_cmd_usage_embed(self, ctx):
    embed = discord.Embed(title=self.bot.hyrtcc, description=f'Invalid command usage. \n\nFor more information about this command, type `{self.bot.prefix}help {ctx.command.name}`.', color=self.bot.color)
            
    # Checking if the command has arguments, and therefore required syntax for the embed.
    required = ''
    optional = ''
    foobar = ''
    if '<' in ctx.command.signature:
        required = '`<> - required`\n'
    if '[' in ctx.command.signature:
        optional = '`[] - optional`\n'
    if '|' in ctx.command.signature:
        foobar = '`item1/item2 - choose either item1 or item2`\n'

    if required != '' or optional != '':
        embed.add_field(name="Syntax:", value=required + optional + foobar, inline=False)
    
    # Adding command usage for the embed.
    embed.add_field(name=self.bot.usage, value=f'```{self.bot.prefix if "Slash command only." not in ctx.command.description else "/"}{ctx.command} {ctx.command.signature.replace("_", " ")}```', inline=False)
    
    # Checking if the command has an alias for the embed.
    if ctx.command.aliases:
        embed.add_field(name=self.bot.aliases, value=f'`' + '`, `'.join(ctx.command.aliases) + '`', inline=False)

    return embed