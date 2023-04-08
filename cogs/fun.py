import datetime
import random
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.errors import *
from discord.ext.commands import *

from functions import *
from bot import *

preferences = load_json('./info/preferences.json')

class Fun(commands.Cog):
    def __init__(self, bot:PattlesBot):
        self.bot = bot
    
    @commands.Cog.listener(name='on_message')
    async def leveling(self, message):
        if message.author.bot:
            return

        if self.bot.prefix in message.content:
            return

        """Checking if a member's profile exists in the json."""
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)

        """If it doesn't, creates a fresh profile for the member."""
        if str(message.author.id) not in leveling_json[str(message.guild.id)]:
            leveling_json[str(message.guild.id)][str(message.author.id)] = {}
            leveling_json[str(message.guild.id)][str(message.author.id)]['experience'] = 0
            leveling_json[str(message.guild.id)][str(message.author.id)]['level'] = 0

            with open(LEVELING_JSON, 'w') as f:
                json.dump(leveling_json, f)
            return
    
        """If it does, then adds experience to the member's profile."""
        member_level = leveling_json[str(message.guild.id)][str(message.author.id)]['level']
        member_experience = leveling_json[str(message.guild.id)][str(message.author.id)]['experience']
                
        level_up_formula = 5 * (member_level ** 2) + (50 * member_level) + 100
        
        member_new_experience = member_experience + random.randint(2, 10)

        """If a member's experience exceeds the required experience to level up, the member's level is +1 and their experience is reset."""
        if level_up_formula - member_new_experience <= 0:
            member_new_level = leveling_json[str(message.guild.id)][str(message.author.id)]['level'] + 1

            leveling_json[str(message.guild.id)][str(message.author.id)]['experience'] = 0
            leveling_json[str(message.guild.id)][str(message.author.id)]['level'] = member_new_level

            with open(LEVELING_JSON, 'w') as f:
                json.dump(leveling_json, f)
            
            embed = discord.Embed(title=f'{self.bot.party_popper_emoji} Level up!', description=f'{message.author.mention}, you have leveled up to **level {member_new_level}**!', color=self.bot.color)
            await message.channel.send(embed=embed)
            return
        
        """If it doesn't, then the member's experience is updated."""
        leveling_json[str(message.guild.id)][str(message.author.id)]['experience'] = member_new_experience
        
        with open(LEVELING_JSON, 'w') as f:
            json.dump(leveling_json, f)

    @commands.hybrid_command(description='Displays the level of yourself or a mentioned member.', aliases=['rank'])
    async def level(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author

        if member.bot:
            embed = discord.Embed(description=f'The level of {member.mention} will remain a mystery...', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        """Checking if a member's profile exists in the json."""
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)

        """If it doesn't, sends a response embed."""
        if str(member.id) not in leveling_json[str(ctx.guild.id)]:
            embed = discord.Embed(description=f'{member.mention} has no XP. Maybe start a conversation with them?', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        """Getting some objects that are required for the profile."""
        member_level = leveling_json[str(ctx.guild.id)][str(member.id)]['level']
        member_experience = leveling_json[str(ctx.guild.id)][str(member.id)]['experience']
        level_up_formula = 5 * (member_level ** 2) + (50 * member_level) + 100

        """If it does, displays the member's profile."""
        embed = discord.Embed(title=f'{member} | Level', color=self.bot.color)
        embed.add_field(name='Level:', value=f'{member.mention} is level **{member_level}**.')
        embed.add_field(name='XP Left to Next Level:', value=
            f'`{0 if level_up_formula - member_experience <= 0 else level_up_formula - member_experience}` XP left.\n'
            f'`{member_experience}/{level_up_formula}` XP total.'
            )
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f'User ID: {member.id}')
        await msg.edit(embed=embed)

    @commands.hybrid_command(description='Set a member to a certain level.')
    @commands.has_permissions(manage_roles=True)
    async def setlevel(self, ctx, member:discord.Member, level:int):
        if member.bot:
            embed = discord.Embed(description=f'You cannot change the level of bots.', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        if level < 0:
            embed = discord.Embed(description='You cannot set a member\'s level lower than 0.', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        if level > 9999:
            embed = discord.Embed(description=f'This level is unreasonably high for any member to have, let alone {member.mention}. Maybe try a lower level next time?', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)
        
        """Checking if a member's profile exists in the json."""
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)

        """If it doesn't, creates a fresh profile for the member."""
        if str(member.id) not in leveling_json[str(ctx.guild.id)]:
            leveling_json[str(ctx.guild.id)][str(member.id)] = {}
            leveling_json[str(ctx.guild.id)][str(member.id)]['experience'] = 0
            leveling_json[str(ctx.guild.id)][str(member.id)]['level'] = level

            with open(LEVELING_JSON, 'w') as f:
                json.dump(leveling_json, f)
            
            embed = discord.Embed(description=f'Successfully set {member.mention}\'s level to level **{level}**!', color=self.bot.color)
            await msg.edit(embed=embed)
            return

        leveling_json[str(ctx.guild.id)][str(member.id)]['experience'] = 0
        leveling_json[str(ctx.guild.id)][str(member.id)]['level'] = level
        with open(LEVELING_JSON, 'w') as f:
            json.dump(leveling_json, f)
            
        embed = discord.Embed(description=f'Successfully set {member.mention}\'s level to level **{level}**!', color=self.bot.color)
        await msg.edit(embed=embed)

    @commands.hybrid_command(description='Resets the level of a member.')
    @commands.has_permissions(manage_roles=True)
    async def resetlevel(self, ctx, member:discord.Member):
        if member.bot:
            embed = discord.Embed(description=f'You cannot reset the level of bots.', color=self.bot.color)
            await ctx.send(embed=embed)
            return        

        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        """Checking if a member's profile exists in the json."""
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)

        """If it doesn't, creates a fresh profile for the member."""
        if str(member.id) not in leveling_json[str(ctx.guild.id)]:
            leveling_json[str(ctx.guild.id)][str(member.id)] = {}
            leveling_json[str(ctx.guild.id)][str(member.id)]['experience'] = 0
            leveling_json[str(ctx.guild.id)][str(member.id)]['level'] = 0

            with open(LEVELING_JSON, 'w') as f:
                json.dump(leveling_json, f)
            
            embed = discord.Embed(description=f'Successfully reset {member.mention}\'s level.', color=self.bot.color)
            await msg.edit(embed=embed)
            return
        
        leveling_json[str(ctx.guild.id)][str(member.id)]['experience'] = 0
        leveling_json[str(ctx.guild.id)][str(member.id)]['level'] = 0
        with open(LEVELING_JSON, 'w') as f:
            json.dump(leveling_json, f)

        embed = discord.Embed(description=f'Successfully reset {member.mention}\'s level.', color=self.bot.color)
        await msg.edit(embed=embed)
        
    @commands.hybrid_command(description='Displays the top 25 members with the highest level.', aliases=['levelslb', 'levellb', 'levelsleaderboard', 'levels'])
    async def levelleaderboard(self, ctx):
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        """Getting all of the members' profiles in a dict."""
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)

        all_members_list = {}
        for member_id in leveling_json[str(ctx.guild.id)]:
            all_members_list.update({member_id: leveling_json[str(ctx.guild.id)][member_id]['level']})
        
        # Starting from here, I have no idea how this works.
        top_members = {id: level for id, level in sorted(all_members_list.items(), reverse=True, key=lambda item: item[1])}

        names = ''

        for postion, user in enumerate(top_members):
            """Add 1 to postion to make the index start from 1."""
            names += f'[**{get_ordinal(postion+1)}**]: <@!{user}> - Level **{top_members[user]}**\n'
            if postion >= 25 or postion + 1 == len(top_members):
                embed = discord.Embed(title='Levels Leaderboard', description=names, color=self.bot.color)
                embed.set_footer(text=f'Levels Leaderboard as of {get_local_time(self)} UTC.')
                await msg.edit(embed=embed)
                return
    
    



            
        

        

        

        

async def setup(bot):
    await bot.add_cog(Fun(bot))