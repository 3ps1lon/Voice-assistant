import os
import requests
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

'''p = requests.get("https://images.wallpaperscraft.ru/image/single/krasivyj_kotik_kot_morda_pushistyj_93328_1920x1080.jpg")
//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img
out = open("images/img.jpg", "wb")
out.write(p.content)
out.close()
#https://www.google.ru/search?q=котики&tbm=isch    %20 пробел'''


sec = 0
global k
k = 0

opts = {
    "alias": ('лена', 'леночка', 'елена', 'ленусик', 'ленка', 'еленочка',
              'ленуся'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'какой', 'какая', 'какое', 'открой','включи'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час', 'время'),
        "date": ('число', 'год', 'месяц', 'день', 'дата'),
        "quit": ('выход', 'стоп', 'домой', 'хватит', 'прекрати', 'выключись', 'выйди', 'выйти'),
        "sec_start": ('секундомер старт', 'запуск секундомера'),
        "sec_stop": ('секундомер стоп', 'останови секундомер', 'выключи секундомер'),
        "photo": ('фото', 'картинку', 'фотографию', 'фоточку'),
        "video": ('видео', 'видосик'),
        "audio": ('музыку', 'аудио')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def command():
    global k
    r = sr.Recognizer()
    with sr.Microphone() as source:

        audio = r.listen(source)

    try:

        zadanie = r.recognize_google(audio, language="ru-RU").lower()
        if zadanie.startswith(opts["alias"]):

            cmd = zadanie

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
                k = 1

    except sr.UnknownValueError:
        zadanie = command()
    except sr.RequestError:
        speak("Неизвестная ошибка, проверьте интернет!")
        zadanie = command()

    return zadanie


def callback(voice):
    global k


    if voice.startswith(opts["alias"]):

        cmd = voice

        for x in opts['alias']:
            cmd = cmd.replace(x, "").strip()
            k = 1

        for i in opts['tbr']:
            cmd = cmd.replace(i, "").strip()

        non_mg = cmd

        for c, v in opts['cmds'].items():
            if c == 'photo' or c == 'video' or c == 'audio':
                for i in v:
                    non_mg = non_mg.replace(i, "").strip()

        cmd = recognize_cmd(cmd)
        cmd = cmd['cmd']
        return cmd, non_mg


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


def execute_cmd(cmd):
    global k
    if k == 1:
        text = str(cmd[1])
        if cmd[0] == 'ctime':
            # сказать текущее время
            now = datetime.datetime.now()
            speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

        elif cmd[0] == 'date':
            now = datetime.datetime.now()
            speak("Сейчас " + now.strftime("%d/%m/%Y"))

        elif cmd[0] == 'quit':
            speak('Пока пока')
            quit()
        elif cmd[0] == 'sec_start':
            global sec
            sec = time.time()
        elif cmd[0] == 'sec_stop':
            if sec != 0:
                speak('Прошло ' + str(round(time.time() - sec, 2)) + ' секунды')
                sec = 0
            else:
                speak('Секундомер не запущен')
        elif cmd[0] == 'photo':
            os.system(r"C:\Users\Strixgamer\PycharmProjects\kursach\media\images" + "\\" + text + ".jpg")
        elif cmd[0] == 'video':
            os.system(r"C:\Users\Strixgamer\PycharmProjects\kursach\media\videos" + "\\" + text + ".mp4")
        elif cmd[0] == 'audio':
            os.system(r"C:\Users\Strixgamer\PycharmProjects\kursach\media\musics" + "\\" + text + ".mp3")

        else:
            speak('Команда не распознана, повторите!')

        k = 0

    else:
        execute_cmd(callback(command()))


speak_engine = pyttsx3.init()

speak("Лена слушает")

while True:
    speak("Говорите")
    time.sleep(1)
    execute_cmd(callback(command()))
