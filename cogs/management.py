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

    @commands.hybrid_command(description='Bans every member in the server with a keyword in their username. Case sensitive!')
    @commands.has_permissions(administrator=True)
    async def keywordban(self, ctx, keyword:str):
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)
        
        banned_users, not_banned_users = [], []
        
        for member in ctx.guild.members:
            if keyword in member.name:
                try:
                    await ctx.guild.ban(member)
                    banned_users.append(member)
                except:
                    not_banned_users.append(member)

        embed = discord.Embed(title=f'Banned {len(banned_users)} {"members" if len(banned_users) != 1 else "member"}.', color=self.bot.color)
        
        if not_banned_users != []:
            embed.add_field(name=f'{len(not_banned_users)} {"members" if len(not_banned_users) != 1 else "member"} fit the paramenters but could not be banned', value=' '.join(member.mention for member in not_banned_users[0:30]))

        try:
            await msg.edit(embed=embed)
        except:
            await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Management(bot))