import os
from twitchio.errors import HTTPException
from twitchio.ext import commands, eventsub, routines

# FORGIVE THE MESS.

# Constants for ChatBot
TMI_TOKEN     = os.environ['TMI_TOKEN']
CLIENT_ID     = os.environ['CLIENT_ID']
BOT_NICK      = os.environ['BOT_NICK']
BOT_PREFIX    = os.environ['BOT_PREFIX']
CHANNELS      = [os.environ['CHANNEL']]
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

es_bot = commands.Bot.from_client_credentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
esclient = eventsub.EventSubClient(es_bot, webhook_secret=WH_SEC, callback_route=CUR_DOMAIN)

# [x] Before subscribing to events, you must create a callback that listens for events
# [x] Your callback must use SSL and listen on port 443.


class ChatBot(commands.Bot):
    """SIQ BOT"""
    def __init__(self):
        super().__init__(token=TMI_TOKEN, prefix=BOT_PREFIX, initial_channels=CHANNELS,
                         nick=BOT_NICK)

    async def __ainit__(self) -> None:
        self.loop.create_task(esclient.listen(port=9999))
        try:
            await esclient.subscribe_channel_follows_v2(broadcaster=109361217, moderator=109361217)
        except HTTPException as e:
            print(f"HTTP Exception encountered while subscribing to ChannelFollows: \n{e.message}\n{e.reason}\n{e.args}")
        try:
            await esclient.subscribe_channel_stream_end(broadcaster=109361217)
        except HTTPException as e:
            print(f"HTTP Exception encountered while subscribing to StreamEnd: \n{e.message}\n{e.reason}\n{e.args}")
        # TODO: Auto-shoutout when someone raids.
        # try:
        #     await esclient.subscribe_channel_raid()
        # except HTTPException as e:
        #     print(f"HTTP Exception encountered while subscribing to StreamEnd: \n{e.message}\n{e.reason}\n{e.args}")

 
    async def event_ready(self):
        print(f"Logged in as: {self.nick}")
        print(f"Connected channel(s): {self.connected_channels}")
        for channel in self.connected_channels:
            ch = self.get_channel(channel.name)
            await ch.send(f'{BOT_NICK} has arrived!')

    async def event_channel_joined(self, channel: str):
        print(f"Successfully joined channel: {channel}")
    
    # TODO: Could use this return to make my own chat overlay >>>
    async def event_message(self, message):
        if message.echo:  # If it's a bot message
            return
        # usr_badges = message.author._badges  # Returns a string: moderator/1 (type/id)
        #  print("\033[31;1;4m Hello \033[0m")
        if message.author.is_broadcaster:
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

    @commands.command(name='hi', aliases=('hello', 'sup', 'greet'))
    async def hi(self, ctx: commands.Context):
        """Should respond to the user when !greet is sent"""
        await ctx.send(f"Hi, {ctx.author.display_name}!")

    @commands.command(name='project', aliases=('pj', 'current'))
    async def project(self, ctx: commands.Context):
        await ctx.send(f"Project: Currently working on {PROJECT}")

    @commands.command(name='github', aliases=('gh', 'code'))
    async def github(self, ctx: commands.Context):
        await ctx.send(f"I don't have a ton of public repos yet, but here's my " \
                       f"GitHub link: {GH_LINK}")

    @commands.command(name='donate', aliases=('dono', 'support'))
    async def donate(self, ctx: commands.Context):
        await ctx.send(f"If you want to donate to the stream, you can! " \
                       f"{KOFI_LINK}")

    @commands.command(name='commands', aliases=('command', 'cmd', 'cmds'))
    async def command(self, ctx:commands.Context):
        cmds = "!" + ", !".join(list(self.commands.keys()))
        await ctx.send(f"Available commands: {cmds}")

    @commands.command(name='so', aliases=('shoutout',))
    async def so(self, ctx:commands.Context):
        msg = ctx.message.content
        name = msg.split()[1]  # This works.
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            # print(f"{ctx.author.display_name} initiated a shoutout command for {name}")
            ctx.send(f'/shoutout {name}')  # This doesn't

    @commands.command(name='five', aliases=('5',))
    async def five(self, ctx:commands.Context):
        await ctx.send('"FIVE"')

    @commands.command(name='twitter', aliases=('twt',))
    async def twitter(self, ctx:commands.Context):
        await ctx.send('Twitter: sux')

    # @commands.command(name='instagram', aliases=('ig', 'insta'))
    # async def instagram(self, ctx:commands.Context):
    #     await ctx.send(f'Instagram: {INSTAGRAM}')

    @commands.command(name='youtube', aliases=('yt',))
    async def youtube(self, ctx:commands.Context):
        await ctx.send(f'No videos (yet), but my YouTube is: {YT_LINK}')

    @commands.command(name='lurk', aliases=('afk',))
    async def lurk(self, ctx:commands.Context):
        await ctx.send(f'{ctx.author.display_name} sits in the corner.')

    @commands.command(name='twerkwhilelurk', aliases=('tww', 'twerklurk'))
    async def lurktwerk(self, ctx:commands.Command):
        await ctx.send(f'{ctx.author.display_name} sits in the corner, twerking.')

@es_bot.event()
async def event_eventsub_notification_followV2(payload: eventsub.ChannelFollowData):
    print(f'Received a notification for follow. Payload received:\n{payload=}')
    channel = bot.get_channel('kolkhis')
    if channel:
        await channel.send(f"{payload.user.name} followed! Thanks!")

@es_bot.event()
async def event_eventsub_notification_stream_end(event: eventsub.StreamOfflineData):
    print(f"End of stream!")
    ch = bot.get_channel(event.broadcaster.name)
    if ch:
        await ch.send(f"That's it for today! Thanks for hanging out! If you want to support the stream, you can! {KOFI_LINK}")

# twitchio.ext.eventsub.event_eventsub_notification_raid(event: Channel)
# subscribe_channel_shoutout_create(broadcaster: Union[PartialUser, str, int], moderator: Union[PartialUser, str, int])

# Routines
@routines.routine(minutes=15)
async def support():
    bot.get_channel('kolkhis').send(f'If you want to support my work, you can here: {KOFI_LINK}')


bot = ChatBot()
bot.loop.run_until_complete(bot.__ainit__())

bot.run()
# support.start()


