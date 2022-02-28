from dotenv import load_dotenv
import os
import telebot
import youtube_dl

load_dotenv()

API_KEY = os.getenv('API_KEY')
DOWNLOADABLE = False

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start', 'help'])
def responder(mensagem):
    bot.reply_to(mensagem,
        '''
        /baixarmp3 Baixa seu vídeo em mp3

        ''')


@bot.message_handler(commands=['baixarmp3'])
def baixar_mp3(mensagem):
    bot.reply_to(mensagem, 
        '''
        Envie seu link válido do YouTube    
            
        ''')
    global DOWNLOADABLE
    DOWNLOADABLE = True


def downloadable(self):
    if DOWNLOADABLE:
        return True
    else:
        return False


@bot.message_handler(func=downloadable)
def download_mp3(link):
    try:
        video_url = link.text
        video_info = youtube_dl.YoutubeDL().extract_info(
            url = video_url,download=False
        )
        filename = f"{video_info['title']}.mp3"
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        with open(filename, 'rb') as audio_file:
            bot.send_audio('1095525330', audio_file)

        os.remove(filename)

        print("Download complete... {}".format(filename))

        global DOWNLOADABLE
        DOWNLOADABLE = False

    except:
        bot.send_message('1095525330', 'Não foi possível concluir a solicitação de seu envio, tente novamente')


bot.polling()
