import tkinter as tk
import threading
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
import os

# Create a Recognizer object
recognizer = sr.Recognizer()

# Initialize the OpenAI client
client = OpenAI(api_key='YOUR CHATGPT3.5 API HERE')

# Define a list of questions
questions = [
    'How long did it take you to complete this coding task (in months)?',
    'Can you outline the timeline of your work on this coding task? How much time was allocated to each sub-task?',
    'What were the main challenges you encountered for the coding task, and what lessons did you learn from them?',
    'How did you ensure the usability and aesthetic appeal of your application interface? Can you share your design and implementation strategies?',
    'What steps did you take to maintain professional code quality and application appearance?',
    'Reflecting on your experience with this coding task, what are three key takeaways you would like to emphasize?',
    'What aspects of the coding task do you believe you handled well, and what tips can you offer based on your experience?',
]

# Create the main window
root = tk.Tk()
root.title("Interview Information")

# Create a text window to display information
info_text = tk.Text(root, height=50, width=200)
info_text.pack(padx=15, pady=15)

# Open a file to write questions and generated responses
def process_interview():
    with open('write.txt', 'w') as file:
        # Add questions to the text window and the file
        for question in questions:
            info_text.insert(tk.END, question + '\n')
            file.write(question + '\n')

            # Use the microphone to capture audio
            with sr.Microphone() as source:
                tts = gTTS(text=question, lang='en')
                tts.save("question.mp3")

                # Play the generated speech file
                os.system("afplay question.mp3")  # For macOS
                info_text.insert(tk.END, "Please speak...\n")
                file.write("Please speak...\n")

                try:
                    # Continuously listen for audio until silence is detected
                    audio = recognizer.listen(source, timeout=10)  # Set timeout parameter to 10 seconds
                    info_text.insert(tk.END, "Processing...\n")
                    file.write("Processing...\n")

                    text = recognizer.recognize_google(audio, language='en-US')  # Recognize audio
                    info_text.insert(tk.END, "You said: " + text + '\n')
                    file.write("You said: " + text + '\n')

                    # Use the OpenAI GPT-3.5 model to generate a response
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system",
                             "content": "You are an interview assistant, you can choose a deeper question based on the user's answer or make a summary."},
                            {"role": "user", "content": text}
                        ]
                    )
                    generated_response = completion.choices[0].message
                    info_text.insert(tk.END, "Generated response: " + generated_response.content + '\n')
                    file.write("Generated response: " + generated_response.content + '\n')

                    tts = gTTS(text=generated_response.content, lang='en')
                    tts.save("response.mp3")

                    # Play the generated speech file
                    os.system("afplay response.mp3")  # For macOS
                    info_text.insert(tk.END, "Speak now...\n")
                    file.write("Speak now...\n")

                    audio_additional_info = recognizer.listen(source, timeout=5)  # Capture additional information's audio input
                    info_text.insert(tk.END, "Processing additional info...\n")
                    file.write("Processing additional info...\n")

                    additional_info = recognizer.recognize_google(audio_additional_info, language='en-US')
                    info_text.insert(tk.END, "Additional info: " + additional_info + '\n')
                    file.write("Additional info: " + additional_info + '\n')

                except sr.UnknownValueError:
                    info_text.insert(tk.END, "No speech detected\n")
                    file.write("No speech detected\n")
                except sr.RequestError as e:
                    info_text.insert(tk.END, "Unable to connect to Google Speech Recognition service: {0}\n".format(e))
                    file.write("Unable to connect to Google Speech Recognition service: {0}\n".format(e))

    # Generate a summary
    def generate_summary(text):
        # Use the OpenAI GPT-3.5 model to generate a summary
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a summarizer, summarize the full text."},
                {"role": "user", "content": text}
            ]
        )
        summary = completion.choices[0].message.content.strip()
        return summary

    # Read the text file
    with open('write.txt', 'r') as file:
        text = file.read()

    # Call the function to generate a summary
    summary = generate_summary(text)

    # Write the summary to the file
    with open('write.txt', 'a') as file:
        file.write(summary)
        print('summary:', summary)

# Create a thread to execute the interview process
interview_thread = threading.Thread(target=process_interview)

# Add a button to start the interview
start_button = tk.Button(root, text="START", command=interview_thread.start)
start_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
