from dotenv import load_dotenv
import os
import telebot
import youtube_dl

load_dotenv()

DOWNLOADABLE = False

bot = telebot.TeleBot(os.getenv('API_KEY'))


@bot.message_handler(commands=['start', 'help'])
def responder(mensagem):
    global USER_ID

    bot.reply_to(mensagem, '''/baixarmp3 Baixa seu vídeo em mp3''')
    USER_ID = mensagem.chat.id


@bot.message_handler(commands=['baixarmp3'])
def baixar_mp3(mensagem):
    global DOWNLOADABLE
    
    bot.reply_to(mensagem, 
        '''
        Envie seu link válido do YouTube    
            
        ''')
    DOWNLOADABLE = True


def downloadable():
    if DOWNLOADABLE:
        return True
    else:
        return False


@bot.message_handler(func=downloadable)
def download_mp3(link):
    global USER_ID
    global DOWNLOADABLE

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
            bot.send_audio(USER_ID, audio_file)

        os.remove(filename)
        print("Download complete... {}".format(filename))

        DOWNLOADABLE = False

    except:
        bot.send_message(USER_ID, 'Não foi possível concluir a solicitação de seu envio, tente novamente')


bot.polling()
