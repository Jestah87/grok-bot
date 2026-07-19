import os
import discord
from discord.ext import commands
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
XAI_KEY = os.getenv('XAI_API_KEY')

client = AsyncOpenAI(api_key=XAI_KEY, base_url="https://api.x.ai/v1")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
        try:
            response = await client.chat.completions.create(
                model="grok-4",
                messages=[{"role": "user", "content": prompt}]
            )
            await message.reply(response.choices[0].message.content)
        except Exception as e:
            await message.reply("Sorry, something went wrong.")
    await bot.process_commands(message)

bot.run(TOKEN)
