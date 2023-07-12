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

# Define a dictionary to cache generated responses
response_cache = {}

# Define a function to generate a response using ChatGPT 3.5 Turbo
async def generate_response(message):
    model_prompt = f"User: {message.content}\nAI: "
    cache_key = model_prompt + str(message.author.id)
    
    if cache_key in response_cache:
        generated_text = response_cache[cache_key]
    else:
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
        
        response_cache[cache_key] = generated_text
    
    if "?" not in generated_text:
        prompt_with_question = f"{generated_text} AI: "
        cache_key = prompt_with_question + str(message.author.id)
        
        if cache_key in response_cache:
            generated_text = response_cache[cache_key]
        else:
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
            
            response_cache[cache_key] = generated_text
    
    return generated_text

# Event handler for the on_message event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        # Delete bot messages after 2 minutes
        await asyncio.sleep(120)
        try:
            await message.delete()
        except discord.errors.NotFound:
            pass
        return

    if message.channel.name == "ask-anything":
        special_access_role = discord.utils.get(message.guild.roles, name="Special Access")
        verified_role = discord.utils.get(message.guild.roles, name="Verified")

        if special_access_role in message.author.roles and verified_role in message.author.roles:
            try:
                response = await generate_response(message)
                await message.channel.send(response)

                # Delete user question after 1 minute
                await asyncio.sleep(60)
                try:
                    await message.delete()
                except discord.errors.NotFound:
                    pass

                # Delete bot response after 2 minutes
                await asyncio.sleep(120)
                async for msg in message.channel.history(limit=200):
                    if msg.author == bot.user and msg.reference is not None and msg.reference.message_id == message.id:
                        try:
                            await msg.delete()
                        except discord.errors.NotFound:
                            pass
                        break
            except openai.Error as e:
                # Handle OpenAI API errors
                await message.channel.send(f"OpenAI API error: {str(e)}")
            except Exception as e:
                # Handle other errors
                await message.channel.send(f"An error occurred: {str(e)}")
        elif verified_role in message.author.roles:
            # User has only "Verified" role
            # Delete user message instantly
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass

            # Send access denial message if not already sent
            error_sent = False
            async for msg in message.channel.history(limit=10):
                if msg.author == bot.user and msg.content == "You do not have the required role for special access.":
                    error_sent = True
                    break
            if not error_sent:
                await message.channel.send("You do not have the required role for special access.")

        else:
            # Send access denial message if not already sent
            error_sent = False
            async for msg in message.channel.history(limit=10):
                if msg.author == bot.user and msg.content == "You do not have the required role for special access.":
                    error_sent = True
                    break
            if not error_sent:
                await message.channel.send("You do not have the required role for special access.")

    await bot.process_commands(message)

# Event handler for the on_ready event
@bot.event
async def on_ready():
    print(f'Bot is ready. Connected to {len(bot.guilds)} server(s).')

# Event handler for command-related errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore invalid commands silently
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument.")
    elif isinstance(error, openai.Error):
        await ctx.send(f"OpenAI API error: {str(error)}")
    else:
        # Log the error and send a generic error message
        error_message = f"An error occurred: {str(error)}"
        print(f"Error: {error_message}")
        await ctx.send("An error occurred while processing the command.")

# Start the bot
bot.run(token)
