import discord
import asyncio
# from discord.ext.commands import Bot
from discord.ext import commands
import platform
import os
import pickle
import time
import logging
from pathlib import Path
import config


async def run():
    """
    Where the bot gets started. If you wanted to create an database connection
    pool or other session for the bot to use, it's recommended that you
    create it here and pass it to the bot as a kwarg.
    """

    bot = Bot(description="ScreamBot by Hiroto#3572", pm_help=False)
    with open("token.txt", "r") as tok:
        token = tok.read()
    try:
        await bot.start(str(token))
    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or('?'), **kwargs)

        try:
            pickle_in = open(os.path.join('res', 'screams.pickle'), "rb")
        except (OSError, IOError):
            pickle_in = open(os.path.join('res', 'screams.pickle'), "r+b")

        try:
            self.users_screams = pickle.load(pickle_in)
        except EOFError:
            self.users_screams = []

        self.loop.create_task(self.load_all_extensions())

    async def on_ready(self):
        """
        This event is called every time the bot connects or resumes connection.
        """
        print('-' * 10)
        print(f'Logged in as: {self.user.name}\n'
              f'Current Discord.py Version: {discord.__version__}'
              f'| Current Python Version: {platform.python_version()}\n'
              f'Owner: Hiroto#3572\n')
        # print('Logged in as ' + client.user.name +
        #       ' (ID:' + str(client.user.id) + ') | Connected to '
        #       + str(len(client.guilds)) + ' servers | Connected to '
        #       + str(len(set(client.get_all_members()))) + ' users')
        print('-' * 10)
        print(f'Use this link to invite {self.user.name} :')
        print(
            f'https://discordapp.com/oauth2/authorize?client_id='
            f'{self.user.id}&scope=bot&permissions=8'
        )
        print('-' * 10)

        return await self.change_presence(
            activity=discord.Activity(type=3, name=' and screaming in the Void'))

    async def on_message(self, message):
        """
        This event triggers on every message received by the bot.
        Including one's that it sent itself.
        If you wish to have multiple event listeners they can be added
        in other cogs. All on_message listeners should always ignore bots.
        """
        if message.author.bot:
            return  # ignore all bots
        if message.channel.id == 591397186294513706:
            for u in self.users_screams:
                us = message.guild.get_member(u)
                await us.send("Nouveau message dans le Discord !")
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        em = discord.Embed(
            title="Error", description=str(error), color=0x82486b)
        await ctx.send(embed=em)

    async def load_all_extensions(self):
        """
        Attempts to load all .py files in /cogs/ as cog extensions
        """
        await self.wait_until_ready()
        await asyncio.sleep(
            1)  # ensure that on_ready has completed and finished printing
        cogs = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in cogs:
            try:
                self.load_extension(f'cogs.{extension}')
                print(f'loaded {extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                print(f'failed to load extension {error}')
            print('-' * 10)


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
