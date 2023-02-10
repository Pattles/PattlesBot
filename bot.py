import datetime
import json
import sys
import traceback
from datetime import datetime, timezone

import discord
from discord.ext import commands
from discord.ext.commands.errors import *

from functions import *

def load_token():
    with open("./info/token.json") as f:
        return json.load(f)

INITIAL_EXTENSIONS = [
    # "cogs.exampleCog", 
    'cogs.developer',
    'cogs.fun',
    'cogs.general',
    'cogs.management',
    'cogs.tags',
    'cogs.utility'
    ]

LEVELING_JSON = './info/leveling.json'
LIKES_JSON = './info/likes.json'
GM_JSON = './info/gm_counter.json'

preferences = load_json('./info/preferences.json')
  
class PattlesBot(commands.Bot):
    def __init__(self):
        super().__init__(help_command=MyHelp(command_attrs={'aliases':['h'], 'description':'Displays a list of all available commands. Text command only.'}), command_prefix=commands.when_mentioned_or(preferences['primary']['prefix']), intents=discord.Intents.all(), case_insensitive=True, activity=discord.Activity(type=discord.ActivityType.playing, name=f"mind games"))
        self.client_id = 1038161541230501959
        self.owner_id = 480126550868754465
        self.token = load_token()["token"]

        # Important information. 
        self.prefix = preferences['primary']['prefix']
        self.color = preferences['primary']['color']
        self.arrow = preferences['primary']['arrow']
        self.displayed_strftime = preferences['primary']['displayed_strftime']
        
        self.version = preferences['primary']['version']
        self.icon_url = preferences['primary']['icon_url']
        self.dev = self.get_user(self.owner_id)

        # Saved Texts, used for simplifying return messages.
        self.syntax = preferences['saved_text']['syntax']
        self.hyrtcc = preferences['saved_text']['hyrtcc']
        self.swr = preferences['saved_text']['swr']
        self.usage = preferences['saved_text']['usage']
        self.aliases = preferences['saved_text']['aliases']
        self.required = preferences['saved_text']['required']
        self.optional = preferences['saved_text']['optional']
        self.foobar = preferences['saved_text']['foobar']
        self.ratelimited = preferences['saved_text']['ratelimited']

        # Emojis
        self.redX = preferences['emojis']['redX']
        self.red_warning = preferences['emojis']['red_warning']
        self.orange_warning = preferences['emojis']['orange_warning']
        self.green_warning = preferences['emojis']['green_warning']
        self.staff_icon = preferences['emojis']['staff_icon']
        self.green_tick = preferences['emojis']['green_tick']
        self.grey_tick = preferences['emojis']['grey_tick']
        self.task_list = preferences['emojis']['task_list']
        self.twitter_logo = preferences['emojis']['twitter_logo']
        self.developer_emoji = preferences['emojis']['developer']
        self.house_1 = preferences['emojis']['house_1']
        self.plus_one = preferences['emojis']['plus_one']
        self.minus_one = preferences['emojis']['minus_one']
        self.humans_emoji = preferences['emojis']['humans']
        self.nitro_boost_emoji = preferences['emojis']['nitro_boost']
        self.robot_emoji = preferences['emojis']['robot_icon']
        self.text_channel_emoji = preferences['emojis']['text_channel']
        self.voice_channel_emoji = preferences['emojis']['voice_channel']
        self.fun_emoji = preferences['emojis']['fun_emoji']
        self.heart_emoji = preferences['emojis']['heart']
        self.heart_animated_emoji = preferences['emojis']['heart_animated']
        self.party_popper_emoji = preferences['emojis']['party_popper']


    async def setup_hook(self):
        for extension in INITIAL_EXTENSIONS:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            pass

        if isinstance(error, (MissingRequiredArgument, BadArgument)):
            embed = discord.Embed(title=self.hyrtcc, description=f'Invalid command usage. \n\nFor more information about this command, type `{self.prefix}help {ctx.command.name}`.', color=self.color)
            
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
            embed.add_field(name=self.usage, value=f'```{self.prefix if "Slash command only." not in ctx.command.description else "/"}{ctx.command} {ctx.command.signature.replace("_", " ")}```', inline=False)
            
            # Checking if the command has an alias for the embed.
            if ctx.command.aliases:
                embed.add_field(name=self.aliases, value=f'`' + '`, `'.join(ctx.command.aliases) + '`', inline=False)
            await ctx.send(embed=embed)
            
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def on_message(self, message):
        if str(self.user.mention) == message.content:
            if message.author.bot:
                return
            now = datetime.now(timezone.utc)
            local_time = now.strftime(self.displayed_strftime)

            desc = f"I'm {self.user.mention}. My current prefixes are `{self.prefix}` & `/`.\n\n" \
                + f"To view all my commands, type `{self.prefix}help`."
            embed = discord.Embed(description=desc, color=self.color)
            embed.set_footer(text=f"{self.user} • Asked by {message.author} • {local_time}", icon_url=message.author.avatar)
            await message.reply(embed=embed)

        await self.process_commands(message)

    def run(self):
        super().run(self.token, reconnect=True)

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title=f'Help | {self.context.author}', description=f'{PattlesBot.user.mention} is a powerful Discord bot which is working on becoming the best Discord bot on the market. \n\nFor custom Discord bot development, visit https://pattlesstore.com/.', color=PattlesBot.color)

        for cog, commands in mapping.items():
            if cog:
                cog_name = cog.qualified_name.replace('_', ' ')
                if True:
                    emoji = ''
                    if cog_name == 'General':
                        emoji = PattlesBot.staff_icon
                    if cog_name == 'Tags':
                        emoji = PattlesBot.task_list
                    if cog_name == 'Management':
                        emoji = PattlesBot.orange_warning
                    if cog_name == 'Utility':
                        emoji = PattlesBot.green_tick
                    if cog_name == 'Developer':
                        emoji = PattlesBot.developer_emoji
                    if cog_name == 'Fun':
                        emoji = PattlesBot.fun_emoji

                # Adding embed fields for each command category.
                # Not displaying hidden categories.
                if cog_name not in ['Developer', 'Events']:
                    command_list = []
                    for command in commands:
                        command_list.append(command.name)
                    if cog_name in ['General']:
                        command_list.append('help')
                    command_list.sort()
                    command_list = '`, `'.join(command_list)
                    embed.add_field(name=f'{emoji} {cog_name}', value=f'`{command_list}`', inline=False)

                # Displaying hidden categories is author is a developer.
                if cog_name in ['Developer'] and self.context.author.id == PattlesBot.owner_id:
                    command_list = []
                    for command in commands:
                        command_list.append(command.name)
                    command_list.sort()
                    command_list = '`, `'.join(command_list)
                    embed.add_field(name=f'{emoji} {cog_name}', value=f'`{command_list}`', inline=False)

            # Rewrite to correspond to DAWbot, not PattlesSetup.
            # Displays commands without a category in a category called 'No category'.
            """
            else:
                command_list = []
                for command in commands:
                    command_list.append(command.name)
                command_list = "`, `".join(command_list)
                if self.context.author.id in PattlesSetup.dev and PattlesSetup.display_no_category in ["True", True]:
                    embed.add_field(name="No category :)", value=f"`{command_list}`", inline=False)
            """

        embed.set_footer(text=f'Use {PattlesBot.prefix}help [command] for more info on a specific command.', icon_url=PattlesBot.icon_url)
        await self.context.reply(embed=embed)
       
   # !help <command>
    async def send_command_help(self, command):
        cog_name = command.cog_name
    
        # Cancels the command if the author is attempting to view a command from a hidden category.
        if cog_name in ['Developer', 'Events'] and self.context.author.id != PattlesBot.owner_id:
            return

        if command.cog:
            cog_name = cog_name.replace('_', ' ')
        if True:
            emoji = ''
            if cog_name == 'General' or command.name == 'help':
                emoji = PattlesBot.staff_icon
            if cog_name == 'Tags':
                emoji = PattlesBot.task_list
            if cog_name == 'Management':
                emoji = PattlesBot.orange_warning
            if cog_name == 'Utility':
                emoji = PattlesBot.green_tick
            if cog_name == 'Developer':
                emoji = PattlesBot.developer_emoji
            if cog_name == 'Fun':
                emoji = PattlesBot.fun_emoji

        # Temporary fix for 'help' not displaying under the 'General' category for '!help help'.
        if command.name in ['help'] and not command.cog:
            cog_name = 'General'

        embed = discord.Embed(title=f'{emoji} {cog_name} › {command.name}', description=command.description, color=PattlesBot.color)
        
        if True:
            required = ''
            optional = ''
            foobar = ''
            if '<' in command.signature:
                required = '`<> - required`\n'
            if '[' in command.signature:
                optional = '`[] - optional`\n'
            if '|' in command.signature:
                foobar = '`item1/item2 - choose either item1 or item2`\n'

        if required != '' or optional != '':
            embed.add_field(name='Syntax:', value=required + optional + foobar, inline=False)

        signature = command.signature.replace("=", "").replace("None", "").replace("...", "").replace("|", "/").replace('"', "").replace("_", " ")
        embed.add_field(name='Usage:', value=f"```{PattlesBot.prefix if 'Slash command only.' not in command.description else '/'}{command.name} {signature}```", inline=False)
        
        if command.aliases:
            embed.add_field(name='Aliases:', value='`' + '`, `'.join(command.aliases)+ f'`, `{command.name}`', inline=False)

        embed.set_footer(text=f'Use {PattlesBot.prefix}help [command] for more info on a specific command.', icon_url=PattlesBot.icon_url)
        await self.context.reply(embed=embed)
        
      
   # !help <group>
    async def send_group_help(self, group):
        return
        await self.context.reply("This is help group")
    
   # !help <cog>
    async def send_cog_help(self, cog):
        return
        await self.context.reply("This is help cog")

class Help(commands.Cog):
    '''
    Kukiko\'s help command!
    but worse
    '''

    def __init__(self, bot: PattlesBot) -> None:
        self.bot = bot
        self.bot._original_help_command = bot.help_command
        self.bot.help_command = MyHelp()
        # self.bot.help_command.cog = General()

    async def cog_unload(self) -> None:
        assert self.bot._original_help_command is not None
        self.bot.help_command = self.bot._original_help_command



if __name__ == '__main__':
    PattlesBot = PattlesBot()
    PattlesBot.run()
