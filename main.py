import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
import asyncio
import logging
import logging.handlers


load_dotenv()
TOKEN = os.getenv('TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
myID = os.getenv('myID')

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=",,", intents=intents, owner_id=myID)
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

bot.help_command = MyHelpCommand()


defaultPrefix = "`"
prefix = defaultPrefix



@bot.event
async def on_ready():
    print("Bot ready!")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.custom, name="i went to the beach that makes you old")
    )
    print('status set')
   

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def setup_logging():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename='bot.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8} {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

async def main():
    await setup_logging()
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)
    


if __name__ == "__main__":
    asyncio.run(main())
