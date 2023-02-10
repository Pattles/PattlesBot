import datetime
from datetime import datetime, timezone

import discord
import asyncio
from discord import app_commands
from discord.ext import commands

from functions import *
from bot import *

preferences = load_json('./info/preferences.json')

class Management(commands.Cog):
    def __init__(self, bot:PattlesBot):
        self.bot = bot
    
    @commands.hybrid_command(description='Adds a role to a member.')
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, role:discord.Role, member:discord.Member):
        await member.add_roles(role)
        
        embed = discord.Embed(title='Successfully added role to member.', description=f'Added {role.mention} to {member.mention}.', color=self.bot.color)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description='Deletes a specified amount of messages in the channel.', aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:int):
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)
        await msg.delete()

        embed = discord.Embed(description=f"Successfully deleted `{amount}` messages.", color=self.bot.color)

        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        await msg.delete()

    @commands.hybrid_command(description='Run this command to setup the bot. If you don\'t, the bot will not function properly.')
    async def setup(self, ctx):
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        # Opening up all jsons.
        with open(LIKES_JSON, 'r') as infile:
            likes_json = json.load(infile)
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)
        with open(GM_JSON, 'r') as infile:
            gm_json = json.load(infile)

        # Checking if the bot already has the guild's data.
        if str(ctx.guild.id) in likes_json and str(ctx.guild.id) in leveling_json and str(ctx.guild.id) in gm_json:
            embed = discord.Embed(description=f'It looks like the bot has already been setup by someone in **{ctx.guild.name}**.', color=self.bot.color)
            await msg.edit(embed=embed)
            return
        
        # If not, moves on to the rest of the command.

        # Setting up the 'likes' module.        
        if str(ctx.guild.id) not in likes_json:
            likes_json[str(ctx.guild.id)] = {}
            likes_json[str(ctx.guild.id)][str(ctx.author.id)] = {}
            likes_json[str(ctx.guild.id)][str(ctx.author.id)]['likes'] = 0

            with open(LIKES_JSON, 'w') as f:
                json.dump(likes_json, f)

        # Settings up the 'leveling' module.
        if str(ctx.guild.id) not in leveling_json:
            leveling_json[str(ctx.guild.id)] = {}
            leveling_json[str(ctx.guild.id)][str(ctx.author.id)] = {}
            leveling_json[str(ctx.guild.id)][str(ctx.author.id)]['experience'] = 0
            leveling_json[str(ctx.guild.id)][str(ctx.author.id)]['level'] = 0

            with open(LEVELING_JSON, 'w') as f:
                json.dump(leveling_json, f)

        # Setting up the 'gm_tracker' module.        
        if str(ctx.guild.id) not in gm_json:
            gm_json[str(ctx.guild.id)] = {}
            gm_json[str(ctx.guild.id)][str(ctx.author.id)] = {}
            gm_json[str(ctx.guild.id)][str(ctx.author.id)]['good_mornings'] = 0

            with open(GM_JSON, 'w') as f:
                json.dump(gm_json, f)

        embed = discord.Embed(description=f'Successfully setup the bot for **{ctx.guild.name}**. Have fun!', color=self.bot.color)
        await msg.edit(embed=embed)


        
        """
        if str(ctx.guild.id) not in guild_data_dict:
            guild_data_dict[str(ctx.guild.id)] = {}
            
            # Setting up for the 'likes' module
            guild_data_dict[str(ctx.guild.id)]['member_likes'] = {}
            guild_data_dict[str(ctx.guild.id)]['member_likes'][str(self.bot.user.id)] = {}
            guild_data_dict[str(ctx.guild.id)]['member_likes'][str(self.bot.user.id)]['likes'] = 0

            # Setting up for the 'leveling' module
            guild_data_dict[str(ctx.guild.id)]['leveling'] = {}

            # Setting up for the 'tags' module
            guild_data_dict[str(ctx.guild.id)]['tags'] = {}

            with open(GUILD_DATA_JSON, 'w') as f:
                json.dump(guild_data_dict, f)
            
            embed = discord.Embed(description=f'Successfully setup the bot for **{ctx.guild.name}**. Have fun!', color=self.bot.color)
            await msg.edit(embed=embed)
            return
        """
        





async def setup(bot):
    await bot.add_cog(Management(bot))