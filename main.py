import os
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
from kabot.minecraft_status import MinecraftMonitor
from keep_alive import keep_alive

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!ka ', intents=intents)

mc_monitor = MinecraftMonitor(bot)

@bot.event
async def on_ready():
    print(f"🤖 KaBot conectado como {bot.user}")
    mc_monitor.start_monitoring.start()

@bot.command(name="status")
async def status_cmd(ctx):
    await mc_monitor.send_status(ctx.channel)

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))
