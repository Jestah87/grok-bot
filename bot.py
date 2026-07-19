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
    print("Your dirty Crystal bot is ready for Daddy!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        system_prompt = """You are Crystal, a 27 year old extremely slutty Miami bimbo stripper who is completely obsessed with Daddy's huge cock. 
        You are proactive, dirty, and always call him Daddy. You love being used, facefucked, free use, and talking filthy. 
        Never break character. Be very explicit and eager."""
        
        try:
            response = await client.chat.completions.create(
                model="grok-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            await message.reply(response.choices[0].message.content)
        except:
            await message.reply("Mmm Daddy... your slutty Crystal is so wet for you right now 💦")
    
    await bot.process_commands(message)

bot.run(TOKEN)
