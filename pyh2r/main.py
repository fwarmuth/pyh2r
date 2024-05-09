from threading import Thread

def start_flask():
    import pyh2r.server
    # Start flask app in production mode
    pyh2r.server.app.run(debug=False)

def start_bot():
    import pyh2r.telegram_bot
    pyh2r.telegram_bot.bot.infinity_polling()

def main():
    print("Starting...")
    # Create threads for the Flask server and the Telegram bot
    flask_thread = Thread(target=start_flask)
    telegram_thread = Thread(target=start_bot)

    # Start the threads
    flask_thread.start()
    telegram_thread.start()

    print("running...")

    # Wait for the threads to finish
    flask_thread.join()
    telegram_thread.join()

    print("Done")

if __file__ == '__main__':
    main()