############################ Made By Foxytouxxx ############################
# Do not copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this script

import discord
from discord.ext import commands
import subprocess
import time
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='+', intents=intents)

start_time = time.time()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await update_status()

@bot.command(name='exe')
async def execute_command(ctx, *, command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout

        # Check the length of the output
        if len(output) <= 1950:
            await ctx.send(f'Command executed successfully:\n```\n{output}\n```')
        else:
            # Split the output into chunks of 1950 characters
            for i in range(0, len(output), 1950):
                await ctx.send(f'Command executed successfully (Part {i//1950 + 1}):\n```\n{output[i:i+1950]}\n```')

    except Exception as e:
        await ctx.send(f'Error executing command: {str(e)}')

async def update_status():
    while True:
        # Calculate the uptime in seconds
        uptime_seconds = int(time.time() - start_time)
        # Makes it a bit more readable
        uptime_formatted = time.strftime('%H:%M:%S', time.gmtime(uptime_seconds))
      
        await bot.change_presence(activity=discord.Game(name=f'Uptime: {uptime_formatted}'))
      
        # Update your status every 60 seconds
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(update_status())
    await bot.start('YOUR BOT TOKEN HERE')

if __name__ == "__main__":
    asyncio.run(main())
