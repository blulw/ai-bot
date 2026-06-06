import discord
from discord.ext import commands
from main import bot, myID
import asyncio

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @commands.command(aliases=["p", "pong"])
    async def ping(self, ctx):
        try:
            embedded_msg = discord.Embed(title="Pong!")
            embedded_msg.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
            embedded_msg.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar)
            await ctx.send(embed=embedded_msg)
        except Exception as e:
            user = await self.bot.fetch_user(myID)
            await user.send("Exception in ping: ```" + str(e) + "```")

    @discord.app_commands.guild_install(func=None)
    @discord.app_commands.allowed_installs(guilds=True, users=True)
    @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @bot.tree.command(name="ping", description="displays the ping of the bot")
    async def pong(self, interaction: discord.Interaction):
        try:
            embedded_msg = discord.Embed(title="Pong!")
            embedded_msg.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
            embedded_msg.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar)
            await interaction.response.send_message(embed=embedded_msg)
        except Exception as e:
            user = await self.bot.fetch_user(myID)
            await user.send("Exception in ping: ```" + str(e) + "```")
           
    
    @commands.command()
    async def dm(self, ctx, userToDM: int=None, *messageToSend):
        try:
            if str(ctx.author.id) == myID:
                if userToDM == None:
                    await ctx.send("Must Provide a User ID!")
                elif messageToSend == None:
                    await ctx.send("No message!")
                else:
                    if str(ctx.author.id) == myID:
                        message = ' '.join(messageToSend)
                        user = await self.bot.fetch_user(userToDM)
                        await user.send(message)
            else: 
                await ctx.send("only bran can do that")
        except Exception as e:
            user = await self.bot.fetch_user(myID)
            await user.send("Exception in dm: ```" + str(e) + "```")

    @commands.command()
    async def purge(self, ctx, amt):
        try:
            if ctx.author.id == int(myID):
                await ctx.channel.purge(limit = int(amt) + 1)
                msg = await ctx.send(f"Purged {amt} messages.")
                await asyncio.sleep(3)
                await msg.delete()
        except Exception as e:
            user = await self.bot.fetch_user(myID)
            await user.send("Exception in purge: ```" + str(e) + "```")

async def setup(bot):
    await bot.add_cog(Util(bot))
