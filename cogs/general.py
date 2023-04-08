import datetime
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from functions import *
from bot import *

LIKES_JSON = './info/likes.json'
LEVELING_JSON = './info/leveling.json'

preferences = load_json('./info/preferences.json')

class General(commands.Cog):
    def __init__(self, bot:PattlesBot):
        self.bot = bot


    @commands.hybrid_command(description='Displays some information about the server.')
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=ctx.guild.name, description=f'[Download Server Icon]({ctx.guild.icon})', color=self.bot.color)

        """Getting information about the server owner."""
        desc = f'{ctx.guild.owner.mention} \n' \
            + f'{ctx.guild.owner} \n' \
            + f'{ctx.guild.owner_id}'
        embed.add_field(name='Owner:', value=desc)

        """Getting informtion about the server's creation date."""
        duration = discord.utils.utcnow() - ctx.guild.created_at
        days, remainder = divmod(int(duration.total_seconds()), 86400)
        hours, minutes = divmod(remainder, 3600)
        minutes, seconds = divmod(minutes, 60)
        months, days = divmod(days, 30.416666666666667)
        years, months = divmod(months, 12)     

        years, months, days, hours, minutes, seconds = int(years), int(months), int(days), hours, minutes, seconds

        if True:
            years_str = months_str = days_str = hours_str = minutes_str = seconds_str = ''

            if years != 0:
                years_str = f'{years} years, ' if years != 1 else f'{years} year, '
            if months != 0:
                months_str = f'{months} months, ' if months != 1 else f'{months} month, '
            if days != 0:
                days_str = f'{days} days, ' if days != 1 else f'{days} day, '
            if hours != 0:
                hours_str = f'{hours} hours, ' if hours != 1 else f'{hours} hour, '
            if minutes != 0:
                minutes_str = f'{minutes} minutes, ' if minutes != 1 else f'{minutes} minute, '
            if seconds != 0:
                seconds_str = f'{seconds} seconds' if seconds != 1 else f'{seconds} second, '

        created_at_pretty = f'{years_str}{months_str}{days_str}{hours_str}{minutes_str}{seconds_str} ago'

        embed.add_field(name='Server Creation Date:', value=created_at_pretty + '\n' + str(ctx.guild.created_at)[:16] + ' UTC.\n' + discord.utils.format_dt(ctx.guild.created_at, 'f'))

        """Less difficult-to-code in information (role count, member count, etc.)"""
        embed.add_field(name='Role Count:', value=len(ctx.guild.roles) - 1)

        bot_count = 0
        for member in ctx.guild.members:
            if member.bot:
                bot_count += 1
        embed.add_field(name='Member Count:', value=f'{self.bot.humans_emoji} {ctx.guild.member_count} Members\n' + f'{self.bot.nitro_boost_emoji} {len(ctx.guild.premium_subscribers)} Boosters\n' + f'{self.bot.robot_emoji} {bot_count} Bots')

        text_channel_count = voice_channel_count = 0
        for channel in ctx.guild.channels:
            if type(channel) in [discord.TextChannel, discord.CategoryChannel, discord.ForumChannel]:
                text_channel_count += 1
            if type(channel) in [discord.VoiceChannel, discord.StageChannel]:
                voice_channel_count += 1

        embed.add_field(name='Channel Count:', value=f'{len(ctx.guild.channels)} Total Channels\n' + f'{self.bot.text_channel_emoji} {text_channel_count} Text Channels\n' + f'{self.bot.voice_channel_emoji} {voice_channel_count} Voice Channels')
        embed.add_field(name='Boost Level:', value=f'Boost Level {ctx.guild.premium_tier}\n' + f'{ctx.guild.premium_subscription_count} Boosts\n' + f'{len(ctx.guild.premium_subscribers)} Boosters')

        """Other information about the server (icon, ID, etc.)"""
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text=f'Guild ID: {ctx.guild.id}')

        await ctx.send(embed=embed)
    
    @commands.hybrid_command(description='Displays the amount of messages you or a mentioned member have sent.')
    async def messages(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author

        embed = discord.Embed(title='Working...', description='I\'ll let you know when I\'m done.', color=self.bot.color)
        await ctx.send(embed=embed)

        """Getting the amount of messages sent in all channels."""
        message_count = 0
        for channel in ctx.guild.text_channels:
            async for message in channel.history(limit=None):
                if message.author == member:
                    message_count += 1

        embed = discord.Embed(title=member, description=f'{"You have" if member == ctx.author else f"{member.mention} has"} sent **{message_count}** messages in this server.', color=self.bot.color)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(description='Displays the bot\'s latency.')
    async def ping(self, ctx):
        embed = discord.Embed(title=':ping_pong: Pong!', description=f'{self.bot.user.mention}\'s ping is `{round(self.bot.latency * 1000)}ms.`', color=self.bot.color)
        embed.set_footer(text=f'{self.bot.user.name} • Asked by {ctx.author} • {get_local_time(self)}', icon_url=self.bot.icon_url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description='Displays some information about the bot.')
    async def about(self, ctx):
        desc = 'PattlesBot is a multi-purpose bot aimed at providing utility, moderation, logging, games, and more to communities. \n\nFor custom Discord bot development, visit https://pattlesstore.com/.'
        information = f'{self.bot.arrow} **Python:** 3.9.7\n' \
            + f'{self.bot.arrow} **Library:** [discord.py {discord.__version__}](https://github.com/Rapptz/discord.py)\n' \
            + f'{self.bot.arrow} **Latency:** {round(self.bot.latency * 1000)} ms\n' \
            + f'{self.bot.arrow} **Servers:** {get_readable_number(len(self.bot.guilds))}'
        links = f'{self.bot.arrow} **Discord:** [Click me](https://discord.gg/pattlesstore)\n' \
            + f'{self.bot.arrow} **Website:** [Click me](https://pattlesstore.com/)\n'
        embed = discord.Embed(title=self.bot.user.name + ' | ' + ctx.command.name, description=desc, color=self.bot.color)
        embed.add_field(name='Information', value=information, inline=False)
        embed.add_field(name='Links', value=links, inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text='cool beans', icon_url=self.bot.user.avatar)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description='Get an invite link to invite the bot to a server.')
    async def invite(self, ctx):
        embed = discord.Embed(description='Click [here](https://discord.com/api/oauth2/authorize?client_id=1038161541230501959&permissions=2416274434&scope=applications.commands%20bot) to invite the bot.', color=self.bot.color)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description='Forces the bot to leave the server.')
    @commands.has_permissions(kick_members=True)
    async def leave(self, ctx):
        """Opening up all jsons."""
        with open(LIKES_JSON, 'r') as infile:
            likes_json = json.load(infile)
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)
        # with open(GM_JSON, 'r') as infile:
            # gm_json = json.load(infile)

        # """Checking if the bot has likes data. If so, clears all likes data from json."""
        # if str(ctx.guild.id) in likes_json:
            # del likes_json[str(ctx.guild.id)]

            # with open(LIKES_JSON, 'w') as f:
                # json.dump(likes_json, f)
        
        """Checking if the bot has leveling data. If so, clears all leveling data from json."""
        if str(ctx.guild.id) in leveling_json:
            del leveling_json[str(ctx.guild.id)]

            with open(LEVELING_JSON, 'w') as f:
                json.dump(leveling_json, f)

        # """Checking if the bot has good_monrning_tracker data. If so, clears all good_monrning_tracker data from json."""
        # if str(ctx.guild.id) in gm_json:
            # del gm_json[str(ctx.guild.id)]

            # with open(GM_JSON, 'w') as f:
                # json.dump(gm_json, f)


        embed = discord.Embed(description=f'Leaving **{ctx.guild.name}**. If you wish to re-invite the bot, click [here](https://discord.com/api/oauth2/authorize?client_id=1038161541230501959&permissions=2416274434&scope=applications.commands%20bot).', color=self.bot.color)
        await ctx.send(embed=embed)

        await ctx.guild.leave()


async def setup(bot):
    await bot.add_cog(General(bot))