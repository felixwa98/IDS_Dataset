import discord
import random
import datetime
import time
from discord.utils import get
from discord.ext import tasks
import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)
import Packages.logging.log_file as log


#import ../Packages.logging.log_file as log

client = discord.Client()
song = ''

#Einlogggen
 
@client.event
async def on_message(message):

    ch_name = str(random.randint(1,6))
    channel = get(message.guild.channels, name = ch_name)
    print(message.guild.channels)
    voicechannel = await channel.connect()
    log.log_event("Telfon; Start")
    voicechannel.play(discord.FFmpegPCMAudio(song))
    while voicechannel.is_playing():
        time.sleep(1)
    await client.logout()
    log.log_event("Telfon; Stop")
 

@client.event
async def on_ready():
    print("Fertig")
    channel = client.get_channel(796045283880337463)
    await channel.send("test")


def choose_random_line(xlist):
    lines = open(xlist).read().splitlines()
    return random.choice(lines)

def main(music):

    global song
    song = choose_random_line(music)


    client.run('API-Key')
