import datetime
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from functions import *
from bot import *

TAGS_LIST_JSON = './info/tags_list.json'

preferences = load_json('./info/preferences.json')

class Tags(commands.Cog):
    def __init__(self, bot:PattlesBot):
        self.bot = bot

    @commands.hybrid_command(description=f'Allows you to tag text for later retrieval. Use "name" for tags with more than 1 word.')
    async def tag(self, ctx, name):
        with open(TAGS_LIST_JSON, 'r') as infile:
            tags_dict = json.load(infile)

        if name not in tags_dict:
            embed = discord.Embed(description='Tag not found.', color=self.bot.color)
            await ctx.reply(embed=embed)
            return

        for tag_name in tags_dict:
            if name.lower() == tag_name.lower():
                await ctx.send(tags_dict[name]['description'])

                tags_dict[str(name)]['uses'] += 1

                with open(TAGS_LIST_JSON, 'w') as f:
                    json.dump(tags_dict, f)
                return

    @commands.hybrid_command(description=f'Creates a new tag. {preferences["saved_text"]["slash_command_only"]}', aliases=["createtag"])
    async def tagcreate(self, ctx, name, description:str):
        """
        Tries to find tag name in tags_list.json.
            If finds it, return.
        Creates a new tag with:
            description
            owner_id
            name
            aliases = []
            tag_creation_date
        """
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        with open(TAGS_LIST_JSON, 'r') as infile:
            tags_dict = json.load(infile)
        
        for tag_name in tags_dict:
            if name.lower() == tag_name.lower():
                embed = discord.Embed(description='This tag already exists.', color=self.bot.color)
                await msg.edit(embed=embed)
                return

        tags_dict[name] = {}
        tags_dict[name]['name'] = name
        tags_dict[name]['description'] = description
        tags_dict[name]['owner_id'] = ctx.author.id
        tags_dict[name]['uses'] = 0
        tags_dict[name]['tag_creation_date'] = str(datetime.utcnow())

        with open(TAGS_LIST_JSON, 'w') as f:
            json.dump(tags_dict, f)

        embed = discord.Embed(description='Successfully created tag!', color=self.bot.color)
        await msg.edit(embed=embed)

    @commands.hybrid_command(description='Displays some information about a tag.')
    async def taginfo(self, ctx, name:str):
        """
        Tries to find tag name in tags_list.json.
            if doesn't find it, return
        Retrieves and creates an embed with:
            description
            owner_id
            name
            aliases
            tag_creation_date
        """
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)
        
        with open(TAGS_LIST_JSON, 'r') as infile:
            tags_dict = json.load(infile)

        if name not in tags_dict:
            embed = discord.Embed(description='Tag not found.', color=self.bot.color)
            await msg.edit(embed=embed)
            return

        for tag_name in tags_dict:
            if name.lower() == tag_name.lower():
                found_tag = tags_dict[tag_name]

                author = self.bot.get_user(found_tag['owner_id'])
                embed = discord.Embed(title=tag_name, color=self.bot.color)
                embed.set_author(name=author, icon_url=author.avatar)
                embed.add_field(name='Owner:', value=author.mention)

                if found_tag['aliases'] != []:
                    tag_aliases = '`, `'.join(found_tag['aliases'])
                    embed.add_field(name='Aliases:', value=f'`{tag_aliases}`')

                embed.add_field(name='Uses:', value=found_tag['uses'])

                # Converting tag_creation_date into a readable string and adding it to the embed.
                stripped_datetime = datetime.strptime(found_tag["tag_creation_date"], "%Y-%m-%d %H:%M:%S.%f")
                pretty_time = stripped_datetime.strftime(self.bot.displayed_strftime)

                embed.set_footer(text=f'Created at: {pretty_time} UTC')
                await msg.edit(embed=embed)

                return

    @commands.hybrid_command(description='Lists all the tags that belong to you or someone else.')
    async def taglist(self, ctx, member:discord.Member=None):
        """
        Tries to find all tags that have 'member.id' as their 'owner_id'
            If doesn't find one, return
        If finds at least one, creates an embed with:
            paginator - '#number' 'name' \n
        """
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)
        
        if not member:
            member = ctx.author

        with open(TAGS_LIST_JSON, "r") as infile:
            tags_dict = json.load(infile)

        n = 1

        paginator = commands.Paginator(prefix="", suffix="")

        for tag_name in tags_dict:
            if tags_dict[tag_name]["owner_id"] == member.id:
                paginator.add_line(line=f"**#{n}**: `{tags_dict[tag_name]['name']}`")
                n += 1
        
        desc = ""
        if len(paginator.pages) == 0:
            embed = discord.Embed(description=f"{member.mention} has no tags.", color=self.bot.color)
            await msg.edit(embed=embed)
            return

        for page in paginator.pages:
            desc += page

        embed = discord.Embed(title=f"All {member}'s Tags", description=desc, color=self.bot.color)
        await msg.edit(embed=embed)

    @commands.hybrid_command(description='Deletes an existing tag.', aliases=['deltag'])
    async def deletetag(self, ctx, name:str):
        embed = discord.Embed(description='Working...', color=self.bot.color)
        msg = await ctx.send(embed=embed)

        with open(TAGS_LIST_JSON, 'r') as infile:
            tags_dict = json.load(infile)

        if name not in tags_dict:
            embed = discord.Embed(description='Tag not found.', color=self.bot.color)
            await msg.edit(embed=embed)
            return


        if tags_dict[name]['owner_id'] != ctx.author.id:
            if ctx.author.id != self.bot.owner_id:
                embed = discord.Embed(description='You cannot delete a tag that is not owned by you.', color=self.bot.color)
                await msg.edit(embed=embed)
                return

        del tags_dict[name]['name']
        del tags_dict[name]['description']
        del tags_dict[name]['owner_id']
        del tags_dict[name]['uses']
        del tags_dict[name]['tag_creation_date']
        del tags_dict[name]

        with open(TAGS_LIST_JSON, 'w') as f:
            json.dump(tags_dict, f)

        embed = discord.Embed(description='Successfully deleted tag.', color=self.bot.color)
        await msg.edit(embed=embed)

    

    

async def setup(bot):
    await bot.add_cog(Tags(bot))