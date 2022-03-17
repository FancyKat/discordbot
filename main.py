from typing import TextIO
import discord
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
from discord import Webhook, RequestsWebhookAdapter, \
    Embed  # Importing discord.Webhook and discord.RequestsWebhookAdapter as well as Embed class
import aiohttp  # We need aiohttp for async usage.
import pandas_datareader as web
import datetime as dt
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')


def get_stock_price(ticker):
    data = web.DataReader(ticker, "yahoo")
    return data['Close'].iloc[-1]


class ResponseBot:
    # "INFORMATION"
    def __init__(self, message):
        message = "hello"

    def say_hello(self):
        return self.name


@bot.event
def on_connect():
    print(ResponseBot.say_hello)


# Checks time that bot was started
botStartTime = dt.datetime.now()

# Prefix to be entered before commands. Ex. !test
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

# Creates a log file if it doesn't exist and then writes to the log file, whether it just created it,
# what time the bot was started.
f = open('../FancyBotLogs.txt', 'a')
f.write('\nFancyBot ready! | ')
f.write(str(dt.datetime.now()))
f.write('\n')
f.close()


# Handles what needs to be printed in the console
def console_output(command_name, command_time):  # Defines consoleOutput()
    start_time = command_time  # (laziness) passing startTime from the beginning of the command into the function
    run_time = dt.datetime.now() - start_time
    print('')
    print('---------FancyBot----------')  # Divider to make console readable
    print('Time to Run:', run_time)  # Prints how long it took the bot to run the command
    print('Current Time:',
          dt.datetime.now())  # Prints time command was run in the console, from the variable 'currentDT'
    print(command_name, 'has been run')  # Prints 'test has been run' in console
    print('--------------------------')  # Divider to make console readable

    # Write to log
    f: TextIO = open('../FancyBotLogs.txt', 'a')
    f.write('\n---------FancyBot----------\n')
    f.write('Time to Run: ')
    f.write(str(run_time))
    f.write('\nCurrent Time: ')
    f.write(str(dt.datetime.now()))
    f.write('\n')
    f.write(
        str(command_name))  # commandName should always be a string, this is just to limit any possible errors in the future.
    f.write(' has been run\n')
    f.write('--------------------------\n')
    f.close()


@bot.command(pass_context=True)
async def test(ctx):  # Defines the command 'test' so to run this command you type '!test'
    start_time = dt.datetime.now()  # Stores the time the command was initiated at
    await ctx.send('Working!')  # Types 'Working!' in discord channel where command was run
    console_output('test', start_time)


async def on_message(self):
    # Looking For Group
    if self.content.startswith('$LFG'):
        player_info = self.content.split(" ")
        print(player_info)
        channel = bot.fetch_channel(946833421777383444)
        print(channel)
        if "tank" in player_info:
            await channel.send(str(player_info[1]) + " Tank")
    # Test Code for Tank
    if self.content.startswith('$Tank'):
        await self.channel.send(self.author.name + " Tank")

    # Response Test
    if self.content == 'This is SO HARD':
        await self.channel.send("I believe in you!!!")

    # Response Test
    if self.content == 'You are a sweet robot':
        await self.channel.send("I love you even if you are my overlord <3")

    # Response Test
    if self.content == 'Tell the people what you can say':
        await self.channel.send(
            "Try to talk to me so I can try out function My commands are $hello, $Tank, This is SO "
            "HARD, You are a sweet robot Case Sensitive")

    # Stock Checker with Pandas
    if self.content.startswith('$stockprice'):
        if len(self.content.split(" ")) == 2:
            ticker = self.content.split(" ")[1]
            data = get_stock_price(ticker)
            await self.channel.send(f"Stock Price of {ticker} is {data}!")

    # Private Response Check
    if self.content.startswith("$private"):
        await self.author.send("Function Working Smoothly")

    # Help Checker
    if self.content.startswith('$FancyHelp') and self.author.name == "FancyKat":
        'Building a list of Options'
        options = ["$MENU_1", "$MENU_2", "$MENU_3"]
        i = 0
        while i < len(options):
            print(i)
            await self.author.send(options[i])
            i += 1
        await self.channel.send("Let Me Check this out!")

    if self.content.startswith("$binarytree"):
        await self.channel.send("TIME TO SEND BINARIES")


@bot.event
async def on_message(message):
    # Pulling history of Channel
    if message.content.startswith('LFG'):
        print(message)
        messages = await message.channel.history(limit=10).flatten()
        print(messages)
        population = [message.content.split(" ") for message in messages]
        print(f"Population: {population}")

        # Logic For Grouping
        i = 2
        group = []
        string_joining = " "
        roles = ["DPS", "DPS", "DPS", "TANK", "HEALER"]
        for player in population:
            if "HEALER" in player and "HEALER" in roles:
                print(f"Player Information: {player}")
                roles.remove("HEALER")
                current_player = [player[1], player[3]]
                group.insert(4, current_player)
                print(group)
                continue

            elif "TANK" in player and "TANK" in roles:
                print(f"Player Information: {player}")
                roles.remove("TANK")
                current_player = [player[1], player[3]]
                group.insert(3, current_player)
                print(group)
                continue

            elif "DPS" in player and "DPS" in roles:
                print(f"Player Information: {player}")
                roles.remove(roles[0])
                current_player = [player[1], player[3]]
                group.insert(i, current_player)
                i -= 1
                print(group)
                continue

            elif len(group) == 5:
                webhook = Webhook.from_url(
                    'https://discord.com/api/webhooks/951948996266561566/aDL8XNin01Yb53gpryUAcrjqxZdwlgk4F7sc2DNmM4KMdygKqJmSTvJnsRwhDkjUmtUa',
                    adapter=RequestsWebhookAdapter())  # Initializing webhook
                embed = discord.Embed(title="Genesis",
                                      description="Gotta later Fix This Hard Coded In")  # Initializing an Embed
                embed.add_field(name="Tank", value=f"{group[4][0]}\n{group[4][1]}", inline=True)  # Adding a new field
                embed.add_field(name="Healer", value=f"{group[3][0]}\n{group[3][1]}", inline=True)  # Adding a new field
                embed.add_field(name="DPS", value=f"{group[2][0]}\n{group[2][1]}", inline=True)  # Adding a new field
                embed.add_field(name="DPS", value=f"{group[1][0]}\n{group[1][1]}", inline=True)  # Adding a new field
                embed.add_field(name="DPS", value=f"{group[0][0]}\n{group[0][1]}", inline=True)  # Adding a new field

                webhook.send(embed=embed)  # Executing webhook and sending embed.
                break

            else:
                print("Something is breaking here")
                while len(group) != 5:
                    missing_player = "Waiting On Players...."
                    group.append(missing_player)
                    print(group)
                webhook = Webhook.from_url('https://discord.com/api/webhooks/946946646724448317/Dggs5bvVVonZMxNrLwwB7aXAjg9va_gp3i-5Kz4ecRWhYbfphXegzv4joRMs9GRl60Wn', adapter=RequestsWebhookAdapter())  # Initializing webhook
                embed = discord.Embed(title="Hello World", description=":wave:")  # Initializing an Embed
                embed.add_field(name="Field name", value="Field value")  # Adding a new field
                webhook.send(embed=embed)  # Executing webhook and sending embed.


bot.run(TOKEN)
