import os
import random
import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MANAGEMENT = os.getenv('DISCORD_MANAGEMENT_CHANNEL')
INTRODUCTIONS = os.getenv('DISCORD_INTRODUCTION_CHANNEL')
ROLES = os.getenv('DISCORD_ROLES_CHANNEL')
BASEROLE = os.getenv('DISCORD_GUILD_BASE_ROLE')
client = discord.Client()


# checks to make sure nickname is in format "name (ign)"
def checkNickFormat(name):
    nick = name.split()
    # checks to see if nickname is multiple words
    if len(nick) > 1:
        nicklast = nick[-1]
        #checks to see if the ign is in the correct format
        if (nicklast.startswith('(') and nicklast.endswith(')')):
            return True
    return False

# Can add in future if needed
# Base template
# def checkMessageContent(contents):
#    if 'cwru' or 'case' in contents:
#        return True
#    return False

# Creates a dm based on what the user is missing
def generateErrorMessage(error):
    msg = 'Hey! Thanks for joining the server. You are getting this message because the introduction you posted is not in the correct format. '
    if 'nick' in error:
        msg = msg + 'Your nickname is not in the correct format. Please format it as: ' + '"' + "Name (ign)" + '"' + '. '
    # if 'cwru' in error:

    msg = msg + 'Your previous message has been deleted. Below are the contents of your previous message. If you are not a cwru student, please tag @exec in your message and explain your situation'
    return msg

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    manageChannel = discord.utils.get(client.get_all_channels(), name=MANAGEMENT)
    await manageChannel.send(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # If message is not in introductions, ignore it
    if str(message.channel) == INTRODUCTIONS:
        error = []
        nick = message.author.display_name
        contents = message.content

        # Generate a list of error's with the name/intro
        if not checkNickFormat(nick):
            error.append('nick')
        # if not checkMessageContent(contents):
        #    error.append('cwru')

        if len(error):
            # Prob not the correct way to do it but it works
            if "exec" not in str(message.role_mentions):
                dm = generateErrorMessage(error)
                await message.delete()
                await message.author.send(dm)
                await message.author.send(contents)
        else:
            cwruRole = discord.utils.get(message.guild.roles, name=BASEROLE)
            await message.author.add_roles(cwruRole)
            rolesChannel = discord.utils.get(client.get_all_channels(), name=ROLES)
            reply = message.author.mention + 'Welcome to the server! You have access now. Head over to ' + rolesChannel.mention + 'for access to game specific roles'
            await message.channel.send(reply)

client.run(TOKEN)