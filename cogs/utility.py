import re
import datetime
import urllib
import math
from ast import literal_eval
from datetime import datetime, timezone

import discord
from bot import *
from discord import app_commands
from discord.ext import commands
from etherscan import Etherscan
from functions import *

preferences = load_json('./info/preferences.json')

def load_etherscan_api_key():
    with open("./info/etherscan_api_key.json") as f:
        return json.load(f)

class Utility(commands.Cog):
    def __init__(self, bot:PattlesBot):
        self.bot = bot

    @commands.hybrid_command(description='Converts a specified amount of ETH into USD.')
    async def tousd(self, ctx, eth_to_convert:float):
        """Getting the objects, I have no clue how most of this works."""
        x = urllib.request.urlopen('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
        bytes_object = x.read()
        eth_dict = literal_eval(bytes_object.decode('utf-8'))
        eth_price_in_usd = eth_dict['USD']

        """Converting ETH to USD with current ETH price."""
        result = eth_to_convert * eth_price_in_usd

        """Sending response embed."""
        embed = discord.Embed(title='ETH › USD', description=f'The exchange rate of ETH to USD is `${eth_price_in_usd}`', color=self.bot.color)
        embed.add_field(name='ETH', value=get_readable_number(round(eth_to_convert, 4)))
        embed.add_field(name='USD', value=f'${get_readable_number(round(result, 2))}')
        embed.set_footer(text=f'Exchange rate as of {get_local_time(self)}')
        await ctx.send(embed=embed)

    @commands.hybrid_command(description='Converts a specified amount of USD into ETH.')
    async def toeth(self, ctx, usd_to_convert:float):
        """Getting the objects, I have no clue how most of this works."""
        x = urllib.request.urlopen('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
        bytes_object = x.read()
        eth_dict = literal_eval(bytes_object.decode('utf-8'))
        eth_price_in_usd = eth_dict['USD']

        """Converting ETH to USD with current ETH price."""
        result = usd_to_convert / eth_price_in_usd

        """Sending response embed."""
        embed = discord.Embed(title='USD › ETH', description=f'The exchange rate of ETH to USD is `${eth_price_in_usd}`', color=self.bot.color)
        embed.add_field(name='ETH', value=get_readable_number(round(result, 4)))
        embed.add_field(name='USD', value=f'${get_readable_number(round(usd_to_convert) if usd_to_convert % 10 == 0 else usd_to_convert)}')
        embed.set_footer(text=f'Exchange rate as of {get_local_time(self)}')
        await ctx.send(embed=embed)

    @commands.hybrid_command(description='Displays the balance of an ETH address.')
    async def ethbal(self, ctx, eth_address):        
        eth = Etherscan(load_etherscan_api_key()['api_key'])
        try:
            eth_balance = float(eth.get_eth_balance(eth_address))/1_000_000_000_000_000_000
        except AssertionError:
            await ctx.send(embed=invalid_cmd_usage_embed(self, ctx))
            return

        hidden_eth_address = f'{eth_address[:5]}...{eth_address[38:]}'

        embed = discord.Embed(color=self.bot.color)
        embed.add_field(name='ETH Address:', value=hidden_eth_address)
        embed.add_field(name='ETH Balance:', value=f'{get_readable_number(round(eth_balance, 4))} ETH')
        embed.set_footer(text=f'ETH Address: {eth_address}')
        await ctx.send(embed=embed)

        # /^0x[a-fA-F0-9]{40}$/gm - Regex for an ETH address

    @commands.hybrid_command(description='Displays the current ETH to USD exchange rate.')
    async def ethprice(self, ctx):
        """Getting the objects, I have no clue how most of this works."""
        x = urllib.request.urlopen('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
        bytes_object = x.read()
        eth_dict = literal_eval(bytes_object.decode('utf-8'))
        eth_price_in_usd = eth_dict['USD']

        embed = discord.Embed(title='ETH to USD Exchange Rate', description=f'As of {get_local_time(self)} UTC, ETH is `{eth_price_in_usd}` USD.', color=self.bot.color)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description=f'Sends an idea into the ideas channel. {preferences["saved_text"]["slash_command_only"]}')
    async def idea(self, ctx, explanation:str):
        if not ctx.interaction:
            await not_interaction_embed(self, ctx)
            return

        ideas_channel = self.bot.get_channel(1068628218334150686)

        embed = discord.Embed(title=f'New Idea by {ctx.author}', description=explanation, color=self.bot.color)
        msg = await ideas_channel.send(embed=embed)

        embed = discord.Embed(description=f'Successfully sent your idea into the {ideas_channel.mention} channel. [Jump to idea.]({msg.jump_url})', color=self.bot.color)
        await ctx.send(embed=embed)


   


        
        

    

async def setup(bot):
    await bot.add_cog(Utility(bot))
