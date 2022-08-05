###package#import###############################################################################

import datetime
import nextcord
from nextcord import Embed
from nextcord.ext import commands
import asyncpraw
from pytz import timezone
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_reddit import get_history_ids, add_new_id_to_database
from database.database_command_uses import uses_update
from utilities.variables import REDDIT_ID, REDDIT_FEED_ID, SUBREDDIT_ICON, REDDIT_COLOR, CLOCK_ICON, REDDIT_ICON



class reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###reddit###########################################################

    @commands.Cog.listener()
    async def on_ready(self):
        reddit = asyncpraw.Reddit(
            client_id=os.getenv('REDDIT_ID'),
            client_secret=os.getenv('REDDIT_SECRET'),
            username="SomiBot",
            password=os.getenv('REDDIT_PASSWORD'),
            user_agent="testscript by u/SkillpTm")

        subreddit = await reddit.subreddit("somi", fetch=True)

        history_ids = get_history_ids()

        async for submission in subreddit.stream.submissions():
            if not submission.id in history_ids:
                print(f"reddit_feed() {submission.title}\n{submission.permalink}")

                REDDIT_FEED = self.client.get_channel(REDDIT_FEED_ID)

                embed = Embed(description = f"[New Post in **r/{subreddit.display_name}**](https://www.reddit.com{submission.permalink})",
                              colour=REDDIT_COLOR)

                if not subreddit.icon_img == "":
                    embed.set_thumbnail(url=subreddit.icon_img)
                else:
                    embed.set_thumbnail(url=SUBREDDIT_ICON)

                embed.set_author(name= "Subreddit Update", icon_url = REDDIT_ICON)

                format = "%Y/%m/%d %H:%M:%S %Z"
                post_utc = datetime.datetime.fromtimestamp(submission.created_utc)
                now_korea = post_utc.astimezone(timezone('Asia/Seoul'))
                embed.set_footer(text = now_korea.strftime(format), icon_url = CLOCK_ICON)

                clean_flair = re.sub(":.*?:", "", str(submission.link_flair_text))
                
                if clean_flair.endswith(" "):
                    clean_flair = clean_flair[:-1]
                if clean_flair.startswith(" "):
                    clean_flair = clean_flair[-1:]

                if submission.selftext == "":
                    embed.add_field(name=f"`{clean_flair}` {submission.title}"[:256], value=submission.url, inline=False)

                    image_endings = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif"]

                    for ending in image_endings:
                        if submission.url.endswith(ending):
                            embed.set_image(url=submission.url)

                    if submission.url.startswith("https://www.reddit.com/gallery/"):
                        all_images = []
                        image_dict = submission.media_metadata
                        for image_item in image_dict.values():
                            largest_image = image_item['s']
                            image_url = largest_image['u']
                            all_images.append(image_url)

                        embed.set_image(url=all_images[0])

                else:
                    embed.add_field(name=f"`{submission.link_flair_text}` {submission.title}"[:256], value=submission.selftext[:300], inline=False)

                await REDDIT_FEED.send(content = f"<@&{REDDIT_ID}>",embed=embed)

                uses_update("log_activations", "reddit feed")

                add_new_id_to_database(submission.id)

def setup(client):
    client.add_cog(reddit(client))