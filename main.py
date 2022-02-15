import requests
import json
import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from googleapiclient.discovery import build

client = commands.Bot(command_prefix=".")
configfile = json.load(open("config.json", "r", encoding="utf-8"))
Key = configfile["Key"]
BlogID = configfile["BlogID"]
Token = configfile["Token"]
Roles = ["ATOM", "BOT"]  # Add your server roles here.
blog = build("blogger", "v3", developerKey=Key)

@client.event
async def on_ready():
    print("Bot has started running")
    await client.change_presence(activity=discord.Game(name="cmd: .search"))


@client.command()
async def search(ctx, arg):
    search_term = str(arg).replace(" ", "%")
    base_url = "https://www.googleapis.com/blogger/v3/blogs/" + BlogID + "/posts/search"
    complete_url = base_url + "?q=" + search_term + \
        "&key=" + Key
    response = requests.get(complete_url)
    result = response.json()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    embed = discord.Embed(title="List of Search results",
                          description="Checked on " + f"{current_time}\n",
                          color=0x349bfc)
    embed.set_author(name="Your Website Name")
    embed.set_thumbnail(url="https://www.yourwebsite.com/favicon.ico")
    try:
        for count, value in enumerate(result["items"]):
            title = result["items"][count]["title"]
            url = result["items"][count]["url"]
            embed.description = embed.description + \
                f"{count + 1}. [{title}]({url})\n"
        embed.set_footer(text='This message will be deleted in 60min.')

        await ctx.send(
            embed=embed,
            delete_after=3600.0,
        )
    except:
        info = discord.Embed(title="Something is wrong")
        await ctx.send(embed=info)


client.recentPosts = None
client.recentPostsTime = None
client.recentPostsEdit = None

client.load_extension("feed")

client.run(Token, bot=True)
