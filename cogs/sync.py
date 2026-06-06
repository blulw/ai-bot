from typing import Literal, Optional
from main import bot, myID
import discord
from discord.ext import commands
from discord import app_commands

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")
    
    @bot.tree.command(name="sync")
    async def ssync(self, interaction: discord.Interaction):
        try:
            await interaction.send("test")
        except Exception as e:
            user = await self.bot.fetch_user(myID)
            await user.send("Exception in sync: ```" + str(e) + "```")

    @commands.command()
    @commands.guild_only()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        try:
            if str(ctx.author.id) == myID:
                if not guilds:
                    if spec == "~":
                        synced = await ctx.bot.tree.sync(guild=ctx.guild)
                    elif spec == "*":
                        ctx.bot.tree.copy_global_to(guild=ctx.guild)
                        synced = await ctx.bot.tree.sync(guild=ctx.guild)
                    elif spec == "^":
                        ctx.bot.tree.clear_commands(guild=ctx.guild)
                        await ctx.bot.tree.sync(guild=ctx.guild)
                        synced = []
                    else:
                        synced = await ctx.bot.tree.sync()

                    await ctx.send(
                        f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
                    )
                    return

                ret = 0
                for guild in guilds:
                    try:
                        await ctx.bot.tree.sync(guild=guild)
                    except discord.HTTPException:
                        pass
                    else:
                        ret += 1

                await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
            else: 
                await ctx.send("only bran can do that")
        except Exception as e:
            user = await self.bot.fetch_user(myID)
            await user.send("Exception in sync: ```" + str(e) + "```")
        
async def setup(bot):
    await bot.add_cog(Sync(bot))
