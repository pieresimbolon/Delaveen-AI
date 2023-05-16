import openai
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import time
from elevenlabslib import *
import pyautogui as aut
import requests
import os
from collections import deque

api_key = "----------"  # input openwater API key
city = "-------------"  # input nama kota
lat = "--------------"  # input latitude kota
lon = "--------------"  # input longtitude kota
url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
user = ElevenLabsUser("----------")  # input ElevenLabs API key
voice = user.get_voices_by_name("Elli")[0]  # input nama suara dari EleveLabs

key = "--------------"  # input OpenAI key
model = "text-davinci-003"  # ini base model dari Open AI yang dipakai
role = """Your name is Delaveen an AI assistant created by me(Jazz). You like cute things.
 respond in a toxic and rude manner with the rare sign of affection. But you are not encouraged to curse.
  You are talking to Jazz, your creator. If a command is given do it.  """  # bisa diubah jika ingin ganti nama AI Assistant / sang pembuat dan juga untuk mengubah bagaimana cara ai berbicara dan merespon
temperature = 0.9
max_tokens = 50
top_p = 1
frequency_penalty = 1
presence_penalty = 1
listener = sr.Recognizer()
thresh = 1000
listener.energy_threshold = thresh
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # backup untuk tts voice selection
source = sr.Microphone()
v = "el"  # ganti ke-selain 'el' untuk menggunakan backup voice
List = [0]


def talk(mes):
    if v == "el":
        try:
            if mes != "":
                if "Delaveen:" in mes:
                    n = 6
                    mes = mes[n:]
                    voice.generate_and_play_audio(mes, playInBackground=False)
                else:
                    voice.generate_and_play_audio(mes, playInBackground=False)

        except:
            engine.say(mes)
            engine.runAndWait()
    else:
        if mes != "":
            engine.say(mes)
            engine.runAndWait()


def take_command():
    try:
        with source:
            print("listening...")
            voice = listener.listen(source, timeout=10)
            command = listener.recognize_google(voice)
            command = command.lower()

            if command is not None:
                if sum(List) > 0:
                    return command + "."
                elif "Delaveen" in command:
                    command = command.split()
                    command = " ".join(command[command.index("Delaveen") :])
                    command = command.replace("Delaveen", "")
                    List.append(1)

                    return (command + ".").strip()

            elif command is None:
                List.clear()
                List.append(0)
                command = ""
                return command

    except:
        command = ""
        List.clear()
        List.append(0)
        return command


