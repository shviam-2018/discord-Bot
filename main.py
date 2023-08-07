import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import datetime
import wikipedia
import webbrowser

load_dotenv()
intents = discord.Intents.all()
intents.members = True  # Enable the intents.members flag
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("BOT ON!")


@bot.event
async def on_member_update(before, after):
    member = after
    if member.status == discord.Status.online:
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"

        message = f"{greeting} {member.name}! Welcome to the server!"
        await member.send(message)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        prefix = bot.command_prefix
        command_list = [
            f"{prefix}campa",
            f"{prefix}search",
            f"{prefix}youtube",
            f"{prefix}google",
            f"{prefix}email",
            f"{prefix}chatgpt",
            f"{prefix}commands",
        ]

        suggestion_text = "Did you mean one of these commands? " + ", ".join(command_list)
        await message.channel.send(suggestion_text)

    await bot.process_commands(message)


@bot.command()
async def campa(ctx):
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    message = f"{greeting}\nI am Campa. Please tell me how can I assist you today."
    await ctx.send(message)


@bot.command()
async def search(ctx, *, query):
    try:
        results = wikipedia.summary(query, sentences=2)
        message = f"According to Wikipedia:\n{results}"
    except wikipedia.exceptions.DisambiguationError:
        message = "Multiple results found. Please be more specific."

    await ctx.send(message)


@bot.command()
async def youtube(ctx):
    await ctx.send("Opening YouTube...")
    webbrowser.open("https://www.youtube.com/")


@bot.command()
async def google(ctx):
    await ctx.send("Opening Google...")
    webbrowser.open("https://www.google.com/")


@bot.command()
async def email(ctx):
    await ctx.send("Opening email...")
    webbrowser.open("https://mail.google.com/")


@bot.command()
async def chatgpt(ctx):
    await ctx.send("Opening Chat GPT...")
    webbrowser.open("https://chat.openai.com/chat")


@bot.command(name="commands")
async def commandlist(ctx):
    prefix = bot.command_prefix
    command_list = [
        f"{prefix}campa: Greet the bot",
        f"{prefix}search <query>: Search Wikipedia for information",
        f"{prefix}youtube: Open YouTube",
        f"{prefix}google: Open Google",
        f"{prefix}email: Open email",
        f"{prefix}chatgpt: Open Chat GPT",
        f"{prefix}commands: Show available commands",
    ]
    message = "Here are the available commands:\n" + "\n".join(command_list)
    await ctx.send(message)


bot.run(os.getenv("TOKEN"))
