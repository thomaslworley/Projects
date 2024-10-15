import discord
from discord.ext import commands
import api

intents= discord.Intents.default()

client = commands.Bot(intents=intents, command_prefix= '/')

@client.event
async def on_ready():
    print('Up and running')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Visual Studio Code"))

global auth_check
auth_check = False

@client.event
async def on_message(message):
    global auth_check
    await client.process_commands(message)
    if message.content.startswith('/report') or message.content.startswith('/apply'):
        await message.delete()
        return str(message.author)

    if message.content.startswith('/clear_channel'):
        if message.author.id == 379457469602070530:
            auth_check = True

    channel_list = [721636855912857652, 
                    721616905164816414, 
                    721972959501090846, 
                    721972984767840296, 
                    722200998055116853, 
                    724804033029865532, 
                    722193319890911302, 
                    701178536685207643, 
                    692613575205715968,
                    709477868794544141,
                    732623018836361387,
                    714664518730514434] 

    if message.channel.id not in channel_list:
        channel = client.get_channel(721972959501090846)
        
        if len(message.content) == 0 or message.content.startswith('https://'):
            await channel.send('```A File was sent by ' + str(message.author) + '```')
        else:
            await channel.send('```{' + message.content + '} Sent by: ' + str(message.author) + '```')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(721972959501090846)
    await channel.send(str(member) + 'is no longer in this server.')

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 721618100822343762 or 721622811948482591:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

    if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
            await member.add_roles(role)
            print(member.name + ' has been added the role ' + role.name)
        else:
            print('Something went wrong with getting a member.')
    else:
        print('Something went wrong with getting a role.')


@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 721618100822343762 or 721622811948482591:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

    if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
            await member.remove_roles(role)
            print(member.name + ' has removed the role ' + role.name)
        else:
            print('Something went wrong with getting a member.')
    else:
        print('Something went wrong with getting a role.')


@client.command()
async def apply(ctx,  *, message):
    user = client.get_channel(724804033029865532)
    await user.send(f'{ctx.message.author} has applied for Moderator.\n{message}')

@client.command()
async def report(ctx, Topic, *, message):
    user = client.get_user(379457469602070530)
    await user.send(f'Topic: {Topic} \nComplaint: {message} \nUser: {ctx.message.author}')

global strike_list
strike_list = []

@client.command()
async def strike(ctx, user, *, reason):
    global strike_list

    guild = discord.utils.find(lambda g : g.id == 709477868794544138,client.guilds)
    member = discord.utils.find(lambda m : m.id == int(user), guild.members)
    strike1 = discord.utils.get(guild.roles, name='Strike 1')
    strike2 = discord.utils.get(guild.roles, name='Strike 2')
    strike3 = discord.utils.get(guild.roles, name='Strike 3')

    send = client.get_channel(732623018836361387)
    await send.send(f'```{member} Has been struck for: \n{reason} \nBy {ctx.message.author}.```')

    if user not in strike_list:
        strike_list.append(user)
        await member.add_roles(strike1)
    else:
        if strike2 not in member.roles:
            await member.remove_roles(strike1)
            await member.add_roles(strike2)
        else:
            await member.remove_roles(strike2)
            await member.add_roles(strike3)

    print(guild, member)

@client.command()
async def get_list(ctx):
    print(strike_list)

@client.command()
async def clear_channel(ctx, amount):
    if ctx.author.id == 379457469602070530:
        await ctx.channel.purge(limit=int(amount))
    else:
        print('Authorization failed')


client.run(api.key)