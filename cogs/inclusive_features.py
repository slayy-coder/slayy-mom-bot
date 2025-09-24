import discord
from discord.ext import commands
import json
import os
import datetime

class InclusiveFeatures(commands.Cog):
    """Commands for inclusive features and safety tools"""
    
    def __init__(self, bot):
        self.bot = bot
        self.resources_file = os.path.join("data", "resources.json")
    
    def load_resources(self):
        try:
            with open(self.resources_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    @commands.command(name="resources")
    async def resources(self, ctx, category=None):
        """Get LGBTQIA+ resources"""
        resources = self.load_resources()
        
        if not resources:
            await ctx.send("I don't have any resources available yet.")
            return
        
        if category and category.lower() in resources:
            # Show specific category
            category_name = category.lower()
            category_resources = resources[category_name]
            
            embed = discord.Embed(
                title=f"LGBTQIA+ {category_name.capitalize()} Resources",
                description=f"Here are some helpful {category_name} resources:",
                color=discord.Color.from_rgb(255, 20, 147)  # Deep pink
            )
            
            for resource in category_resources:
                embed.add_field(
                    name=resource["name"],
                    value=f"[{resource['description']}]({resource['url']})",
                    inline=False
                )
        else:
            # Show all categories
            embed = discord.Embed(
                title="LGBTQIA+ Resources",
                description="Here are resources that might help you:",
                color=discord.Color.from_rgb(255, 20, 147)  # Deep pink
            )
            
            for category_name, category_resources in resources.items():
                resource_list = "\n".join([f"• [{r['name']}]({r['url']})" for r in category_resources[:3]])
                if len(category_resources) > 3:
                    resource_list += f"\n• *...and {len(category_resources) - 3} more*"
                
                embed.add_field(
                    name=f"{category_name.capitalize()}",
                    value=f"{resource_list}\n\nUse `!resources {category_name}` for more details.",
                    inline=False
                )
        
        embed.set_footer(text="Remember that you're not alone. There's a whole community here for you! 🌈")
        await ctx.send(embed=embed)
    
    @commands.command(name="tw", aliases=["trigger_warning"])
    async def trigger_warning(self, ctx, topic, *, message=None):
        """Add a trigger warning to your message"""
        # Delete the original command
        await ctx.message.delete()
        
        if not message:
            await ctx.send("Please provide both a topic and a message. Usage: `!tw topic Your message here`")
            return
        
        embed = discord.Embed(
            title=f"⚠️ Trigger Warning: {topic}",
            description="The following message may contain content that could be triggering.",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="Message Content (click to reveal)",
            value=f"||{message}||"
        )
        embed.set_footer(text=f"Posted by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn_user(self, ctx, member: discord.Member, *, reason=None):
        """Warn a user for inappropriate behavior (Requires Manage Messages permission)"""
        reason = reason or "No reason provided"
        
        # DM the user
        try:
            embed = discord.Embed(
                title="Warning",
                description=f"You have received a warning in {ctx.guild.name}",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason)
            embed.add_field(name="Warned by", value=ctx.author.display_name)
            embed.set_footer(text="Please review the server rules. Repeated warnings may result in further action.")
            
            await member.send(embed=embed)
            
            # Confirmation in channel
            await ctx.send(f"✅ {member.mention} has been warned. Reason: {reason}")
            
        except discord.Forbidden:
            await ctx.send(f"⚠️ Could not DM {member.mention}, but the warning has been recorded. Reason: {reason}")
    
    @warn_user.error
    async def warn_user_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to warn users.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("I couldn't find that member.")
        else:
            await ctx.send(f"An error occurred: {error}")
    
    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute_user(self, ctx, member: discord.Member, duration: int, *, reason=None):
        """Timeout a user for a specified duration in minutes (Requires Moderate Members permission)"""
        reason = reason or "No reason provided"
        
        try:
            # Convert minutes to seconds for the timeout duration
            duration_seconds = duration * 60
            await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=duration_seconds), reason=reason)
            
            embed = discord.Embed(
                title="User Timed Out",
                description=f"{member.mention} has been timed out for {duration} minutes.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason)
            
            await ctx.send(embed=embed)
            
            # DM the user
            try:
                await member.send(f"You have been timed out in {ctx.guild.name} for {duration} minutes. Reason: {reason}")
            except discord.Forbidden:
                pass  # Can't DM the user
                
        except discord.Forbidden:
            await ctx.send("I don't have permission to timeout that user.")
        except discord.HTTPException:
            await ctx.send("Failed to timeout the user. Please try again.")
    
    @mute_user.error
    async def mute_user_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to timeout users.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("I couldn't find that member.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid duration in minutes.")
        else:
            await ctx.send(f"An error occurred: {error}")
    
    @commands.command(name="pride")
    async def pride_message(self, ctx, flag=None):
        """Send a pride-themed message with optional flag type"""
        pride_flags = {
            "rainbow": {
                "colors": [0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x0000FF, 0x4B0082, 0x9400D3],
                "message": "Pride is about celebrating the beautiful diversity of the LGBTQIA+ community!"
            },
            "trans": {
                "colors": [0x55CDFC, 0xF7A8B8, 0xFFFFFF, 0xF7A8B8, 0x55CDFC],
                "message": "Trans rights are human rights! You are valid, seen, and loved."
            },
            "bi": {
                "colors": [0xD60270, 0x9B4F96, 0x0038A8],
                "message": "Bi visibility matters! Your identity is valid regardless of your relationship."
            },
            "pan": {
                "colors": [0xFF1B8D, 0xFFDA00, 0x1BB3FF],
                "message": "Pan pride! Love knows no gender boundaries."
            },
            "ace": {
                "colors": [0x000000, 0xA4A4A4, 0xFFFFFF, 0x810081],
                "message": "Ace pride! Your identity is valid and important."
            },
            "nb": {
                "colors": [0xFFF430, 0xFFFFFF, 0x9C59D1, 0x000000],
                "message": "Non-binary pride! Gender is a spectrum, and you are valid wherever you are on it."
            }
        }
        
        if flag and flag.lower() in pride_flags:
            selected = pride_flags[flag.lower()]
            color = selected["colors"][0]  # Use first color for embed
            message = selected["message"]
        else:
            # Default to rainbow
            selected = pride_flags["rainbow"]
            color = selected["colors"][0]
            message = selected["message"]
            
            if flag:
                await ctx.send(f"I don't have that flag yet, so I'll use the rainbow flag instead! Available flags: {', '.join(pride_flags.keys())}")
        
        embed = discord.Embed(
            title="🌈 Pride and Love! 🌈",
            description=message,
            color=color
        )
        
        flag_name = flag.lower() if flag and flag.lower() in pride_flags else "rainbow"
        embed.set_footer(text=f"Showing {flag_name} pride flag colors. Remember: You are loved exactly as you are! 💖")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(InclusiveFeatures(bot))