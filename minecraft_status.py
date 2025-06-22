import os
import discord
from discord.ext import tasks
from mcstatus import JavaServer

class MinecraftMonitor:
    def __init__(self, bot):
        self.bot = bot
        self.server_address = os.getenv("MC_SERVER")
        self.port = int(os.getenv("MC_PORT", 25565))
        self.channel_id = int(os.getenv("MC_CHANNEL_ID"))
        self.mention_ids = os.getenv("MC_MENTION_IDS", "").split()
        self.last_online = False

    async def send_status(self, channel):
        try:
            server = JavaServer.lookup(f"{self.server_address}:{self.port}")
            status = server.status()
            embed = discord.Embed(title="🟢 Servidor Online", color=0x00ff00)
            embed.add_field(name="Players Online", value=f"{status.players.online}/{status.players.max}")
            embed.add_field(name="Versão", value=status.version.name, inline=False)
            await channel.send(embed=embed)
        except Exception:
            await channel.send(embed=discord.Embed(title="🔴 Servidor Offline", color=0xff0000))

    @tasks.loop(seconds=60)
    async def start_monitoring(self):
        try:
            server = JavaServer.lookup(f"{self.server_address}:{self.port}")
            server.status()
            if not self.last_online:
                self.last_online = True
                channel = self.bot.get_channel(self.channel_id)
                mentions = " ".join(self.mention_ids)
                await channel.send(f"🟢 O servidor Minecraft está ONLINE!
{mentions}")
        except:
            self.last_online = False
