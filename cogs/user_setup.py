import discord
from discord.ext import commands
import json
import os
import datetime

class UserSetup(commands.Cog):
    """Commands for user profile setup and customization"""
    
    def __init__(self, bot):
        self.bot = bot
        self.user_data_file = os.path.join("data", "user_data.json")
    
    def load_user_data(self):
        try:
            with open(self.user_data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_user_data(self, data):
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def get_user_profile(self, user_id):
        data = self.load_user_data()
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
            self.save_user_data(data)
        
        return data[user_id]
    
    @commands.command(name="pronouns")
    async def set_pronouns(self, ctx, *, pronouns=None):
        """Set your preferred pronouns"""
        if pronouns is None:
            # Display current pronouns
            user_profile = self.get_user_profile(ctx.author.id)
            current_pronouns = user_profile.get("pronouns", "not set")
            
            embed = discord.Embed(
                title="Your Pronouns",
                description=f"Your current pronouns are: **{current_pronouns}**",
                color=discord.Color.from_rgb(255, 105, 180)
            )
            embed.add_field(
                name="How to Update",
                value=f"To update your pronouns, use `!pronouns your/pronouns`\nExamples: `!pronouns she/her`, `!pronouns they/them`, `!pronouns he/him/his`"
            )
            await ctx.send(embed=embed)
            return
        
        # Update pronouns
        user_data = self.load_user_data()
        user_id = str(ctx.author.id)
        
        if user_id not in user_data:
            user_data[user_id] = {}
        
        user_data[user_id]["pronouns"] = pronouns
        self.save_user_data(user_data)
        
        embed = discord.Embed(
            title="Pronouns Updated",
            description=f"I've updated your pronouns to: **{pronouns}**",
            color=discord.Color.green()
        )
        embed.set_footer(text="Thank you for sharing this with me! 💖")
        await ctx.send(embed=embed)
    
    @commands.group(name="trigger", invoke_without_command=True)
    async def trigger(self, ctx):
        """Manage your trigger words"""
        await ctx.send(f"Please use one of the subcommands: `{ctx.prefix}trigger add`, `{ctx.prefix}trigger remove`, or `{ctx.prefix}trigger list`")
    
    @trigger.command(name="add")
    async def trigger_add(self, ctx, *, word):
        """Add a word to your trigger list"""
        user_data = self.load_user_data()
        user_id = str(ctx.author.id)
        
        if user_id not in user_data:
            user_data[user_id] = {"triggers": []}
        elif "triggers" not in user_data[user_id]:
            user_data[user_id]["triggers"] = []
        
        # Check if trigger is already in the list
        if word.lower() in [t.lower() for t in user_data[user_id]["triggers"]]:
            await ctx.send(f"'{word}' is already in your trigger list.")
            return
        
        user_data[user_id]["triggers"].append(word)
        self.save_user_data(user_data)
        
        # Send confirmation as DM for privacy
        try:
            embed = discord.Embed(
                title="Trigger Word Added",
                description=f"I've added '{word}' to your trigger list. I'll help warn about content containing this.",
                color=discord.Color.green()
            )
            embed.set_footer(text="Your privacy is important to me. This list is private.")
            await ctx.author.send(embed=embed)
            
            if ctx.guild:  # If command was used in a server
                await ctx.send("I've sent you a DM with the confirmation.")
        except discord.Forbidden:
            # If DM couldn't be sent
            await ctx.send("Trigger word added. (Note: I tried to DM you but couldn't. Please enable DMs for privacy.)")
    
    @trigger.command(name="remove")
    async def trigger_remove(self, ctx, *, word):
        """Remove a word from your trigger list"""
        user_data = self.load_user_data()
        user_id = str(ctx.author.id)
        
        if user_id not in user_data or "triggers" not in user_data[user_id]:
            await ctx.send("You don't have any trigger words set.")
            return
        
        # Case-insensitive removal
        triggers = user_data[user_id]["triggers"]
        for trigger in triggers:
            if trigger.lower() == word.lower():
                user_data[user_id]["triggers"].remove(trigger)
                self.save_user_data(user_data)
                
                try:
                    await ctx.author.send(f"I've removed '{trigger}' from your trigger list.")
                    if ctx.guild:
                        await ctx.send("I've sent you a DM with the confirmation.")
                except discord.Forbidden:
                    await ctx.send(f"Removed '{trigger}' from your trigger list.")
                return
        
        await ctx.send(f"'{word}' was not found in your trigger list.")
    
    @trigger.command(name="list")
    async def trigger_list(self, ctx):
        """List your trigger words"""
        user_data = self.load_user_data()
        user_id = str(ctx.author.id)
        
        if user_id not in user_data or "triggers" not in user_data[user_id] or not user_data[user_id]["triggers"]:
            await ctx.send("You don't have any trigger words set.")
            return
        
        triggers = user_data[user_id]["triggers"]
        
        # Send as DM for privacy
        try:
            embed = discord.Embed(
                title="Your Trigger Words",
                description="Here are the words on your trigger list:",
                color=discord.Color.blue()
            )
            
            # Format the list of triggers
            trigger_text = "\n".join([f"• {trigger}" for trigger in triggers])
            embed.add_field(name="Words", value=trigger_text)
            embed.set_footer(text="Your privacy is important to me. This list is private.")
            
            await ctx.author.send(embed=embed)
            
            if ctx.guild:  # If command was used in a server
                await ctx.send("I've sent you a DM with your trigger list.")
        except discord.Forbidden:
            # If DM couldn't be sent, send a more discreet message
            await ctx.send("I couldn't send you a DM. Please enable DMs for privacy with sensitive information.")
    
    @commands.command(name="birthday")
    async def set_birthday(self, ctx, date_str=None):
        """Set your birthday for celebrations (format: DD-MM-YYYY)"""
        if date_str is None:
            # Display current birthday
            user_profile = self.get_user_profile(ctx.author.id)
            current_bday = user_profile.get("birthdate", "not set")
            
            embed = discord.Embed(
                title="Your Birthday",
                description=f"Your birthday is currently: **{current_bday}**",
                color=discord.Color.from_rgb(255, 105, 180)
            )
            embed.add_field(
                name="How to Update",
                value=f"To update your birthday, use `!birthday DD-MM-YYYY`\nExample: `!birthday 15-06-1995`"
            )
            await ctx.send(embed=embed)
            return
        
        # Validate date format
        try:
            day, month, year = map(int, date_str.split('-'))
            birthday = datetime.date(year, month, day)
            formatted_date = birthday.strftime("%d-%m-%Y")
        except (ValueError, TypeError):
            await ctx.send("Invalid date format. Please use DD-MM-YYYY (e.g., 15-06-1995).")
            return
        
        # Update birthday
        user_data = self.load_user_data()
        user_id = str(ctx.author.id)
        
        if user_id not in user_data:
            user_data[user_id] = {}
        
        user_data[user_id]["birthdate"] = formatted_date
        self.save_user_data(user_data)
        
        embed = discord.Embed(
            title="Birthday Updated",
            description=f"I've updated your birthday to: **{formatted_date}**",
            color=discord.Color.green()
        )
        embed.set_footer(text="I'll remember to celebrate with you! 🎂")
        await ctx.send(embed=embed)
    
    @commands.command(name="milestone")
    async def add_milestone(self, ctx, date_str, *, description):
        """Add a personal milestone to celebrate (format: DD-MM-YYYY)"""
        # Validate date format
        try:
            day, month, year = map(int, date_str.split('-'))
            milestone_date = datetime.date(year, month, day)
            formatted_date = milestone_date.strftime("%d-%m-%Y")
        except (ValueError, TypeError):
            await ctx.send("Invalid date format. Please use DD-MM-YYYY (e.g., 15-06-2022).")
            return
        
        # Update milestones
        user_data = self.load_user_data()
        user_id = str(ctx.author.id)
        
        if user_id not in user_data:
            user_data[user_id] = {"milestones": {}}
        elif "milestones" not in user_data[user_id]:
            user_data[user_id]["milestones"] = {}
        
        user_data[user_id]["milestones"][formatted_date] = description
        self.save_user_data(user_data)
        
        embed = discord.Embed(
            title="Milestone Added",
            description=f"I've added your milestone: **{description}** on **{formatted_date}**",
            color=discord.Color.green()
        )
        embed.set_footer(text="I'll remember to celebrate this special day with you! 🎉")
        await ctx.send(embed=embed)
    
    @commands.command(name="forgetme")
    async def forget_me(self, ctx):
        """Delete all your stored data"""
        # Ask for confirmation
        embed = discord.Embed(
            title="⚠️ Delete Your Data?",
            description="Are you sure you want to delete all your stored data? This cannot be undone.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Confirmation",
            value="Reply with 'yes' to confirm or 'no' to cancel."
        )
                
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['yes', 'no']
        
        try:
            response = await self.bot.wait_for('message', check=check, timeout=30.0)
            
            if response.content.lower() == 'yes':
                user_data = self.load_user_data()
                user_id = str(ctx.author.id)
                
                if user_id in user_data:
                    del user_data[user_id]
                    self.save_user_data(user_data)
                    
                    embed = discord.Embed(
                        title="Data Deleted",
                        description="All your data has been deleted from my records.",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("You don't have any stored data.")
            else:
                await ctx.send("Operation cancelled. Your data remains unchanged.")
                
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out. Your data remains unchanged.")

async def setup(bot):
    await bot.add_cog(UserSetup(bot))