import os
import json
import asyncio
import platform
import discord
from discord.ext import commands
import feedparser
from keep_alive import keep_alive
from datetime import datetime

configfile = json.load(open("config.json", "r", encoding="utf-8"))

Token = configfile["Token"] # Bot token

Bot_Prefix = configfile["Bot_Prefix"] # Bot prefix

Feed_URL = configfile["Feed_URL"] # RSS Feed link

Channel_ID = int(configfile["Channel_ID"]) # Channel id in which you need to send the updates

LogChannel_ID = int(configfile["LogChannel_ID"]) #log of updates  Channel ID

Wait = int(configfile["Wait"]) # Delay of sending the request in seconds

client = commands.Bot(command_prefix=Bot_Prefix)

@client.event
async def on_ready():
    print(f"Bot is ready to be used!")

    Feed_channel = client.get_channel(Channel_ID)
    Log_channel = client.get_channel(LogChannel_ID)

    # Online Notice
    await Log_channel.send(f""" **+ BOT ONLINE!** - {datetime.now()} - Bot Prefix: `{Bot_Prefix}` - Request Send Time: *{Wait}* Seconds """)

    while True:
        try:
            # Feedparser is real helpful here
            blog_feed = feedparser.parse(Feed_URL)

            # Get the title of the current video at top
            TITLE = blog_feed.entries[0].title

            #  If the current title is same as the last title recieved
            # (stored in old.txt) btw
            # This will be skipped and will be tried again in the next round
            try:
                with open("old.txt", "r", encoding="utf-8") as old_file:
                    OLD_TITLE = old_file.read()
            except:
                OLD_TITLE = "NO FILE FOUND"

            if TITLE == OLD_TITLE:
                await Log_channel.send(f"""**- Info:** RSS Feed not updated yet.""")

            # If the above check is false
            else:
                with open("old.txt", "w", encoding="utf-8") as new_file:
                    new_file.write(TITLE)

                LINK = blog_feed.entries[0].link
                PUB_DATE = blog_feed.entries[0].published
                SUMMARY = blog_feed.entries[0].summary
                print("-"*25)
                print("Title:", TITLE)
                print("Link:", LINK)
                print("Published Date:", PUB_DATE)
                print("Summary:", SUMMARY)

                embed = discord.Embed(
                    title=f"""{TITLE}""", color=0x00ff00)
                embed.set_author(name=f"{client.user.name}",
                                 icon_url=f"{client.user.avatar_url}")
                embed.add_field(
                    name="Title", value=f"""{TITLE}""", inline=False)
                embed.add_field(
                    name="Link", value=f"""{LINK}""", inline=False)
                embed.add_field(name="Published on",
                                value=f"""{PUB_DATE}""", inline=False)
                embed.add_field(name="Decription",
                                value=f"""{SUMMARY}""", inline=False)
                await Feed_channel.send(embed=embed)
                await Log_channel.send(f"""**+ Success:** Sent *{TITLE}*""")

        except Exception as e:
            # If this happens....
            # DAMN! something is really wrong
            await Log_channel.send(f"""**- Error:** {e}""")

        await asyncio.sleep(Wait)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('^d hello'):
        await message.channel.send('Hello!')

keep_alive()
client.run(Token)
