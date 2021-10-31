# Helper bot for Discord
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
import os
from dotenv import load_dotenv
import random
import logging
import pymongo
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

with open('dadjokes') as dad:
    jokes = dad.read().splitlines()
with open('wisdoms') as wis:
    quotes = wis.read().splitlines()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_CONN = os.getenv('CONN_URL')

client = discord.Client()
bot = commands.Bot(command_prefix='j!')

cluster = MongoClient(DB_CONN)
db = cluster['jenkins']
coll = db['jenkincoll']

# Event function definitions
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected.')

# User command function definitions
@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('Greetings.')

@bot.command(name='dadjoke', help='Presents a random dad joke')
async def dad_joke(ctx):
    await ctx.send(random.choice(jokes))

@bot.command(name='wisdom', help='Presents a random wisdom')
async def sayings(ctx):
    await ctx.send(random.choice(quotes))

@bot.command(name='coinflip', help='Flips a coin')
async def c_flip(ctx):
    c_result = ['Heads', 'Tails']
    await ctx.send(f':coin: The result is {random.choice(c_result)}. :coin: ')

@bot.command(name='roll', help='Rolls a die. Will default to six-sided if a number is not given')
async def dice(ctx, sides=6):
    d_roll = random.randint(1, sides)
    await ctx.send(f':game_die: You rolled a {d_roll}. :game_die:')

@bot.command(name='smug', help='Presents smug')
async def anismug(ctx):
    path = random.choice(os.listdir('smug/'))
    await ctx.send(file=discord.File('smug/' + path))

@bot.command(name='jankenpon', help='Play rock paper scissors with the bot')
async def rps(ctx, choice):
    choice = choice.capitalize()
    comp = random.choice(['Rock', 'Paper', 'Scissors'])
    comparison = {'Rock': 'Scissors', 'Scissors': 'Paper', 'Paper': 'Rock'}
    if comparison[choice] == comp:
        await ctx.send(f'{comp}. You win!')
    elif comp == choice:
        await ctx.send(f'{comp}. It\'s a draw.')
    else:
        await ctx.send(f'{comp}. You lose.')


@bot.command(name='admincheck')
@has_permissions(administrator=True)
async def adcheck(ctx):
    await ctx.send('Admin check passed')

@bot.command(name='nickname', help='Changes a user\'s nickname. ADMIN')
@has_permissions(administrator=True)
async def change_nickname(ctx, member: discord.Member, nname):
    await member.edit(nick=nname)
    await ctx.send(f'Nickname has been changed to {nname}.')

@bot.command(name='createtc', help='Creates a text channel. Requires a name for the new channel. ADMIN')
@has_permissions(administrator=True)
async def create_txt(ctx, cname):
    await ctx.message.guild.create_text_channel(cname)
    await ctx.send(f'Text channel **{cname}** created.')

@bot.command(name='createvc', help='Creates a voice channel. Requires a name for the new channel. ADMIN')
@has_permissions(administrator=True)
async def create_vc(ctx, cname):
    await ctx.message.guild.create_voice_channel(cname)
    await ctx.send(f'Voice channel **{cname}** created.')

@bot.command(name='addrole', help='Adds a new role to the server. ADMIN')
@has_permissions(administrator=True)
async def add_role(ctx, rname=None):
    if not rname:
        await ctx.send('You must choose a name for the new role.')
    else:
        await ctx.guild.create_role(name=rname)
        await ctx.send(f'New role **{rname}** created.')



bot.run(TOKEN)
