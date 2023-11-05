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
    await update.message.reply_markdown_v2(
        f'*Olá, {update.effective_user.first_name}\\!*\n'
        '\n'
        'Tenho algumas informações para te ajudar como morador no Parque dos Passaros 2\\!\n'
        'Interfones úteis:\n'
        '\tPortaria:\n'
        '\t\t*`100`*\n'
        '\t\t*`94`*\n'
        '\tUtilidades:\n'
        '\t\tSedex/Entregas/"Base 3":\n'
        '\t\t\t*`203`*\n'
        '\tPara ligar para algum apartamento,\n'
        '\t\tdigite o número do bloco seguido\n'
        '\t\tdo número do apartamento, exemplos:\n'
        '\t\t\t*`1 107`* \\(apto 107 do bloco 1\\)\n'
        '\t\t\t*`3 37`* \\(apto 37 do bloco 3\\)\n'
        '\n'
        'E a seguir, alguns contatos úteis \\(que também atendem via WhatsApp\\)\n'
        '\tAdministração:\n'
        '\t\t[\\(11\\) 9\\-9218\\-3312](tel:+5511992183312)\n'
        '\tZeladoria:\n'
        '\t\t[\\(11\\) 9\\-7513\\-4719](tel:+5511975134719)\n'
        '\n'
        'Se tiver qualquer problema, por favor, nos informe\\!',
    )
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
