from discord.ext import commands # Again, we need this imported
import requests
import json
import discord
from discord.ext import tasks
from datetime import datetime
from googleapiclient.discovery import build
import os
import asyncio
import platform
import feedparser
from keep_alive import keep_alive


class Feed(commands.Cog):
  
  def __init__(self, client: commands.Bot):

        self.client = client
        configfile = json.load(open("config.json", "r", encoding="utf-8"))
        Feed_URL = configfile["Feed_URL"] # RSS Feed link
        Channel_ID = int(configfile["Channel_ID"]) # Channel id in which you need to send the updates
        LogChannel_ID = int(configfile["LogChannel_ID"]) #log of updates  Channel ID
        Wait = int(configfile["Wait"]) # Delay of sending the request in seconds

        @client.event
        async def on_ready():

          Feed_channel = client.get_channel(Channel_ID)
          Log_channel = client.get_channel(LogChannel_ID)
          
          # Online Notice
          await Log_channel.send(f""" **+ BOT ONLINE!** - {datetime.now()} - Bot Prefix: . - Request Send Time: *{Wait}* Seconds """)

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


def setup(client: commands.Bot):
    client.add_cog(Feed(client))
