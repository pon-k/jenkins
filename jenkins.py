# Helper bot for Discord
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
import os
from dotenv import load_dotenv
import random
import logging

logging.basicConfig(level=logging.INFO)

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

@bot.command(name='coinflip', help='Flip a coin.')
async def c_flip(ctx):
    c_result = ['Heads', 'Tails']
    await ctx.send(f':coin: The result is {random.choice(c_result)}. :coin: ')

@bot.command(name='roll', help='Roll a die.')
async def dice(ctx, sides=6):
    d_roll = random.randint(1, sides)
    await ctx.send(f':game_die: You rolled a {d_roll}. :game_die:')

@bot.command(name='admincheck')
@has_permissions(administrator=True)
async def adcheck(ctx):
    await ctx.send('Admin check passed')

@bot.command(name='nickname')
@has_permissions(administrator=True)
async def change_nickname(ctx, member: discord.Member, nname):
    await member.edit(nick=nname)
    await ctx.send(f'Nickname has been changed to {nname}.')




bot.run(TOKEN)