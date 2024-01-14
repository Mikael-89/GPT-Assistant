import openai
import pyttsx3
import speech_recognition as sr

# open ai API
openai.api_key = "YOUR API KEY HERE"  # add your own key

# text to speech engine
engine = pyttsx3.init()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skilling unknown error")


def generate_response(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-0613",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        # wait for user to say "Hello"
        print("Say 'Hello' to start recording your question.")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(
                    audio, language="en-US")
                if transcription.lower() == "hello":
                    print(transcription)
                    # Record audio
                    filename = "input.wav"
                    print("Ask your question..")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(
                            source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said {text}")

                        # generated response
                        response = generate_response(text)
                        print(f"Computer: {response}")

                        # voice response
                        speak_text(response)
            except Exception as e:
                print("An error occured: {}".format(e))


if __name__ == "__main__":
    main()
