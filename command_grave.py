import discord

@commands.hybrid_command(description='Adds an alias to a tag.', aliases=['tagaa'])
    async def tagaddalias(self, ctx, name:str, alias:str):
        """
        Tries to find tag name in tags_list.json.
            If doesn't find it, return.
        Gets the tag information and updates:
            aliases += name
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
                existing_aliases = tags_dict[tag_name]['aliases']
                existing_aliases.append(alias)
                tags_dict[name]['aliases'] = existing_aliases
                
                with open(TAGS_LIST_JSON, 'w') as f:
                    json.dump(tags_dict, f)

                embed = discord.Embed(description='Successfully added alias.', color=self.bot.color)
                await msg.edit(embed=embed)
                return