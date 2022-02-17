from discord.ext import commands  # Again, we need this imported
import discord
from discord.ext import commands
from discord.ext import tasks


class Feedback(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        @client.command()
        async def feedback(ctx, *, question):

            channel = client.get_channel(943259931346350080)

            embed = discord.Embed(name=ctx.author.display_name,
                                  title="FeedBack",
                                  description=f"{question}",
                                  color=discord.Color.blue())
            embed.set_author(name=ctx.author.display_name,
                             icon_url=ctx.author.avatar_url)

            embed.set_thumbnail(
                url="https://memegenerator.net/img/instances/64051739.jpg")

            await channel.send(embed=embed)

            await ctx.send('Thanks for the feedback')

def setup(client: commands.Bot):
    client.add_cog(Feedback(client))
    
