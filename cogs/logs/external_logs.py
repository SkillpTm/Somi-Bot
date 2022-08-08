###package#import###############################################################################

import nextcord
from nextcord import Color
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from utilities.partial_commands import get_user_avatar, make_bulk_messages_csv, embed_builder
from utilities.variables import AUDIT_LOG_ID



class external_logs(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###on#member#ban###########################################################

    @commands.Cog.listener()
    async def on_member_ban(self,
                            guild,
                            user):
        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        async for entry in guild.audit_logs(limit=1):
            if entry.user == self.client.user:
                return

        member_avatar_url = get_user_avatar(entry.user)

        embed = embed_builder(color = Color.red(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,

                              field_one_name = "External ban:",
                              field_one_value = f"{entry.user.mention} banned: {entry.target.mention} without using {self.client.user.mention}",
                              field_one_inline = False,

                              field_two_name = "Reason:",
                              field_two_value = entry.reason,
                              field_two_inline = False)

        print(f"{entry.user}: External ban {entry.target}\nReason: {entry.reason}")

        await AUDIT_LOG.send(embed=embed)

    ###on#member#unban###########################################################

    @commands.Cog.listener()
    async def on_member_unban(self,
                              guild,
                              user):
        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        async for entry in guild.audit_logs(limit=1):
            if entry.user == self.client.user:
                return

        print(f"{entry.user}: External unban {entry.target}")

        member_avatar_url = get_user_avatar(entry.user)

        embed = embed_builder(color = Color.red(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,

                              field_one_name = "External unban:",
                              field_one_value = f"{entry.user.mention} unbanned: {entry.target.mention} without using {self.client.user.mention}",
                              field_one_inline = False)

        await AUDIT_LOG.send(embed=embed)

    ###on#bulk#message#delete###########################################################

    @commands.Cog.listener()
    async def on_bulk_message_delete(self,
                                     messages):
        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        guild = messages[0].author.guild

        async for entry in guild.audit_logs(limit=1):
            if entry.user == self.client.user:
                return

        print(f"{entry.user}: External purge {entry.target}")

        make_bulk_messages_csv(messages)

        member_avatar_url = get_user_avatar(entry.user)

        embed = embed_builder(color = Color.red(),
                              author = "Mod Activity",
                              author_url = member_avatar_url,

                              field_one_name = "External purge:",
                              field_one_value = f"{entry.user.mention} purged: `{len(messages)} message(s)` in {entry.target.mention}without using {self.client.user.mention}",
                              field_one_inline = False,

                              field_two_name = "Note:",
                              field_two_value = "It is possible that there is no CSV after this message or that messages are missing. This is due to the messages not being cached anymore. In this case there is nothing I can do.",
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)
        await AUDIT_LOG.send(file=nextcord.File("./storage/bulk_messages.csv"))

    ###on#member#kick###########################################################

    @commands.Cog.listener()
    async def on_member_remove(self,
                               member):
        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        guild = member.guild

        async for entry in guild.audit_logs(limit=1):
            if str(entry.action) != "AuditLogAction.kick":
                return
            if entry.user == self.client.user:
                return

        print(f"{entry.user}: External kick {entry.target}")

        member_avatar_url = get_user_avatar(entry.user)

        embed = embed_builder(color = Color.red(),
                              author = "Mod Activity",
                              author_url = member_avatar_url,

                              field_one_name = "External kick:",
                              field_one_value = f"{entry.user.mention} kicked: {entry.target.mention} without using {self.client.user.mention}",
                              field_one_inline = False,

                              field_two_name = "External kick:",
                              field_two_value = entry.reason,
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)



def setup(client):
    client.add_cog(external_logs(client))