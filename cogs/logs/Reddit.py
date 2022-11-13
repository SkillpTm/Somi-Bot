###package#import###############################################################################

import dotenv
import asyncio
import asyncpraw
import datetime
import nextcord
import os
import pytz
import re

dotenv.load_dotenv()

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_reddit import get_history_ids, add_new_id_to_database
from database.database_command_uses import uses_update
from utilities.partial_commands import embed_builder
from utilities.variables import REDDIT_ID, REDDIT_FEED_ID, SUBREDDIT_ICON, REDDIT_COLOR, REDDIT_ICON



async def reddit_loop(client):
    reddit = asyncpraw.Reddit(client_id=os.getenv("REDDIT_ID"),
                              client_secret=os.getenv("REDDIT_SECRET"),
                              username="SomiBot",
                              password=os.getenv("REDDIT_PASSWORD"),
                              user_agent="testscript by u/SkillpTm")

    subreddit = await reddit.subreddit("somi", fetch=True)

    history_ids = get_history_ids()

    print("reddit_feed() online")

    async for submission in subreddit.stream.submissions(): # skip_existing=True could be used here, but using a db allows the posting of Posts that were posted while the bot was down
        if not submission.id in history_ids:
            print(f"reddit_feed() {submission.title}\n{submission.permalink}")

            REDDIT_FEED = client.get_channel(REDDIT_FEED_ID)

            post_utc = datetime.datetime.fromtimestamp(submission.created_utc)
            post_time = post_utc.astimezone(pytz.timezone('Asia/Seoul'))

            if not subreddit.icon_img == "":
                thumbnail_url = subreddit.icon_img
            else:
                thumbnail_url = SUBREDDIT_ICON

            embed = embed_builder(description = f"[New Post in **r/{subreddit.display_name}**](https://www.reddit.com{submission.permalink})",
                                  color = REDDIT_COLOR,
                                  thumbnail = thumbnail_url,
                                  footer = post_time.strftime("%Y/%m/%d %H:%M:%S %Z"),
                                  footer_icon = REDDIT_ICON)

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
                    all_images = [image_url['s']['u'] for image_url in submission.media_metadata.values()]

                    embed.set_image(url=all_images[0])

            else:
                embed.add_field(name=f"`{submission.link_flair_text}` {submission.title}"[:256], value=submission.selftext[:300], inline=False)

            await REDDIT_FEED.send(content = f"<@&{REDDIT_ID}>",embed=embed)

            uses_update("log_activations", "reddit feed")

            add_new_id_to_database(submission.id)



async def infinite_reddit_loop(self):
    try:
        await reddit_loop(self.client)
    except:
        await asyncio.sleep(60)
        await infinite_reddit_loop(self)



class Reddit(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###reddit###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_ready(self):
        await infinite_reddit_loop(self)



def setup(client):
    client.add_cog(Reddit(client))