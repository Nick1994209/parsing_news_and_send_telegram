from core import create_log
from core import models
from .commands import Commands


def reply_on_telegram_messages():
    for bot in models.TelegramBot.objects.all():
        for message in bot.get_last_messages():
            bot_user, _ = bot.users.get_or_create(
                user_id=message['from']['id'],
                username=message['from'].get('username', ''),
                first_name=message['from']['first_name'],
                last_name=message['from'].get('last_name', ''),
            )

            Commands.get_command(bot_user, message)
            # try:
            #     Commands.get_command(bot_user, message)
            # except Exception as e:
            #     create_log.create(
            #         'command_error \t' + str(e), 'reply_on_telegram_messages.log'
            #     )
    return 1
