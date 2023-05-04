import openai

import sounddevice as sd
import wavio as wv
import os
import threading
import sys
import time

fs = 44100
duration = 5

def record(event, query):
    if os.path.isfile("prompt.wav"):
        os.remove("prompt.wav")

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking=True)
    wv.write("prompt.wav", myrecording, fs, sampwidth=2)

    # Whisper
    # query[0] = whispered text

    if os.path.isfile("prompt.wav"):
        os.remove("prompt.wav")

    event.set()


def main():
    gpt_text = "\nWhat can I do for you?\n\t"
    try:
        while True:
            prompt = input(gpt_text)
            if prompt == "":
                e = threading.Event()
                query = [None]
                t = threading.Thread(target=record, args=(e, query), daemon=True)
                t.start()
                # Progress bar/ wheel not working yet
                while not e.is_set():
                    print('\tRecording.', end="\r")
                    time.sleep(0.4)
                    print('\tRecording..', end="\r")
                    time.sleep(0.4)
                    print('\tRecording...', end="\r")
                    time.sleep(0.4)
                # Aanpassen aan return value enzo
                if query[0] is None:
                    print('\tDit was je ingesproken tekst', end="\r")
            else:
                pass
    except KeyboardInterrupt:
        print("\nGoodbye.")
        exit()

main()
