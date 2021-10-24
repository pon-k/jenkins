# Helper bot for Discord
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='j!')

# Event function definitions
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected.')

# User command function definitions
@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('Greetings.')

@bot.command(name='coinflip')
async def c_flip(ctx):
    c_result = ['Heads', 'Tails']
    await ctx.send(f':coin: The result is {random.choice(c_result)}. :coin: ')

bot.run(TOKEN)