from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from functools import wraps
from environs import Env


def send_action(action: ChatAction):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context, *args, **kwargs)
        return command_func
    return decorator


@send_action(ChatAction.TYPING)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open('../templates/intro.md', 'r') as introFD:
        intro = introFD.read().format(first_name=update.effective_user.first_name)
        await update.message.reply_markdown_v2(intro)
        await update.message.reply_contact(
            phone_number='+5511992183312',
            first_name='Administração',
            last_name='Parque dos Pássaros 2',
        )
        await update.message.reply_contact(
            phone_number='+5511975134719',
            first_name='Zeladoria',
            last_name='Parque dos Pássaros 2',
        )


env = Env()
env.read_env()
env.read_env('.env.local')

app = ApplicationBuilder().token(env("TELEGRAM_AUTH_TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", start))
app.add_handler(CommandHandler("oi", start))

app.run_polling()
