import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.default()
intents.messages = True
intents.typing = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
openai.api_key = os.getenv('OPENAI_API_KEY')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def ask(ctx, *, question):
    response = openai.Completion.create(
        engine="text-davinci-002", prompt=question, max_tokens=150)
    await ctx.send(response.choices[0].text.strip())

@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # Latency in milliseconds
    await ctx.send(f'Pong! Latency is {latency:.2f}ms.')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Bot Commands', description='Here are the available commands for this bot:', color=discord.Color.green())
    embed.add_field(name='!ask [question]', value='Ask a question to the OpenAI API', inline=False)
    embed.add_field(name='!ping', value='Check the bot\'s latency', inline=False)
    await ctx.send(embed=embed)

bot.run(os.getenv('DISCORD_TOKEN'))