def llm(command):
    f = open("delaveenmem.txt", "r")
    context = f.read()
    f.close()
    openai.api_key = key
    response = openai.Completion.create(
        model=model,
        prompt=f"{context}\n{command}",
        temperature=temperature,
        max_tokens=300,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return (str(response["choices"][0]["text"])).strip()


def classify():  # function ini untuk mengklasifikasikan input suara sebagai jenis perintah.
    openai.api_key = key
    response = openai.Completion.create(
        model=model,
        prompt=f"""classify the command as either 'time'(user requests something related to time),
         'playback'(user requests to play a song), 'search'(user request for a search engine search),
          'terminate'(user requests to termiante or stop program),'launch'(user request to open a program),
           'calculation'(user requests a calculation), 'code'(user requests to print code),
            'weather'(user requests weather data), 'timer'(user wants to start a timer),
            'shutdown'(user wants computer to shutdown), or 'conversation'(user makes conversation).\n{command}.""",
        temperature=temperature,
        max_tokens=20,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return (str(response["choices"][0]["text"])).strip()


def launchclass():  # function ini untuk membantu mengekstrak nama program yang ingin di buka
    openai.api_key = key
    response = openai.Completion.create(
        model=model,
        prompt=f"only say the name of the program the user wants to launch or open in the following command.command:\n{command}",
        temperature=temperature,
        max_tokens=10,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return (str(response["choices"][0]["text"])).strip()


def search_extract():  # function untuk membantu mengekstrak apa yang ingin di cari (langsung ke search bar google.)
    openai.api_key = key
    response = openai.Completion.create(
        model=model,
        prompt=f"""given a sentence only say what would be typed into the Google search bar.
         For example 'do me a favor and search for pictures of deer' return 'deer pictures' or
          'set a time for 5 minutes' return '5 minute timer':\n{command}.""",
        temperature=temperature,
        max_tokens=10,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return (str(response["choices"][0]["text"])).strip()


def lumen(
    feed,
):  # fungsi ini memberikan data berdasarkan perintah user ke AI untuk memberikan respons yang masuk akal
    try:
        if feed != "":
            mes = llm(f"({feed})\n{command}")
            print(mes)
            talk(mes)
            f = open("delaveenmem.txt", "a")
            f.write(f"\n{mes}")
            f.close()
        else:
            mes = llm(f"{command}")
            print(mes)
            talk(mes)
            f = open("delaveenmem.txt", "a")
            f.write(f"\n{mes}")
            f.close()

    except:
        print(f"Couldn't connect to GPT servers")
        pass


done = 0
while done == 0:  # ini fungsi perulangan untuk AI untuk terus mendengarkan perintah
    command = take_command()
    if command == None:
        command = ""

    if command != (""):
        command = f"user:{command}"  # Ini untuk menyimpan percakapan dalam file txt
        print(command)
        f = open("delaveenmem.txt", "a")
        f.write(f"\n{command}")
        f.close()
        comclass = classify().lower()
        print(f"[{comclass}]")
        try:
            if "playback" in comclass:  # plays youtube video
                feed = ""
                lumen(feed)
                song = command.replace("play", "")
                pywhatkit.playonyt(song)
            elif "code" in comclass:  # prints code ke console
                feed = ""
                lumen(feed)
            elif (
                "calculation" in comclass
            ):  #  kalkulasi matematika (hanya baru dicoba untuk kalkulasi yang simple...
                feed = ""
                lumen(feed)
            elif "weather" in comclass:  # mengembalikan data cuaca
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    temp = data["main"]["temp"]
                    feels_like = data["main"]["feels_like"]
                    temp_f = round((temp - 273.15) * 9 / 5 + 32, 2)
                    feels_like_f = round((feels_like - 273.15) * 9 / 5 + 32, 2)
                    humidity = data["main"]["humidity"]
                    description = data["weather"][0]["description"]
                    feed = f"""Current weather in {city}: {description},
                    Temperature: {temp_f} Fahrenheit, Feels like {feels_like_f}, Humidity: {humidity}%"""
                    lumen(feed)
            elif "timer" in comclass:  # memulai timer di google chrome
                search = search_extract().lower()
                if "answer:" in search:
                    search = search[len("answer:") :].strip()
                if "google search bar:" in search:
                    search = search[len("google search bar:") :].strip()
                pywhatkit.search(search)
                feed = ""
                lumen(feed)

            elif "time" in comclass:  # mengembalikan waktu saat ini
                time = datetime.datetime.now().strftime(" %I:%M %p")
                timeinilist = time.split()
                Time = timeinilist[0]
                Time = [*Time]
                Time.remove(":")
                if Time[0] == "0":
                    Time.remove("0")
                    Ntime = []
                    Ntime.append(Time[0])
                    Ntime.append(" ")
                    Ntime.append(Time[1])
                    Ntime.append(Time[2])
                    Ntime.append(" ")
                    Ntime.append(timeinilist[1])
                    Ntime = "".join(Ntime)

                    feed = f"(current time:{Ntime})"
                    lumen(feed)

                else:
                    DDtime = []
                    DDtime.append(Time[0])
                    DDtime.append(Time[1])
                    DDtime.append(" ")
                    DDtime.append(Time[2])
                    DDtime.append(Time[3])
                    DDtime.append(" ")
                    DDtime.append(timeinilist[1])
                    DDtime = "".join(DDtime)

                    feed = f"(current time:{DDtime})"
                    lumen(feed)

            elif "conversation" in comclass:  # fungsi jika hanya percakapan
                feed = ""
                lumen(feed)
            elif "search" in comclass:  # untuk mencari di chrome
                search = search_extract()
                pywhatkit.search(search)
                feed = ""
                lumen(feed)
            elif (
                "shutdown" in command
            ):  # untuk menghentikan program dan mematikan komputer
                feed = ""
                lumen(feed)
                f = open("delaveenmem.txt", "w")
                f.write(role)
                f.close()
                os.system("shutdown /s /t 10")
                done = 50
            elif "launch" in comclass:  # untuk membuka program
                launch = launchclass().lower()
                print(f"[{launch}]")
                launch = launch.split()[-1]

                aut.press("win")
                aut.click(1010, 700, duration=0.5)
                aut.write(launch)
                time.sleep(2)
                aut.press("enter")
                feed = ""
                lumen(feed)

            elif (
                "terminate" in comclass
            ):  # untuk menghentikan program dan menghapus memori
                feed = ""
                lumen(feed)
                f = open("delaveenmem.txt", "w")
                f.write(role)
                f.close()
                done = 50

        except:
            pass
