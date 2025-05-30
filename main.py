import discord
from discord.ext import commands
import subprocess
import time
import asyncio
import os  # To read environment variables

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='+', intents=intents)

start_time = time.time()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    asyncio.create_task(update_status())

@bot.command(name='exe')
async def execute_command(ctx, *, command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout

        if len(output) <= 1950:
            await ctx.send(f'Command executed successfully:\n```\n{output}\n```')
        else:
            for i in range(0, len(output), 1950):
                await ctx.send(f'Command executed successfully (Part {i//1950 + 1}):\n```\n{output[i:i+1950]}\n```')

    except Exception as e:
        await ctx.send(f'Error executing command: {str(e)}')

async def update_status():
    while True:
        uptime_seconds = int(time.time() - start_time)
        uptime_formatted = time.strftime('%H:%M:%S', time.gmtime(uptime_seconds))
        await bot.change_presence(activity=discord.Game(name=f'Uptime: {uptime_formatted}'))
        await asyncio.sleep(60)

async def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("ERROR: DISCORD_TOKEN environment variable not set.")
        return
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
    
