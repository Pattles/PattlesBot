import asyncio
import json
import traceback
import random
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context, Greedy

from functions import *
from bot import *

preferences = load_json('./info/preferences.json')

class Developer(commands.Cog):
    def __init__(self, bot:PattlesBot):
        self.bot = bot

    @commands.command(description='Syncs all commands globally. Only accessible to developers.')
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if ctx.author.id != self.bot.owner_id:
            return

        embed = discord.Embed(description="Syncing...", color=self.bot.color)
        await ctx.send(embed=embed)
        print("Syncing...")
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(embed=discord.Embed(description=f"Synced `{len(synced)}` commands {'globally' if spec is None else 'to the current guild.'}.", color=self.bot.color))
            print("Synced.")
            return
        
        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(embed=discord.Embed(description=f"Synced the tree to {ret}/{len(guilds)}.", color=self.bot.color))
        print("Synced.")

    @commands.command(description='Terminates the bot.')
    async def terminate(self, ctx):
        if ctx.author.id != self.bot.owner_id:
            return
            # responses = [
                # f'Oompa loompa doopity doo, {ctx.author.mention} no bot killing for you.',
                # f'Oompa loompa doopity dee, {ctx.author.mention} you cannot put a stop to me.',
                # f'Oompa loompa doopity dug, {ctx.author.mention} don\'t you dare pull the plug.',
                # f'Oompa loompa doopity dort, {ctx.author.mention} I won\'t abort.',
                # f'Oompa loompa doopity dop, {ctx.author.mention} **STOP!!**',
                # f'Oompa loompa doopity two, {ctx.author.mention} soon, {self.bot.user.mention} electric boogaloo.',
                # f'Oompa loompa doopity dood, {ctx.author.mention} you will not conclude\n\n*my existence*.',
                # f'Oompa loompa doopity doo, {ctx.author.mention} do you really want me to discontinue?'
            # ]

            # embed = discord.Embed(description=random.choice(responses), color=self.bot.color)
            # await ctx.send(embed=embed)
            # return
        
        embed = discord.Embed(description=f'Terminating {self.bot.user.mention}.', color=self.bot.color)
        await ctx.send(embed=embed)

        await self.bot.close()
    

async def setup(bot):
    await bot.add_cog(Developer(bot))
