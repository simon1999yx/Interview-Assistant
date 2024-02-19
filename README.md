# Interview Assistant

Interview Assistant is a Python application designed to conduct interviews using speech recognition and AI-powered conversation. It allows interviewers to ask questions verbally, record responses, and generate summaries of interview sessions into a local file `write.txt`(Can be shared as a blog).

## Features

- **Speech Recognition**: Utilizes the `speech_recognition` library to transcribe spoken responses from interviewees.
- **OpenAI Integration**: Interacts with the OpenAI API to generate AI-driven responses and summaries using the GPT-3.5 model.
- **Text-to-Speech**: Employs the `gTTS` library to convert text prompts and responses into speech for interviewees.
- **User Interface**: Built using Tkinter, providing a simple graphical interface for conducting interviews and displaying interview information.

## Requirements

- Python 3.x
- `speech_recognition` library
- `openai` library
- `gtts` library
- Tkinter (usually included with Python distributions)

## Usage

1. Install the required libraries using pip:

2. Set up an OpenAI account and obtain an API key.

3. Clone or download the Interview Assistant repository to your local machine.

4. Navigate to the directory containing the code.

5. Run the application by executing the Python script:

6. Click the "START" button to begin the interview process.

7. Speak the interview questions into the microphone and wait for responses from the interviewee.

8. The application will display the interview dialogue and summary in the text window.

9. Once the interview is complete, the summary will be written to the `write.txt` file in the same directory.

## Notes

- Make sure to provide appropriate permissions for microphone access on your system.
- Adjust the OpenAI model and parameters as needed for specific interview requirements.


