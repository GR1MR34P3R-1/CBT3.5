import discord
from discord.ext import commands
import configparser
import openai
import asyncio

# Read config.ini
config = configparser.ConfigParser()
config.read('config.ini')

token = config['Bot']['token']
api_key = config['OpenAI']['api_key']

# Create an instance of the commands.Bot class
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize the OpenAI API
openai.api_key = api_key

# Define a function to generate a response using ChatGPT 3.5 Turbo
async def generate_response(message):
    model_prompt = f"User: {message.content}\nAI: "
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=model_prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        user=str(message.author.id),
    )
    generated_text = response.choices[0].text.strip()

    if "?" not in generated_text:
        prompt_with_question = f"{generated_text} AI: "
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_with_question,
            max_tokens=100,
            temperature=0.7,
            n=1,
            stop=None,
            user=str(message.author.id),
        )
        generated_text = response.choices[0].text.strip()

    return generated_text

# Event handler for the on_message event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        # Delete bot messages after 2 minutes
        await asyncio.sleep(120)
        await message.delete()
        return

    if message.channel.name == "ask-anything":
        special_access_role = discord.utils.get(message.guild.roles, name="Special Access")
        verified_role = discord.utils.get(message.guild.roles, name="Verified")

        if special_access_role in message.author.roles and verified_role in message.author.roles:
            # User has both "Verified" and "Special Access" roles
            response = await generate_response(message)
            await message.channel.send(response)

            # Delete user question after 1 minute
            await asyncio.sleep(60)
            await message.delete()

            # Delete bot response after 2 minutes
            await asyncio.sleep(120)
            async for msg in message.channel.history(limit=200):
                if msg.author == bot.user and msg.reference is not None and msg.reference.message_id == message.id:
                    await msg.delete()
                    break
        elif verified_role in message.author.roles:
            # User has only "Verified" role
            # Delete user message instantly
            await message.delete()

            # Send access denial message
            access_denial_message = await message.channel.send("You do not have the required role for special access.")

            # Delete access denial message after 30 seconds
            await asyncio.sleep(30)
            await access_denial_message.delete()
        else:
            await message.channel.send("You do not have the required role for special access.")

    await bot.process_commands(message)

# Event handler for the on_ready event
@bot.event
async def on_ready():
    print(f'Bot is ready. Connected to {len(bot.guilds)} server(s).')

# Start the bot
bot.run(token)
