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


async def setup(bot):
    await bot.add_cog(Events(bot))