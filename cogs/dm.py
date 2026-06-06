import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
from main import bot, myID, ACCOUNT_ID, API_TOKEN
import requests
import json
import pickle
import re
from typing import Literal

url = f"https://api.groq.com/openai/v1/chat/completions"

headers = {
    "authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

prompts = {
    "default": "You are a helpful chatbot operating on discord. You will provide direct responses without any fluff, do not provide any unnecessary explanation unless explicitly asked to e.g. 'hey, what's an apple'; 'it's a red fruit' is the correct response, NO fun facts, NO further explanation. You will also always type in all lowercase (you can capitalise some stuff, but don't start sentences with capitals or capitalise nouns/names by default, type casual) don't use emojis, only use commas, question marks, and exclamation marks. The user's name is ",
    "none": ""
}

maxmemory = 50

filename = 'memory.pk'

class Dm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


if os.path.exists(filename) and os.path.getsize(filename) > 0:
    with open(filename, 'rb') as fi:
        memory = pickle.load(fi)
else:
    memory = []

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    async def ai_response(self, character, prompt, name):
pleas            if character in prompts:
                initial_prompt = prompts[character] + name + " Here is the user's prompt: "
                local_memory = "\n".join(memory)
                local_memory = local_memory[len(memory) - 5000:]
                memory_prompt = "This is the last 50 messages of this channel (may be cut off due to character count restrictions.): " + local_memory + "\n"
                messages =[
                    {"role": "system", "content": memory_prompt},
                    {"role": "system", "content": initial_prompt},
                    {"role": "user", "content": prompt},
                ]
                data = {
                    "model": "llama-3.1-8b-instant",
                    "messages": messages
                }
                    
                    
                response = requests.post(url, headers=headers, data=json.dumps(data))

                if response.status_code == 200:
                    result = response.json().get("choices", {})
                    if result:
                        response_text = result[0].get("message", {}).get("content", "No response")
                        response = f"{character.title()}: {response_text}"
                    else:
                        response = "No response generated."
                else:
                    response = f"Error: {response.status_code}"
                return response

    async def add_mem(self, message):
        if "memory chunk" in message.lower():
            return
        else:
            memory.append(message)
            if len(memory) > maxmemory:
                memory.pop(0)
            with open(filename, 'wb') as fi:
                pickle.dump(memory, fi)
                

    @commands.command(aliases=["mem"])
    async def printmem(self, ctx):
        if int(ctx.author.id) == int(myID):
            memstring = "\n".join(memory)
            chunks = [memstring[i:i+1900 ] for i in range(0, len(memstring), 1900)]
            i = 0
            for chunk in chunks:
                await ctx.send(f"memory chunk {i}: {chunk}")
                i = i+1
    
    @commands.command(aliases=["clear"])
    async def clearmem(self, ctx):
        if int(ctx.author.id) == int(myID):
            memory = []

    @commands.command(aliases=["clear"])
    async def clearmem(self, ctx):
        if int(ctx.author.id) == int(myID):
            with open(filename, 'wb') as fi:
                pickle.dump([], fi)
            with open(filename, 'rb') as fi:
                global memory
                memory = pickle.load(fi)
            await ctx.send("command run")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.channel.type is discord.ChannelType.private:
                if message.author.id == int(myID):
                    if not message.startswith(",,"):
                        await self.add_mem(message)
                        response = await self.ai_response("default", message, message.user.display_name)
                        await message.channel.send(response)
        except Exception as e:
                    user = await self.bot.fetch_user(myID)
                    await user.send("Exception in dmai: ```" + str(e) + "```")

async def setup(bot):
    await bot.add_cog(Dm(bot))
