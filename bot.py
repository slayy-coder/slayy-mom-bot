import os
import discord
from discord.ext import commands, tasks
import json
import random
import datetime
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX', '!')
AFFIRMATION_CHANNEL_ID = os.getenv('AFFIRMATION_CHANNEL_ID')

# Set up intents (permissions)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Data storage paths
DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "user_data.json")
RESOURCES_FILE = os.path.join(DATA_DIR, "resources.json")
AFFIRMATIONS_FILE = os.path.join(DATA_DIR, "affirmations.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize data files if they don't exist
def initialize_data_files():
    # User data structure
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({}, f)
    
    # Resources data
    if not os.path.exists(RESOURCES_FILE):
        default_resources = {
            "communities": [
                {"name": "r/trans", "url": "https://www.reddit.com/r/trans/", "description": "Transgender community on Reddit"},
                {"name": "r/lgbtindia", "url": "https://www.reddit.com/r/lgbtindia/", "description": "LGBTQ+ community in India"},
                {"name": "r/transmtf", "url": "https://www.reddit.com/r/MtF/", "description": "Community for trans women"}
            ],
            "youtube": [
                {"name": "Jammidodger", "url": "https://www.youtube.com/c/Jammidodger94", "description": "Trans educator and entertainer"},
                {"name": "Contrapoints", "url": "https://www.youtube.com/c/ContraPoints", "description": "Video essays on gender, politics, and philosophy"}
            ],
            "support": [
                {"name": "Trevor Project", "url": "https://www.thetrevorproject.org/", "description": "Crisis intervention and suicide prevention for LGBTQ+ youth"},
                {"name": "GLAAD", "url": "https://www.glaad.org/", "description": "Media advocacy organization for LGBTQ+ acceptance"}
            ]
        }
        with open(RESOURCES_FILE, 'w') as f:
            json.dump(default_resources, f, indent=4)
    
    # Affirmations data
    if not os.path.exists(AFFIRMATIONS_FILE):
        default_affirmations = {
            "general": [
                "You are loved exactly as you are.",
                "Your identity is valid and beautiful.",
                "I'm so proud of you for being your authentic self.",
                "You deserve all the happiness in the world.",
                "You are strong, brave, and resilient.",
                "Your journey is your own, and it's perfect.",
                "You are making a difference just by being you.",
                "I believe in you completely.",
                "You are enough, just as you are.",
                "Your feelings are valid and important."
            ],
            "comfort": [
                "I'm here for you, no matter what.",
                "It's okay to not be okay sometimes.",
                "This difficult time will pass, I promise.",
                "You're not alone in this struggle.",
                "Take all the time you need to heal.",
                "Your pain matters, and so do you.",
                "I'm sending you a big virtual hug right now.",
                "You've gotten through hard times before, and you'll get through this too.",
                "It's okay to ask for help when you need it.",
                "I love you unconditionally, through good times and bad."
            ]
        }
        with open(AFFIRMATIONS_FILE, 'w') as f:
            json.dump(default_affirmations, f, indent=4)

# User data functions
def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_user_profile(user_id):
    data = load_user_data()
    user_id = str(user_id)  # Convert to string for JSON compatibility
    
    if user_id not in data:
        # Create default profile
        data[user_id] = {
            "pronouns": None,
            "triggers": [],
            "birthdate": None,
            "milestones": {},
            "preferences": {
                "daily_affirmation": False
            }
        }
        save_user_data(data)
    
    return data[user_id]

# Load resources and affirmations
def load_resources():
    with open(RESOURCES_FILE, 'r') as f:
        return json.load(f)

def load_affirmations():
    with open(AFFIRMATIONS_FILE, 'r') as f:
        return json.load(f)

# Bot events
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    initialize_data_files()
    daily_affirmation.start()

@bot.event
async def on_message(message):
    # Don't respond to bot messages
    if message.author.bot:
        return
    
    # Process commands
    await bot.process_commands(message)
    
    # Check for trigger words in messages
    await check_triggers(message)

# Check for trigger words
async def check_triggers(message):
    content = message.content.lower()
    user_data = load_user_data()
    
    # Check all users' triggers
    for profile in user_data.items():
        if "triggers" in profile:
            for trigger in profile["triggers"]:
                if trigger.lower() in content:
                    # If message contains a trigger word, add a warning
                    await message.channel.send(f"⚠️ Content warning: This message may contain triggering content for some members.")
                    return

# Daily affirmation task
@tasks.loop(hours=24)
async def daily_affirmation():
    if AFFIRMATION_CHANNEL_ID:
        channel = bot.get_channel(int(AFFIRMATION_CHANNEL_ID))
        if channel:
            affirmations = load_affirmations()
            daily_msg = random.choice(affirmations["general"])
            
            embed = discord.Embed(
                title="💖 Daily Affirmation",
                description=daily_msg,
                color=discord.Color.from_rgb(255, 105, 180)  # Pink color
            )
            embed.set_footer(text="Slayy Mom loves you! 🌈")
            
            await channel.send(embed=embed)

@daily_affirmation.before_loop
async def before_daily_affirmation():
    await bot.wait_until_ready()
    
    # Wait until it's the right time (9:00 AM)
    now = datetime.datetime.now()
    target_time = datetime.datetime(now.year, now.month, now.day, 9, 0)
    
    if now > target_time:
        # If it's already past 9 AM, wait until tomorrow
        target_time = target_time + datetime.timedelta(days=1)
    
    await asyncio.sleep((target_time - now).total_seconds())

# Help command
@bot.command(name="help")
async def help_command(ctx, command=None):
    if command is None:
        # General help menu
        embed = discord.Embed(
            title="Slayy Mom Bot - Help Menu",
            description="I'm your supportive Discord mom! Here are my commands:",
            color=discord.Color.from_rgb(233, 30, 99)
        )
        
        embed.add_field(
            name="🔧 User Setup",
            value=f"`{PREFIX}pronouns` - Set your preferred pronouns\n"
                  f"`{PREFIX}trigger` - Add words to your trigger list\n"
                  f"`{PREFIX}birthday` - Set your birthday for celebrations",
            inline=False
        )
        
        embed.add_field(
            name="💖 Support & Affirmations",
            value=f"`{PREFIX}affirmation` - Get a positive affirmation\n"
                  f"`{PREFIX}comfort` - Receive comforting words\n"
                  f"`{PREFIX}vent` - Create a private thread to vent",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Safety & Resources",
            value=f"`{PREFIX}resources` - Get LGBTQIA+ resources\n"
                  f"`{PREFIX}tw <topic>` - Add a trigger warning\n"
                  f"`{PREFIX}forgetme` - Delete your stored data",
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ More Info",
            value=f"Type `{PREFIX}help <command>` for more details on a specific command.",
            inline=False
        )
        
        embed.set_footer(text="Slayy Mom loves you unconditionally! 🌈")
    else:
        # Specific command help
        command_info = {
            "pronouns": {
                "title": "Pronouns Command",
                "description": f"Set your preferred pronouns with `{PREFIX}pronouns <your pronouns>`.\n\nExamples:\n`{PREFIX}pronouns she/her`\n`{PREFIX}pronouns they/them`\n`{PREFIX}pronouns he/they`"
            },
            "trigger": {
                "title": "Trigger Command",
                "description": f"Add or remove trigger words with `{PREFIX}trigger add <word>` or `{PREFIX}trigger remove <word>`.\nView your triggers with `{PREFIX}trigger list`."
            },
            "birthday": {
                "title": "Birthday Command",
                "description": f"Set your birthday with `{PREFIX}birthday DD-MM-YYYY`.\nI'll remember and celebrate with you!"
            },
            "affirmation": {
                "title": "Affirmation Command",
                "description": f"Get a positive affirmation with `{PREFIX}affirmation`."
            },
            "comfort": {
                "title": "Comfort Command",
                "description": f"Receive comforting words with `{PREFIX}comfort`."
            },
            "vent": {
                "title": "Vent Command",
                "description": f"Create a private thread to vent with `{PREFIX}vent`.\nI'll be there to listen and support you."
            },
            "resources": {
                "title": "Resources Command",
                "description": f"Get LGBTQIA+ resources with `{PREFIX}resources`.\nYou can also specify a category: `{PREFIX}resources communities`, `{PREFIX}resources youtube`, or `{PREFIX}resources support`."
            },
            "tw": {
                "title": "Trigger Warning Command",
                "description": f"Add a trigger warning to your message with `{PREFIX}tw <topic> <your message>`.\nThis will put your message in a spoiler with a warning."
            },
            "forgetme": {
                "title": "Forget Me Command",
                "description": f"Delete all your stored data with `{PREFIX}forgetme`.\nThis action cannot be undone."
            }
        }
        
        if command.lower() in command_info:
            info = command_info[command.lower()]
            embed = discord.Embed(
                title=info["title"],
                description=info["description"],
                color=discord.Color.from_rgb(233, 30, 99)
            )
        else:
            embed = discord.Embed(
                title="Command Not Found",
                description=f"I couldn't find information for `{command}`.\nUse `{PREFIX}help` to see all available commands.",
                color=discord.Color.red()
            )
    
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("Error: No Discord token found. Please set the DISCORD_TOKEN in your .env file.")
    else:
        bot.run(TOKEN)