from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import pyaudio
import sys

# Initialize a recognizer for speech recognition
recognizer = speech_recognition.Recognizer()

# Initializes the speaker for the responses
speaker = tts.init()

# Sets the rate at which the assistant will talk
speaker.setProperty('rate', 250)

# To do list
to_do_list = ['Go shopping', 'Clean room', 'Do homework', 'Buy groceries']


# Makes the assistant say something and wait for a response
def speech(text):
    speaker.say(text)
    speaker.runAndWait()


# Functions to create a note
def create_note():
    global recognizer

    speech('What do you want to write onto your note?')

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                # Listens for the input audio
                recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
                audio = recognizer.listen(mic)

                # Creates a note from the input audio
                note = recognizer.recognize_google(audio)
                note = note.lower()

                # Creates a file name for the output note
                speech('Choose a file name')

                # Listens for the file name for the output note
                recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
                audio = recognizer.listen(mic)

                # Creates the file name from the input audio
                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            
            # Creates the note
            with open(f'{filename}.txt', 'w') as file:
                file.write(note)
                done = True
                speech(f'I successfully created the note {filename}')

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speech('I did not get that. Please try again!')


# Adds a to do to the to do list
def add_to_do():
    global recognizer

    speech('What to do do you want to add?')

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                # Listens for the input audio
                recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
                audio = recognizer.listen(mic)

                # Creates a to do from the input audio
                item = recognizer.recognize_google(audio)
                item = item.lower()

                # Adds the to do to the to do list
                to_do_list.append(item)
                done = True

                speech(f'I added {item} to the to do list!')

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speech('I did not get that. Please try again!')


# Shows the to do list
def show_to_dos():
    speaker.say('The items on your to do list are the following')
    for item in to_do_list:
        speaker.say(item)
    speaker.runAndWait()


# Greets the user
def hello():
    speech('Hello. What can I do for you?')


# Quits from the assistant
def quit():
    speech('Bye, see you next time')
    sys.exit(0)


mappings = {
    'greeting': hello,
    'create_note': create_note,
    'add_todo': add_to_do,
    'show_to_dos': show_to_dos,
    'exit': quit
}


# Initializes the assistant
assistant = GenericAssistant('intents.json', intent_methods = mappings)
assistant.train_model()

# assistant.save_model()
# assistant.load_model()

# Listens for the user voice input
while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
