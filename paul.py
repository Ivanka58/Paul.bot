import os  # Импортируем модуль os для работы с переменными окружения
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токен из переменной окружения. Если переменная не задана, будет использовано значение по умолчанию (для локальной разработки)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_DEFAULT_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text("Напишите ваше сообщение:")
    context.user_data['waiting_for_message'] = True

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Повторяет сообщение пользователя, только если он ранее нажал /start."""
    if context.user_data.get('waiting_for_message'):
        await update.message.reply_text(update.message.text)
        context.user_data['waiting_for_message'] = False
    else:
        # Просто игнорируем сообщение, если пользователь не запускал /start
        pass

def main() -> None:
    """Запускает бота."""
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота до прерывания
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
