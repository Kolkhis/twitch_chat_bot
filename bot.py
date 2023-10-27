import os
from twitchio.errors import HTTPException
from twitchio.ext import commands, eventsub

# FORGIVE THE MESS.

# Constants for ChatBot
TMI_TOKEN     = os.environ['TMI_TOKEN']
CLIENT_ID     = os.environ['CLIENT_ID']
BOT_NICK      = os.environ['BOT_NICK']
BOT_PREFIX    = os.environ['BOT_PREFIX']
CHANNELS      = [os.environ['CHANNEL']]
CLIENT_SECRET = os.environ['CLIENT_SECRET']
WH_SEC        = os.environ['TW_SEC']

# Constants for EventSub
DOMAIN_NAME   = os.environ['DOMAIN_NAME']
DOMAIN_PORT   = os.environ['DOMAIN_PORT']
DOMAIN_ID     = os.environ['DOMAIN_ID']

PROJECT       = 'a custom Twitch Chatbot!'
GH_LINK       = 'https://github.com/kolkhis'
KOFI_LINK     = 'https://www.ko-fi.com/kolkhis'

es_bot = commands.Bot.from_client_credentials(client_id=CLIENT_ID, client_secret=WH_SEC)
esclient = eventsub.EventSubClient(es_bot, webhook_secret=CLIENT_SECRET, callback_route=DOMAIN_NAME)


# [x] Before subscribing to events, you must create a callback that listens for events
# [x] Your callback must use SSL and listen on port 443.

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# For EventSub:
# This ext requires you to have a public facing ip AND domain, and to be able to receive inbound requests."
#        Requires TLS/SSL, TwitchIO doesn't support this. Reverse proxy - nginx - can handle this.
# Opted for ngrox instead of nginx
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class ChatBot(commands.Bot):
    """SIQ BOT"""
    def __init__(self):
        super().__init__(token=TMI_TOKEN, prefix=BOT_PREFIX, initial_channels=CHANNELS,
                         nick=BOT_NICK,)

    # TODO: See notes above and make this work.
    async def __ainit__(self) -> None:
        self.loop.create_task(esclient.listen(port=9091))
        try:
            es_response = await esclient.subscribe_channel_follows_v2(broadcaster="109361217", moderator="109361217")  # Have also tried using integers for the IDs.
            print(f"All things in es_response list:\n{','.join(es_response)}")
        except HTTPException as e:
            print(f"HTTP Exception encountered \n{e.message}\n{e.reason}\n{e.status}\n{e.args}")
 
    async def event_ready(self):
        print(f"Logged in as: {self.nick}")
        print(f"Connected channel(s): {self.connected_channels}")
        # await self.__ainit__()
        # await esclient.subscribe_channel_follows_v2(broadcaster='kolkhis', moderator='iFlipsy')

    async def event_channel_joined(self, channel: str):
        print(f"Successfully joined channel: {channel}")
    
    # TODO: Could use this return to make my own chat overlay!>>>
    async def event_message(self, message):
        if message.echo:  # If it's a bot message
            return
        print(f"{message.author.name}: {message.content}")
        await self.handle_commands(message=message)

    @commands.command()
    async def hi(self, ctx: commands.Context):
        """Should respond to the user when !greet is sent"""
        await ctx.send(f"Hi, {ctx.author.name}!")

    @commands.command()
    async def project(self, ctx: commands.Context):
        await ctx.send(f"Project: Currently working on {PROJECT}")

    @commands.command()
    async def github(self, ctx: commands.Context):
        await ctx.send(f"I don't have a ton of public repos yet, but here's my " \
                       f"GitHub link: {GH_LINK}")

    @commands.command()
    async def donate(self, ctx: commands.Context):
        await ctx.send(f"If you want to donate to the stream, you can! " \
                       f"{KOFI_LINK}")

    @commands.command()
    async def command(self, ctx:commands.Context):
        cmds = "!" + ", !".join(list(self.commands.keys()))
        await ctx.send(f"Available commands: {cmds}")

    @commands.command()
    async def so(self, ctx:commands.Context):
        msg = ctx.message.content
        name = msg.split()[1]  # This works.
        await ctx.send(f"/shoutout {name}")


bot = ChatBot()
bot.loop.run_until_complete(bot.__ainit__())

@bot.event()
async def event_eventsub_notification_follow_v2(payload: eventsub.ChannelFollowData):
    print(f'Received a notification for follow? Payload received:\n{payload=}')
    channel = bot.get_channel('kolkhis')
    await channel.send(f"{payload.data.user.name} followed!")

bot.run()

