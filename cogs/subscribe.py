import discord
from discord.ext import commands
import pickle
import os


def dump_users_screams(list_users):
    pickle_out = open(os.path.join('res', 'screams.pickle'), "wb")
    pickle.dump(list_users, pickle_out)
    pickle_out.close()



class Subscribe:
    def __init__(self, bot):
        self.bot = bot
        self.users_screams = bot.users_screams
 
 
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def subscribe(self, ctx):
        if ctx.message.author.id in self.users_screams:
            em = discord.Embed(
                title="Echec !",
                description="Vous êtes déjà abonné au Discord !",
                color=0xFF0000)
        else:
            self.users_screams.append(ctx.message.author.id)
            dump_users_screams(self.users_screams)
            em = discord.Embed(
                title="Abonnement au Discord réussi !",
                description="Vous êtes bien abonné au Discord, préparez vous au spam !",
                color=0x000000)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unsubscribe(self, ctx):
        if ctx.message.author.id in self.users_screams:
            self.users_screams.remove(ctx.message.author.id)
            dump_users_screams(self.users_screams)
            em = discord.Embed(
                title="Désabonnement au Discord réussi !",
                description="Vous vous êtes bien désabonné du Discord, à la revoyure !",
                color=0x000000)
        else:
            em = discord.Embed(
                title="Echec !",
                description="Vous n'êtes pas abonné au Discord !",
                color=0xFF0000)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Subscribe(bot))
