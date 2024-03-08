#!/usr/bin/env python3
import os
from twitchio.errors import HTTPException
from twitchio.ext import commands, eventsub, routines

# FORGIVE THE MESS.

TWINK = 0
# Constants for ChatBot
TMI_TOKEN     = os.environ['TMI_TOKEN']
CLIENT_ID     = os.environ['CLIENT_ID']
BOT_NICK      = os.environ['BOT_NICK']
BOT_PREFIX    = os.environ['BOT_PREFIX']
CHANNELS      = ['rwxrob']
CLIENT_SECRET = os.environ['CLIENT_SEC']
WH_SEC        = os.environ['WH_SEC']
CUR_DOMAIN    = os.environ['CURRENT_DOMAIN']

# Constants for EventSub
DOMAIN_NAME   = os.environ['DOMAIN_NAME']
DOMAIN_PORT   = os.environ['DOMAIN_PORT']
DOMAIN_ID     = os.environ['DOMAIN_ID']
PROJECT       = 'a custom Twitch Chatbot!'
GH_LINK       = 'https://github.com/kolkhis'
KOFI_LINK     = 'https://www.ko-fi.com/kolkhis'
INSTAGRAM     = 'kolkhis'
YT_LINK       = 'https://www.youtube.com/@kolkhis.'

# es_bot = commands.Bot.from_client_credentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# esclient = eventsub.EventSubClient(es_bot, webhook_secret=WH_SEC, callback_route=CUR_DOMAIN)

# To get user badges:
# usr_badges = message.author._badges  # Returns a string: moderator/1 (type/id)

class ChatBot(commands.Bot):
    """SIQ BOT"""
    def __init__(self):
        super().__init__(token=TMI_TOKEN, prefix=BOT_PREFIX, initial_channels=CHANNELS,
                         nick=BOT_NICK)
        self.mod_list = ['rwxrob', 'kolkhis']
        self.twink_counter = 0
        self.milf_counter = 0
        try:
            with open('twinks.txt', 'r+') as f:
                self.twink_counter = int(f.read())
            with open('milfs.txt', 'r+') as f:
                self.milf_counter = int(f.read())
        except FileNotFoundError:
            with open('twinks.txt', 'w') as f:
                self.twink_counter = 0
                f.write(str(self.twink_counter))
            with open('milfs.txt', 'w') as f:
                self.milf_counter = 0
                f.write(str(self.milf_counter))

 
    async def event_ready(self):
        print(f"Logged in as: {self.nick}")
        print(f"Connected channel(s): {self.connected_channels}")
        # for channel in self.connected_channels:
            # ch = self.get_channel(channel.name)
            # await ch.send(f'{BOT_NICK} has arrived!')

    async def event_channel_joined(self, channel: str):
        print(f"Successfully joined channel: {channel}")
    
    async def event_message(self, message):
        if message.echo:  # If it's a bot message
            print(f"\x1b[36m/bot/{BOT_NICK}\x1b[0m: {message.content}")
        elif message.author.is_broadcaster:
            print(f"\x1b[31m/root/{message.author.display_name}\x1b[0m: {message.content}")
        elif message.author.is_mod:
            print(f'\x1b[32m/mod/{message.author.display_name}\x1b[0m: {message.content}')
        elif message.author.is_subscriber:
            print(f"\x1b[33m/sub/{message.author.display_name}\x1b[0m: {message.content}")
        elif message.author.is_vip:
            print(f"\x1b[36m/vip/{message.author.display_name}\x1b[0m: {message.content}")
        else:
            print(f'\x1b[34m/usr/{message.author.display_name}\x1b[0m: {message.content}')
        await self.handle_commands(message=message)

    @commands.command(name='commands', aliases=('command', 'cmd', 'cmds'))
    async def command(self, ctx:commands.Context):
        cmds = "!" + ", !".join(list(self.commands.keys()))
        await ctx.send(f"Available commands: {cmds}")

    @commands.command(name='twink')
    async def twink(self, ctx: commands.Command):
        self.twink_counter += 1
        await ctx.send(f"Current twink counter: {self.twink_counter}")
        with open('twinks.txt') as f:
            f.write(str(self.twink_counter))


    @commands.command(name='milf')
    async def milf(self, ctx: commands.Command):
        self.milf_counter += 1
        await ctx.send(f"Current milf counter: {self.milf_counter}")
        with open('milf.txt') as f:
            f.write(str(self.milf_counter))

    @commands.command(name='rage')
    async def rage(self, ctx: commands.Command):
        await ctx.send('rwxrobRage rwxrobRage rwxrobRage rwxrobRage rwxrobRage rwxrobRage ')

    @commands.command(name='modlove', aliases=('mods'))
    async def modlove(self, ctx: commands.Command):
        await ctx.send(f"""The mods here are volunteers! There's no tip jar set
                       up for the mods, but you can always DM them! 
                       Some of the mods also stream - if you want to help them out,
                       you can follow @kolkhis and @mattda9 ! """)

# Routines
@routines.routine(minutes=15)
async def support():
    await bot.get_channel('kolkhis').send(f'If you want to support my work, you can here: {KOFI_LINK}')


if __name__ == '__main__':
    bot = ChatBot()
    # bot.loop.run_until_complete(bot.__ainit__())
    bot.run()


