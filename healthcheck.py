import os
import logging
from threading import Thread
from flask import Flask
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, 
    Filters, CallbackQueryHandler, ConversationHandler,
    PicklePersistence
)
from telegram import ParseMode

# Import handlers
from handlers.admin_handlers import (
    start_admin, list_quizzes, create_quiz, import_questions_from_pdf,
    handle_quiz_details, handle_quiz_question, handle_quiz_options,
    handle_quiz_correct, handle_quiz_continue, handle_quiz_create_confirm,
    handle_quiz_cancel, handle_pdf_callback, delete_quiz
)
from handlers.quiz_handlers import (
    take_quiz, handle_quiz_choice, handle_quiz_answer,
    finish_quiz, handle_finish_callback
)

from config import TELEGRAM_TOKEN, PORT

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_handlers(dispatcher):
    # Admin handlers
    dispatcher.add_handler(CommandHandler("start", start_admin))
    dispatcher.add_handler(CommandHandler("list", list_quizzes))
    dispatcher.add_handler(CommandHandler("create", create_quiz))
    dispatcher.add_handler(CommandHandler("import", import_questions_from_pdf))
    dispatcher.add_handler(CommandHandler("delete", delete_quiz))
    
    # Quiz handlers
    dispatcher.add_handler(CommandHandler("take", take_quiz))
    
    # Callback handlers
    dispatcher.add_handler(CallbackQueryHandler(handle_quiz_choice, pattern="^quiz_"))
    dispatcher.add_handler(CallbackQueryHandler(handle_quiz_answer, pattern="^answer_"))
    dispatcher.add_handler(CallbackQueryHandler(handle_finish_callback, pattern="^finish_"))
    dispatcher.add_handler(CallbackQueryHandler(handle_pdf_callback, pattern="^pdf_"))
    
    # Conversation handlers
    create_quiz_handler = ConversationHandler(
        entry_points=[],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, handle_quiz_details)],
            2: [MessageHandler(Filters.text & ~Filters.command, handle_quiz_question)],
            3: [MessageHandler(Filters.text & ~Filters.command, handle_quiz_options)],
            4: [MessageHandler(Filters.text & ~Filters.command, handle_quiz_correct)],
            5: [MessageHandler(Filters.text & ~Filters.command, handle_quiz_continue)]
        },
        fallbacks=[
            CommandHandler("cancel", handle_quiz_cancel),
            CommandHandler("done", handle_quiz_create_confirm)
        ],
        name="create_quiz",
        persistent=True
    )
    dispatcher.add_handler(create_quiz_handler)

def run_healthcheck():
    app = Flask(__name__)

    @app.route('/')
    def health():
        return "Bot is running!"

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def main():
    logger.info("Starting bot...")
    
    # Create persistence object
    persistence = PicklePersistence(filename='quiz_bot_data')
    
    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_TOKEN, persistence=persistence)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Set up handlers
    setup_handlers(dp)
    
    # Start the webhook
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://quizmaster-bot.koyeb.app/{TELEGRAM_TOKEN}"
    )
    
    logger.info("Bot started")
    
    # Run the Flask health check server
    health_thread = Thread(target=run_healthcheck)
    health_thread.daemon = True
    health_thread.start()
    
    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
