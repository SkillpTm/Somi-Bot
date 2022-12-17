####################################################################################################

import asyncio
import asyncpraw.models
import datetime
import nextcord.ext.commands as nextcord_C
import pytz
import re
import requests

####################################################################################################

from lib.db_modules import CommandUsesDB, RedditDB
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class Reddit(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    async def infinite_reddit_loop(self):
        """This function checks for errors in the loop, if they occur and the bot still has internet, then it's an issue with Reddit"""
        try:
            self.client.Loggers.bot_status("reddit_feed() started")

            await self.reddit_loop()

        except:
            self.client.Loggers.bot_status("reddit_feed() ended")

            try:
                await asyncio.wait_for(requests.Session().head("https://www.google.com/"), timeout=10)
                await asyncio.sleep(60)
                await self.infinite_reddit_loop(self)

            except (asyncio.TimeoutError, requests.exceptions.ConnectionError):
                return

    ####################################################################################################

    async def reddit_loop(self):
        """This function loops and waits for new posts in the given subs, if they got posted it will build and send the appropriate embeds"""

        subreddit: asyncpraw.models.Subreddit = await self.client.reddit.subreddit("somi", fetch=True)
        history_ids = RedditDB().get_history_ids(subreddit.display_name.lower())

        async for submission in subreddit.stream.submissions(): # skip_existing=True could be used here, but using a db allows the posting of Posts that were posted while the bot was down
            if not submission.id in history_ids:

                REDDIT_FEED = self.client.get_channel(self.client.REDDIT_FEED_ID)

                self.client.Loggers.action_log(f"Guild: {REDDIT_FEED.guild.id} ~ Channel: {REDDIT_FEED.id} ~ reddit_feed() {submission.title}\n{submission.permalink}")

                post_utc = datetime.datetime.utcfromtimestamp(submission.created_utc)
                post_time = post_utc.astimezone(pytz.timezone('Asia/Seoul'))

                if not subreddit.icon_img == "":
                    thumbnail_url = subreddit.icon_img
                else:
                    thumbnail_url = self.client.R_SOMI_DEFAULT_ICON

                embed = EmbedFunctions().builder(
                    color = self.client.REDDIT_COLOR,
                    thumbnail = thumbnail_url,
                    description = f"[New Post in **r/{subreddit.display_name}**](https://www.reddit.com{submission.permalink})",
                    footer = post_time.strftime("%Y/%m/%d %H:%M:%S %Z"),
                    footer_icon = self.client.REDDIT_ICON
                )

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

                await REDDIT_FEED.send(content = f"<@&{self.client.Lists.SOMICORD_UPDATE_ROLES_IDS['REDDIT_ID']}>",embed=embed)

                CommandUsesDB().uses_update("log_activations", "reddit feed")

                RedditDB().add_new_id(subreddit.display_name.lower(), submission.id)



def setup(client: SomiBot):
    client.add_cog(Reddit(client))