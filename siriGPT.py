# Imports.
import openai
import os
import sounddevice as sd
import sys
import threading
import time
import wavio as wv

# Module files.
import gpt
import whisper


# Recording settings.
rec_fs = 44100
rec_duration = 6
# Records prompt & sends to whisper API.
def record(event, query):
    # Deletes recording file if one exists.
    if os.path.isfile("prompt.wav"):
        os.remove("prompt.wav")

    # Records & saves prompt.
    myrecording = sd.rec(int(rec_duration * rec_fs), samplerate=rec_fs, channels=1, blocking=True)  # Need to check channel
    wv.write("prompt.wav", myrecording, rec_fs, sampwidth=2)

    transcript = whisper.transcribe()
    query[0] = transcript.text

    # Deletes recording file.
    if os.path.isfile("prompt.wav"):
        os.remove("prompt.wav")

    # Sets event to signal recording is over.
    event.set()


def main():
    # Initial text.
    gpt_text = "\nWhat can I do for you?\n\t"
    try:
        while True:
            prompt = ""
            prompt = input(gpt_text)
            if prompt == "":
                queryT = [None]
                e = threading.Event()
                t = threading.Thread(target=record, args=(e, queryT), daemon=True)
                t.start()
                # Progress bar/ wheel not working yet
                while not e.is_set():
                    print('\tRecording.', end="\r")
                    time.sleep(0.4)
                    print('\tRecording..', end="\r")
                    time.sleep(0.4)
                    print('\tRecording...', end="\r")
                    time.sleep(0.4)
                prompt = queryT[0]
                # Aanpassen aan return value enzo
                if prompt is None:
                    print('\tError parsing prompt.', end="\r")
                else:
                    print(f'\t{prompt}', end="\r")

            # Send prompt to GPT API

    # Catches ctrl+c & exits program.
    except KeyboardInterrupt:
        print("\nGoodbye.")
        exit()

main()
