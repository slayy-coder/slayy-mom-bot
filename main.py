import asyncio
import os
from bot import bot, initialize_data_files

async def main():
    # Initialize data files
    initialize_data_files()
    
    # Load all cogs
    cogs_dir = "cogs"
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"{cogs_dir}.{filename[:-3]}")
                print(f"Loaded extension: {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")
    
    # Run the bot
    async with bot:
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    # Create cogs directory if it doesn't exist
    os.makedirs("cogs", exist_ok=True)
    
    # Run the bot
    asyncio.run(main())