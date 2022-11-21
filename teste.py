from dotenv import load_dotenv
import os
import telebot
import youtube_dl


class Bot:
    def __init__(self, bot):
        self.bot = bot

    def answer(self, mensagem):
        self.bot.reply_to(mensagem, '''/baixarmp3 Baixa seu vídeo em mp3''')
        self.user_id = mensagem.chat.id

    def get_video_link(self):
        pass

    def download_mp3(self):
        pass


load_dotenv()
bot = telebot.TeleBot(os.getenv('API_KEY'))
kita = Bot(bot)

@bot.message_handler(commands=['start', 'help'])
def answerr(mensagem):
    kita.answer(mensagem)

bot.polling()
