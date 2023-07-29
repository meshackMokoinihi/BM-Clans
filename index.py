import discord
from discord.ext import commands
from discord import app_commands
import asyncio

# Insert your Discord bot token here
TOKEN = 'MTExMzg4NDk4NjkxMTc3Mjc4Mg.G3Qrtw.2eFSdOgVadghOtNKLG3uy3aVFoaCi-JK4DSLSo'

# Insert the allowed user IDs who can use the commands

ALLOWED_USER_IDS = [875045400032211004, 962105910501703720, 769685095719632898]
ALLOWED = [1134830159652999218, 769685095719632898]
GENERAL_CHANNEL_ID = 1065179737254797354

# Enable the messages intent
# Initialize the bot with intents
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
@bot.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Check if the command is invoked in the general channel
def is_general_channel(ctx):
    return ctx.channel.id == GENERAL_CHANNEL_ID



@bot.tree.command(name="createclan")
@commands.check(is_general_channel)
async def CreateClan(interaction, *, clan_name: str):
    # Check if the user is allowed to use the command
    if interaction.user.id not in ALLOWED_USER_IDS:
        await interaction.response.send_message("You are not allowed to use this command.")
        return

    # Create a clan role with the given name
    clan_role = await interaction.guild.create_role(name=clan_name)

    # Create a text channel with the same name as the clan
    text_channel = await interaction.guild.create_text_channel(clan_name)
    # Set permissions for the clan role in the text channel
    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        clan_role: discord.PermissionOverwrite(read_messages=True)
    }
    await text_channel.edit(overwrites=overwrites)

    # Create a voice channel with the same name as the clan
    voice_channel = await interaction.guild.create_voice_channel(clan_name)
    # Set permissions for the clan role in the voice channel
    overwrites_voice = {
        interaction.guild.default_role: discord.PermissionOverwrite(connect=False),
        clan_role: discord.PermissionOverwrite(connect=True, read_messages=True)
    }
    await voice_channel.edit(overwrites=overwrites_voice)

    await interaction.response.send_message(f"Clan '{clan_name}' created successfully!")






@bot.tree.command(name="add")
@commands.check(is_general_channel)
async def Add(interaction, *, member: discord.Member, clan_name: str):
    # Check if the user is allowed to use the command
    if interaction.user.id not in ALLOWED:
        await interaction.response.send_message("You are not allowed to use this command.")
        return

    # Get the clan role based on the provided name
    clan_role = discord.utils.get(interaction.guild.roles, name=clan_name)
    if clan_role is None:
        await interaction.response.send_message(f"Clan '{clan_name}' not found.")
        return

    # Add the member to the clan role
    await member.add_roles(clan_role)
    await interaction.response.send_message(f"Member {member.display_name} added to '{clan_name}'!")



@bot.tree.command(name="remove")
@commands.check(is_general_channel)
async def Remove(interaction, *, member: discord.Member, clan_name: str):
    # Check if the user is allowed to use the command
    if interaction.user.id not in ALLOWED:
        await interaction.response.send_message("You are not allowed to use this command.")
        return

    # Get the clan role based on the provided name
    clan_role = discord.utils.get(interaction.guild.roles, name=clan_name)
    if clan_role is None:
        await interaction.response.send_message(f"Clan '{clan_name}' not found.")
        return

    # Remove the member from the clan role
    await member.remove_roles(clan_role)
    await interaction.response.send_message(f"Member {member.display_name} removed from '{clan_name}'!")

# Run the bot
bot.run(TOKEN)