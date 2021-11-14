import re

import deeppavlov

from telegram import Update
from telegram.ext import CallbackContext

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)

greetings = ["hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g’day", "howdy"]
farewells = ["bye", "goodbye", "see you", "Bye for now", "Have fun", "Speak to you then", "Take care", "Ciao"]
farewells = [t.lower() for t in farewells]
classifier_model = deeppavlov.build_model(deeppavlov.configs.classifiers.intents_snips, download=True)


class NLU:
    def __call__(self, text):
        clean_text = re.sub("[^a-z]+", "", text.lower()).strip()

        if clean_text == "taas":
            return "taas"
        if clean_text in greetings:
            return "greeting"
        elif clean_text in farewells:
            return "farewell"
        elif len(clean_text) < 4:
            return "undefined"
        else:
            return classifier_model([text])[0]


class DM:
    def __call__(self, intent):
        if intent == "undefined":
            return "Sorry, I do not understand you"
        elif intent == "taas":
            return "taas"
        elif intent == "greeting":
            return "Hello!"
        elif intent == "farewell":
            return "Bye-bye!"
        elif intent == "GetWeather":
            return "St.-Petersburg: rains"
        elif intent == "BookRestaurant":
            return "Sorry, I can not book restaurant:("
        elif intent == "PlayMusic":
            return "I do not know how to play music..."
        elif intent == "AddToPlaylist":
            return "I do not have any playlists"
        elif intent == "RateBook":
            return "All books are good!"
        elif intent == "SearchScreeningEvent":
            return "No new upcoming events..."
        elif intent == "SearchCreativeWork":
            return "No vacansies available:("


nlu = NLU()
dm = DM()


def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Hello!")


def handle_text(update: Update, context: CallbackContext):
    result = dm(nlu(update.message.text))

    if result == "taas":
        update.message.reply_sticker('CAACAgIAAxkBAAEC4kBhO4LcIuwfQ_3u2IJ-YihtbURKFAACiwAD9CfbAmiuxAyQv7R7IAQ')
    else:
        update.message.reply_text(result)


if __name__ == "__main__":
    updater = Updater(token="2131073480:AAHa5B1Keh6C_ESv4qEL5JPCnrTMl5JA7NA")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_text))
    updater.start_polling()
