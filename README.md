# 🤖 CBT3.5 - ChatBotTurbo3.5 🚀

CBT3.5 is an amazing program that utilizes the Discord API and the power of ChatGPT 3.5 Turbo to create an interactive bot that can respond to user messages.

## Prerequisites
Before you can run CBT3.5, make sure you have the following:

- Python installed on your system.

## Getting Started
📥 Clone this repository to your local machine or download the source code.

🔧 Install the required dependencies by running the following command:

pip install -r requirements.txt

📝 Create a file named `config.ini` in the same directory as the program file and replace the following placeholders:

- `YOUR_DISCORD_BOT_TOKEN` with your actual Discord bot token.
- `YOUR_OPENAI_API_KEY` with your actual OpenAI API key.

🖥️ Open a terminal or command prompt and navigate to the directory where the program is located.

▶️ Run CBT3.5 using the following command:
python3 main.py


The bot should now be online and ready to respond to user messages in the specified Discord server.

## Features
🔹 The bot listens for messages in a channel named "ask-anything" and responds using the power of ChatGPT 3.5 Turbo.
🔹 Users with "Special Access" role can ask questions and receive responses from the bot.
🔹 User questions and bot responses are automatically deleted after a certain period to keep the channel clean.

## Customization
You can customize the behavior of CBT3.5 by modifying the following variables in the program:

- `command_prefix`: The prefix used to invoke bot commands (default: `!`).
- `intents`: The Discord intents to enable for the bot (default: `discord.Intents.default()`).
- `engine`: The ChatGPT engine to use for generating responses (default: `text-davinci-003`).
- `max_tokens`: The maximum number of tokens in the generated response (default: `100`).
- `temperature`: The temperature parameter for response generation (default: `0.7`).
- `delete_delay`: The delay (in seconds) before deleting user messages and bot responses (default: `120` and `60` respectively).

Feel free to modify these variables according to your needs.

## Contributions
Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.

## Credits
CBT3.5 is developed by 6R1MR34P3R-1.

## License
This program is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the terms of the license.

## Have A Good Day!!
🌟 Have fun exploring the capabilities of CBT3.5 and enjoy interacting with the Discord bot! If you have any questions or need assistance, don't hesitate to reach out. 😊

