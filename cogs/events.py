import datetime
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from functions import *
from bot import *

preferences = load_json('./info/preferences.json')

GUILD_DATA_JSON = './info/guild_data.json'

class Events(commands.Cog):
    def __init__(self, bot:PattlesBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open(LEVELING_JSON, 'r') as infile:
            leveling_json = json.load(infile)
        
        """Checking if the bot already has the guild's data."""
        if str(guild.id) in leveling_json:
            return
        
        """If not, moves on to the rest of the command."""

        """Settings up the 'leveling' module."""
        if str(guild.id) not in leveling_json:
            leveling_json[str(guild.id)] = {}
            leveling_json[str(guild.id)][str(guild.owner.id)] = {}
            leveling_json[str(guild.id)][str(guild.owner.id)]['experience'] = 0
            leveling_json[str(guild.id)][str(guild.owner.id)]['level'] = 0

            with open(LEVELING_JSON, 'w') as f:
                json.dump(leveling_json, f)


async def setup(bot):
    await bot.add_cog(Events(bot))