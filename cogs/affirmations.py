import discord
from discord.ext import commands
import json
import os
import random
import asyncio

class Affirmations(commands.Cog):
    """Commands for affirmations and emotional support"""
    
    def __init__(self, bot):
        self.bot = bot
        self.affirmations_file = os.path.join("data", "affirmations.json")
    
    def load_affirmations(self):
        try:
            with open(self.affirmations_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"general": [], "comfort": []}
    
    @commands.command(name="affirmation")
    async def get_affirmation(self, ctx):
        """Get a positive affirmation"""
        affirmations = self.load_affirmations()
        
        if not affirmations.get("general"):
            await ctx.send("I don't have any affirmations yet. Please add some first!")
            return
        
        affirmation = random.choice(affirmations["general"])
        
        embed = discord.Embed(
            title="💖 Affirmation for You",
            description=affirmation,
            color=discord.Color.from_rgb(255, 105, 180)  # Pink color
        )
        embed.set_footer(text="Remember that you are loved! 🌈")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="comfort")
    async def comfort(self, ctx):
        """Get comforting words when you're feeling down"""
        affirmations = self.load_affirmations()
        
        if not affirmations.get("comfort"):
            await ctx.send("I don't have any comfort messages yet. Please add some first!")
            return
        
        comfort_msg = random.choice(affirmations["comfort"])
        
        embed = discord.Embed(
            title="🫂 Mom's Here For You",
            description=comfort_msg,
            color=discord.Color.from_rgb(186, 85, 211)  # Purple color
        )
        embed.set_footer(text="It's okay to not be okay sometimes. I'm here for you. 💜")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="vent")
    async def vent(self, ctx, *, topic=None):
        """Create a private thread to vent about something"""
        # Create a thread for venting
        topic_text = f" about {topic}" if topic else ""
        thread_name = f"{ctx.author.display_name}'s vent{topic_text}"
        
        try:
            thread = await ctx.channel.create_thread(
                name=thread_name,
                auto_archive_duration=1440,  # Archive after 24 hours
                type=discord.ChannelType.private_thread if ctx.guild.premium_tier >= 2 else discord.ChannelType.public_thread
            )
            
            # Add the user to the thread
            await thread.add_user(ctx.author)
            
            # Send initial message in thread
            embed = discord.Embed(
                title="Safe Space for Venting",
                description=(
                    f"Hi {ctx.author.mention}, this is your safe space to vent.\n\n"
                    "I'm here to listen. Take your time and share what's on your mind. "
                    "Remember that your feelings are valid, and it's okay to let them out."
                ),
                color=discord.Color.from_rgb(147, 112, 219)  # Medium purple
            )
            
            await thread.send(embed=embed)
            
            # Send follow-up comfort message after user vents
            def check(m):
                return m.author == ctx.author and m.channel == thread
            
            try:
                # Wait for the user to send a message in the thread
                await self.bot.wait_for('message', check=check, timeout=600.0)  # 10 minute timeout
                
                # Wait a moment before responding
                await asyncio.sleep(2)
                
                # Send a comforting response
                comfort_responses = [
                    "Thank you for sharing that with me. It takes courage to be vulnerable.",
                    "I hear you, and your feelings are completely valid.",
                    "I'm so proud of you for expressing yourself. That can be really hard sometimes.",
                    "You're not alone in feeling this way. I'm here for you.",
                    "Thank you for trusting me with your thoughts. Is there anything specific you need right now?",
                    "It sounds like you're going through a lot. Remember to be gentle with yourself."
                ]
                
                await thread.send(random.choice(comfort_responses))
                
            except asyncio.TimeoutError:
                # If user doesn't send anything within timeout period
                await thread.send("I'm still here if you need to talk. Take your time. 💜")
        
        except discord.Forbidden:
            await ctx.send("I don't have permission to create threads in this channel.")
        except discord.HTTPException:
            await ctx.send("I couldn't create a thread. Please try again later.")
    
    @commands.command(name="celebrate")
    async def celebrate(self, ctx, *, achievement):
        """Celebrate an achievement or milestone"""
        celebration_messages = [
            f"🎉 CONGRATULATIONS on {achievement}! I'm so incredibly proud of you!",
            f"🌟 That's amazing! {achievement} is such a wonderful accomplishment!",
            f"💖 My heart is bursting with pride! {achievement} is worth celebrating!",
            f"🎊 WOW! {achievement} is a huge deal! You should be so proud of yourself!",
            f"✨ Look at you go! {achievement} is proof of your hard work and dedication!"
        ]
        
        embed = discord.Embed(
            title="Time to Celebrate!",
            description=random.choice(celebration_messages),
            color=discord.Color.gold()
        )
        embed.set_footer(text="I'm always here to celebrate your wins, big and small! 💕")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Affirmations(bot))