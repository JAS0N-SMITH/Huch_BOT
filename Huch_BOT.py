import os
import discord
import random
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ".")
status = cycle(['with his catnip!', 'in the arena! MEOW!', 'in his dreams.', 'with his human!', 'with his toys.'])

#
# Startup Event/Status
#

@client.event
async def on_ready():
    #await client.change_presence(status=discord.Status.idle, activity=discord.Game('with his catnip!'))
    change_status.start()
    print("Bot is ready.")

#
# Tasks
#

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#
# Events
#

@client.event
async def on_member_join(member):
    print(f"{member} has joined a server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left a server")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')

#
# Commands
#

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command(aliases = ["8ball", "eightball", "eight_ball"])
async def _8ball(ctx, *, question):
    responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes - definitely.', 'You may rely on it.',
                 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
                 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.',
                 'Concentrate and ask again.', "Don't count on it.", 'My reply is no.', 'My sources say no.',
                 'Outlook not so good.', 'Very doubtful.']

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def pet(ctx):
    await ctx.send(f"Huch purrs with excitement!")

@client.command()
async def blowme(ctx):
    await ctx.send(f"Gagging!")

@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)

@clear.error #only triggered by clear command function
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return

#
#Cogs
#

@client.command()
async def load(ctx, extension):
    client.load_extension(f'Cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')



client.run("NTg3MjI5MTEzOTA3OTM3Mjgy.XPziLA.XyrOZJ0reSBOqQPS7McH9TUXQNc")




