from pathlib import Path
# from discord import channel, client, guild
from discord.ext import commands
from discord.ext import tasks
from src.helper import _sendEmbed, _getPrefix1, _getChannelId, _getRoleId
from itertools import cycle  # for background task
from dotenv import load_dotenv
from discord.utils import to_json
from discord.abc import PrivateChannel
from discord.ext import commands, tasks
from src.contest_calander import _getAllContests
from dateutil.tz import gettz
import discord
import logging
import os
import json
from db import db

# Loading Discord Token
load_dotenv()
dc_token = os.getenv("DISCORD_TOKEN")
# print(f'\n-----------------------------\n{dc_token}\n-----------------------------')


description = '> All in one bot, for now works with Codeforces'

# Logging Stuff
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)

# Intents Stuff
intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix=_getPrefix1,
    description=description, intents=intents,
    help_command=None,
)


@bot.event
async def on_guild_join(guild):
    channel_id = ''

    for channel in guild.text_channels:
        if not isinstance(channel, PrivateChannel):
            channel_id = channel.id

    guildObj = {
        "guild_id": f'{guild.id}',
        "prefix": '-',
        "channel_id": f'{channel_id}',
        "role_id": f'{guild.default_role.id}'
    }

    try:
        db.server_config.insert_one(guildObj)
    except Exception as e:
        await guild.get_channel(int(channel_id)).send("** Something went wrong on server side, please kick and add invite the bot again  **")

    embed = discord.Embed(
        title="Regards π Bot,", url="https://discord.gg/uGWfQY4dj4",
        description="Thanks for inviting me to your server"
    )
    embed.set_thumbnail(url="https://avatars3.githubusercontent.com/pvcodes")
    embed.add_field(
        name="Default Values",
        value=f"**Prefix :** `-`\n**Notification Channel :** <#{int(channel_id)}>\n**Notification Ping Role :** <@&{guild.default_role.id}>", inline=True
    )
    embed.set_footer(text="Hit -help for more help  ")

    channel = guild.get_channel(int(channel_id))

    await channel.send(embed=embed)


@bot.event
async def on_guild_remove(guild):
    print(f'deleting {guild.id}')

    try:
        z = db.server_config.delete_many({"guild_id": f'{guild.id}'})

    except Exception as e:
        print(
            f'--------------------------------------\n{e}\n--------------------------------------')


async def changelog():
    # CHANGELOG FUNCTIONS



# On Bot Ready
@ bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await changelog()


# Background Task
status = cycle([
    'Currently solving problem at universe',
    'OMG, It\'s important'
])


@ tasks.loop(minutes=30)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@ bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        emb = discord.Embed(title="What's that?!",
                            description=f"I've never heard of a command like that before :scream:",
                            color=discord.Color.orange())
        await _sendEmbed(ctx, emb)


@ bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# Loading of cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# For Contest Reminder
if os.path.exists('src/contests.json'):
    os.remove('src/contests.json')

_getAllContests()

# For Server Config
# if not os.path.exists('src/server_config.json'):
#     f = open("src/server_config.json", "x")
#     f.write('{}')

bot.run(dc_token, bot=True, reconnect=True)
