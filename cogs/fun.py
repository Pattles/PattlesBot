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
    
    @commands.hybrid_command(description='Hopefully god accepts your prayer.')
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def pray(self, ctx):
        responses = [
            'You successfully prayed to God and are blessed with good fortune for...3 seconds.', 
            'God was on vacation when you prayed, maybe next time you\'ll catch him when he\'s home.',
            'Instead of praying to God, you accidentally prayed to Pepe. Pepe says subscribe to pewdiepie.',
            'Your prayer didn\'t make it, it got stuck in the stratosphere.',
            'Your account no longer has any funds to pray. To add balance, complete 3 good deeds.'
            ]
        embed = discord.Embed(description=random.choice(responses), color=self.bot.color)
        await ctx.send(embed=embed)

    @pray.error
    async def pray_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = round(error.retry_after, 2)

            time_remaining = f'{cooldown} seconds' if cooldown != 1 else f'{cooldown} second'

            embed = discord.Embed(description=f'{ctx.author.mention}, stop praying so much! God has other prayers to tend to, you can pray again in **{time_remaining}**.', color=self.bot.color)
            await ctx.send(embed=embed)
            return

    @commands.hybrid_command(description='A totally legitimate way to check your IQ.')
    async def iqrate(self, ctx):
        embed = discord.Embed(description=f'{ctx.author.mention}\'s IQ is `{random.randint(20, 170)}`.', color=self.bot.color)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description=f'Ask the magic eight ball a question and receive advice. {preferences["saved_text"]["slash_command_only"]}')
    async def eightball(self, ctx, question:str):
        if not ctx.interaction:
            await not_interaction_embed(self, ctx)
            return

        responses = [
            'It is certain',
            'It is decidedly so',
            'Without a doubt',
            'Yes definitely',
            'You may rely on it',
            'As I see it, yes',
            'Most likely',
            'Outlook good',
            'Yes',
            'Signs point to yes',
            'Reply hazy, try again',
            'Ask again later',
            'Better not tell you now',
            'Cannot predict now',
            'Concentrate and ask again',
            'Don’t count on it',
            'My reply is no',
            'My sources say no',
            'Outlook not so good',
            'Very doubtful',
            'Absolutely not'
        ]

        desc = question + '\n\n' \
            + '> :8ball: ' + random.choice(responses) + '.'

        embed = discord.Embed(description=desc, color=self.bot.color)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description='Play russian roulette, with your remaining stay in the server being the prize.', aliases=['rr'])
    async def russianroulette(self, ctx):
        if random.randint(1,6) == 6:
            embed = discord.Embed(title='You lost', description=f'Thanks for staying at {ctx.guild.name}! Bye bye now.', color=self.bot.color)
            await ctx.send(embed=embed)

            try:
                await ctx.author.kick(reason='They lost russian roulette.')
                embed = discord.Embed(description=f'{ctx.author.mention} has been kicked from {ctx.guild.name} for losing russian roulette.', color=self.bot.color)
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title='Hm....', description='You live to see another day, only because you cheated by being an admin.', color=self.bot.color)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='You live another day', description=f'You managed to not get kicked. Then again, you had a 1 out of 6 chance to lose.', color=self.bot.color)
            await ctx.send(embed=embed)

    @commands.hybrid_command(description='Like someone in the server and give them an ego boost.')
    @commands.cooldown(1, 43200, commands.BucketType.member)
    async def like(self, ctx, member_to_like:discord.Member):
        if member_to_like == ctx.author:
            embed = discord.Embed(description='You can\'t like yourself!', color=self.bot.color)
            await ctx.send(embed=embed)
            await ctx.command.reset_cooldown(ctx)
            return
        
        if member_to_like.bot:
            embed = discord.Embed(description='Although bots are likeable, you can\'t like them.', color=self.bot.color)
            await ctx.send(embed=embed)
            await ctx.command.reset_cooldown(ctx)
            return

        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        with open(LIKES_JSON, 'r') as infile:
            likes_json = json.load(infile)

        for member_id in likes_json[str(ctx.guild.id)]:
            if str(member_to_like.id) == member_id:
                likes_json[str(ctx.guild.id)][str(member_to_like.id)]['likes'] += 1

                with open(LIKES_JSON, 'w') as f:
                    json.dump(likes_json, f)
                
                embed = discord.Embed(description=f'You have liked {member_to_like.mention}! They now have **{likes_json[str(ctx.guild.id)][str(member_to_like.id)]["likes"]}** likes!', color=self.bot.color)
                await msg.edit(embed=embed)
                return

        likes_json[str(ctx.guild.id)][str(member_to_like.id)] = {}
        likes_json[str(ctx.guild.id)][str(member_to_like.id)]['likes'] = 1

        with open(LIKES_JSON, 'w') as f:
            json.dump(likes_json, f)

        embed = discord.Embed(description=f'Congratulations! You\'re the first person to like {member_to_like.mention}!', color=self.bot.color)
        await msg.edit(embed=embed)
        
    @like.error
    async def like_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            cooldown = int(error.retry_after)
            
            hours, remainder = divmod(cooldown, 3600)
            minutes, seconds = divmod(remainder, 60)

            if True:
                hours_response = minutes_response = 0
                seconds_response = '1 second'
                if hours != 0:
                    hours_response = f"{hours} hours, "
                if minutes != 0:
                    minutes_response = f"{minutes} minutes, "
                if seconds != 0:
                    seconds_response = f"{seconds} seconds"

            embed = discord.Embed(description=f"{ctx.author.mention}, you can only like someone once every 12 hours. Please try again in **{hours_response}{minutes_response}and {seconds_response}**.", color=self.bot.color)
            await ctx.send(embed=embed)
            return

    @commands.hybrid_command(description='View yours or a mentioned member\'s likes.')
    async def likes(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author

        if member.bot:
            embed = discord.Embed(description=f'The amount of likes {member.mention} has remains a mystery...', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        with open(LIKES_JSON, 'r') as infile:
            likes_json = json.load(infile)

        if str(member.id) not in likes_json[str(ctx.guild.id)]:
            if member == ctx.author:
                embed = discord.Embed(description='You have no likes. Maybe try being a better person?', color=self.bot.color)
            else:
                embed = discord.Embed(description=f'{member.mention} has no likes. Maybe you\'ll give them their first one?', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        for member_id in likes_json[str(ctx.guild.id)]:
            if str(member.id) == member_id:
                embed = discord.Embed(description=f'{f"{member.mention} has" if member != ctx.author else "You have"} `{likes_json[str(ctx.guild.id)][member_id]["likes"]}` {"likes" if likes_json[str(ctx.guild.id)][member_id]["likes"] != 1 else "like"}.', color=self.bot.color)
                await ctx.send(embed=embed)
                return

    @commands.hybrid_command(description='View the top 25 most liked members.', aliases=['likeslb'])
    async def likesleaderboard(self, ctx):
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        with open(LIKES_JSON, 'r') as f:
            likes_json = json.load(f)

        all_members_list = {}
        for member_id in likes_json[str(ctx.guild.id)]:
            all_members_list.update({member_id: likes_json[str(ctx.guild.id)][member_id]['likes']})
        
        # Starting from here, I have no idea how this works.
        top_members = {id: likes for id, likes in sorted(all_members_list.items(), reverse=True, key=lambda item: item[1])}

        names = ''

        for postion, user in enumerate(top_members):
            """Add 1 to postion to make the index start from 1."""
            names += f'[**{get_ordinal(postion+1)}**]: <@!{user}> - {self.bot.heart_emoji if postion >= 3 else self.bot.heart_animated_emoji}**{top_members[user]}**\n'
            if postion >= 25 or postion + 1 == len(top_members):
                embed = discord.Embed(title='Likes Leaderboard', description=names, color=self.bot.color)
                embed.set_footer(text=f'Likes Leaderboard as of {get_local_time(self)} UTC.')
                embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1068794801685790752.webp?size=80&quality=lossless')
                await msg.edit(embed=embed)
                return

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
    
    @commands.hybrid_command(description='Displays your or a mentioned member\'s profile. Fit with level and likes.')
    async def profile(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author

        if member.bot:
            embed = discord.Embed(title=f'{member} | Profile', color=self.bot.color)
            embed.add_field(name='Likes:', value=f'{self.bot.heart_emoji} ???')
            embed.add_field(name='Level:', value=f'Level **???**')
            embed.add_field(name='GMs:', value=f'**???**')
            embed.set_thumbnail(url=member.avatar)
            embed.set_footer(text=f'User ID: {member.id}')
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        """Getting the JSONs."""
        with open(LIKES_JSON, 'r') as infile:
            likes_json = json.load(infile)
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)
        with open(GM_JSON, 'r') as infile:
            gm_json = json.load(infile)

        amount_of_likes = member_level = gm_count = 0
        if str(member.id) in likes_json[str(ctx.guild.id)]:
            amount_of_likes = likes_json[str(ctx.guild.id)][str(member.id)]['likes']
        if str(member.id) in leveling_json[str(ctx.guild.id)]:
            member_level = leveling_json[str(ctx.guild.id)][str(member.id)]['level']
        if str(member.id) in gm_json[str(ctx.guild.id)]:
            gm_count = gm_json[str(ctx.guild.id)][str(member.id)]['good_mornings']

        """Sending the response embed."""
        embed = discord.Embed(title=f'{member} | Profile', color=self.bot.color)
        embed.add_field(name='Likes:', value=f'{self.bot.heart_emoji} {amount_of_likes}')
        embed.add_field(name='Level:', value=f'Level **{member_level}**')
        embed.add_field(name='GMs:', value=f'**{gm_count}**')
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f'User ID: {member.id}')
        await msg.edit(embed=embed)
        
    @commands.hybrid_command(description='Fight someone. Prize? Bragging rights.')
    async def fight(self, ctx, member:discord.Member=None):
        if not member or member == ctx.author:
            embed = discord.Embed(description='[You fought yourself](https://youtu.be/WKVxKrrbz1E?t=153) and, surprise surprise, you won.', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        if member.bot:
            embed = discord.Embed(description=f'You punched {member.mention} and because of their metal shell, you broke your hand and lost.', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        fighters = [ctx.author.mention, member.mention]

        responses = [
            f'After the 3rd round, {random.choice(fighters)} won by KO.',
            f'{random.choice(fighters)} chickened out and lost by forfeit.',
            f'{random.choice(fighters)} forgot to set their alarm for the fight and overslept.',
            f'On the 1st round, {random.choice(fighters)} fell asleep because they spent all night gaming.',
            f'{random.choice(fighters)} was jumped the night before and is now in hospital recovering. The match was moved to another day.',
            f'{random.choice(fighters)} was paid ${get_readable_number(random.randint(1, 1_000_000))} to throw the fight and subsequently lost the fight.'
        ]

        embed = discord.Embed(description=random.choice(responses), color=self.bot.color)
        await ctx.send(embed=embed)

    @commands.Cog.listener(name='on_message')
    async def gm_tracker(self, message):
        if message.author.bot:
            return

        if self.bot.prefix in message.content:
            return

        if 'gm' not in message.content.lower() and 'good morning' not in message.content.lower():
            return

        if message.guild.id != 916133196184301668:
            return

        """Getting gm_counter.json"""
        with open(GM_JSON, 'r') as infile:
            gm_json = json.load(infile)

        """If the member has 0 gms, create a new profile."""
        if str(message.author.id) not in gm_json[str(message.guild.id)]:
            gm_json[str(message.guild.id)][str(message.author.id)] = {}
            gm_json[str(message.guild.id)][str(message.author.id)]['good_mornings'] = 1

            with open(GM_JSON, 'w') as f:
                json.dump(gm_json, f)
            return
        
        """If the member has at least 1 gm, +1 to their gm count."""
        gm_json[str(message.guild.id)][str(message.author.id)]['good_mornings'] += 1

        with open(GM_JSON, 'w') as f:
            json.dump(gm_json, f)

    @commands.hybrid_command(description='Displays the amount of GMs you or a mentioned member have sent.')
    async def gms(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author

        if member.bot:
            embed = discord.Embed(description=f'The amount of gms {member.mention} has sent remains a mystery...', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        with open(GM_JSON, 'r') as infile:
            gm_json = json.load(infile)

        if str(member.id) not in gm_json[str(ctx.guild.id)]:
            if member == ctx.author:
                embed = discord.Embed(description='You have sent `gm` **0** times. Try sending `gm` now!', color=self.bot.color)
            else:
                embed = discord.Embed(description=f'{member.mention} has sent `gm` **0** times.', color=self.bot.color)
            await ctx.send(embed=embed)
            return

        for member_id in gm_json[str(ctx.guild.id)]:
            if str(member.id) == member_id:
                embed = discord.Embed(description=f'{f"{member.mention} has" if member != ctx.author else "You have"} sent `gm` **{gm_json[str(ctx.guild.id)][member_id]["good_mornings"]}** times.', color=self.bot.color)
                await ctx.send(embed=embed)
                return

    @commands.hybrid_command(description='View the top 25 members with the most GMs sent.', aliases=['gmlb', 'gmslb', 'gmsleaderboard'])
    async def gmleaderboard(self, ctx):
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        with open(GM_JSON, 'r') as f:
            gm_json = json.load(f)

        all_members_list = {}
        for member_id in gm_json[str(ctx.guild.id)]:
            all_members_list.update({member_id: gm_json[str(ctx.guild.id)][member_id]['good_mornings']})
        
        # Starting from here, I have no idea how this works.
        top_members = {id: gms for id, gms in sorted(all_members_list.items(), reverse=True, key=lambda item: item[1])}

        names = ''

        for postion, user in enumerate(top_members):
            """Add 1 to postion to make the index start from 1."""
            names += f'[**{get_ordinal(postion+1)}**]: <@!{user}> - **{top_members[user]}** GMs\n'
            if postion >= 25 or postion + 1 == len(top_members):
                embed = discord.Embed(title='GMs Leaderboard', description=names, color=self.bot.color)
                embed.set_footer(text=f'GMs Leaderboard as of {get_local_time(self)} UTC.')
                embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1045357247544447037.webp?size=240&quality=lossless')
                await msg.edit(embed=embed)
                return
 



            
        

        

        

        

async def setup(bot):
    await bot.add_cog(Fun(bot))