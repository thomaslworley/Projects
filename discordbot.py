"""Discord module allows to connect to Discord Python API to run and code the bot's functions
   And api module holds the API key for the bot without leaving it in the code"""
import discord
from discord.ext import commands
import api


def main():
    """Main function just to run the bot and the events it will handle and commands to execute"""
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix='!', intents=intents)

    log_channel = 1296240616685961237

    @client.event
    async def on_ready():
        print('The bot is running!')
        online = discord.Status.online
        custom = discord.CustomActivity
        channel = client.get_channel(log_channel)
        await client.change_presence(status=online, activity=custom(name='Currently being Wacky!'))
        await channel.send('Bot is running!')

    @client.command()
    async def commandhelp(ctx):
        names = [command.name for command in client.commands]
        clean = '\n '.join(names)
        await ctx.send(f'```Below is a list of commands:\n {clean}```')


    client.run(api.Key)







if __name__=='__main__':
    main()
