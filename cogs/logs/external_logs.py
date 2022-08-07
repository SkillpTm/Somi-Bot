###package#import###############################################################################

import nextcord
from nextcord import Color, Embed, Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from utilities.partial_commands import embed_kst_footer, embed_set_mod_author, make_bulk_messages_csv
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

        print(f"{entry.user}: External ban {entry.target}\nReason: {entry.reason}")

        embed = Embed(colour=Color.red())
        embed_kst_footer(embed)
        embed_set_mod_author(entry, embed)

        if entry.reason != None:
            embed.add_field(name = "External ban:", value = f"{entry.user.mention} banned: {entry.target.mention} without using {self.client.user.mention}", inline = False)
            embed.add_field(name = "Reason:", value = entry.reason, inline = False)
        else:
            embed.add_field(name = "External ban:", value = f"{entry.user.mention} banned: {entry.target.mention} without using {self.client.user.mention}", inline = False)

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

        embed = Embed(colour=Color.red())
        embed_kst_footer(embed)
        embed_set_mod_author(entry, embed)

        embed.add_field(name = "External unban:", value = f"{entry.user.mention} unbanned: {entry.target.mention} without using {self.client.user.mention}", inline = False)

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

        embed = Embed(colour=Color.red())
        embed_kst_footer(embed)
        embed_set_mod_author(entry, embed)

        if len(messages) == 1:
            embed.add_field(name = "External purge:", value = f"{entry.user.mention} purged: `{len(messages)} message` in {entry.target.mention}without using {self.client.user.mention}", inline = False)
        else:
            embed.add_field(name = "External purge:", value = f"{entry.user.mention} purged: `{len(messages)} messages` in {entry.target.mention}without using {self.client.user.mention}", inline = False)

        embed.add_field(name = "Note:", value = "It is possible that there is no CSV after this message or that messages are missing. This is due to the messages not being cached anymore. In this case there is nothing I can do.", inline = False)

        await AUDIT_LOG.send(embed=embed)
        await AUDIT_LOG.send(file=nextcord.File("./storage/bulk_messages.csv"))



def setup(client):
    client.add_cog(external_logs(client))