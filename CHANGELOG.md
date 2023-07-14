# Changelog

All notable changes to this project will be documented in this file.

## Released

### Added
- Initial implementation of the Discord bot.
- Integration with the `discord.ext` module for creating a bot instance.
- Integration with `configparser` for reading the bot's configuration from `config.ini`.
- Integration with OpenAI API for generating AI responses using ChatGPT 3.5 Turbo.
- Implementation of a cache mechanism to store and retrieve generated responses.
- Implementation of a function to generate AI responses based on user messages.
- Event handler for the `on_message` event to process user messages.
- Handling of bot messages by deleting them after 2 minutes.
- Handling of user messages in the "ask-anything" channel.
- Checking user roles for special access and verification.
- Handling of access denial for users without the required roles.
- Handling of API errors and other exceptions during message processing.
- Event handler for the `on_ready` event to print bot readiness information.
- Event handler for command-related errors.
- Starting the bot by running the `bot.run()` function.

## CBT3.5 - ChatBotTurbo3.5 V1- 2023-07-13

### Added
- Initial release of the Discord Chat Bot.
