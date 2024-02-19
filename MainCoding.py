import tkinter as tk
import threading
import speech_recognition as sr
from openai import OpenAI
from gtts import gTTS
import os

# 创建一个 Recognizer 对象
recognizer = sr.Recognizer()

# 初始化 OpenAI 客户端
client = OpenAI(api_key='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')

# 定义问题列表
questions = [
    'How long did it take you to complete this coding task (in months)?',
'Can you outline the timeline of your work on this coding task? How much time was allocated to each sub-task?',
'What were the main challenges you encountered for the coding task, and what lessons did you learn from them?',
'How did you ensure the usability and aesthetic appeal of your application interface Can you share your design and implementation strategies?',
'What steps did you take to maintain professional code quality and application appearance?',
'Reflecting on your experience with this coding task, what are three key takeaways you would like to emphasize?',
'What aspects of the coding task do you believe you handled well, and what tips can you offer based on your experience?',
]

# 创建主窗口
root = tk.Tk()
root.title("Interview Information")

# 创建文本窗口以显示信息
info_text = tk.Text(root, height=50, width=200)
info_text.pack(padx=15, pady=15)

# 打开文件以写入问题和生成的回答
def process_interview():
    with open('write.txt', 'w') as file:
        # 添加问题到文本窗口和文件中
        for question in questions:
            info_text.insert(tk.END, question + '\n')
            file.write(question + '\n')

            # 使用麦克风捕获音频
            with sr.Microphone() as source:
                tts = gTTS(text=question, lang='en')
                tts.save("question.mp3")

                # 播放生成的语音文件
                os.system("afplay question.mp3")  # 适用于 macOS
                info_text.insert(tk.END, "Please speak...\n")
                file.write("Please speak...\n")

                try:
                    # 连续录音，直到检测到静默
                    audio = recognizer.listen(source, timeout=10)  # 设置 timeout 参数为 5 秒
                    info_text.insert(tk.END, "Processing...\n")
                    file.write("Processing...\n")

                    text = recognizer.recognize_google(audio, language='en-US')  # 识别音频
                    info_text.insert(tk.END, "You said: " + text + '\n')
                    file.write("You said: " + text + '\n')

                    # 使用 OpenAI GPT-3.5 模型生成响应
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system",
                             "content": "You are a interview assistant, you can choose deepen question based on user's answer or make a summary，when using gpt-3.5-turbo-instruct only make summary ."},
                            {"role": "user", "content": text}
                        ]
                    )
                    generated_response = completion.choices[0].message
                    info_text.insert(tk.END, "Generated response: " + generated_response.content + '\n')
                    file.write("Generated response: " + generated_response.content + '\n')

                    tts = gTTS(text=generated_response.content, lang='en')
                    tts.save("response.mp3")

                    # 播放生成的语音文件
                    os.system("afplay response.mp3")  # 适用于 macOS
                    info_text.insert(tk.END, "Speak now...\n")
                    file.write("Speak now...\n")

                    audio_additional_info = recognizer.listen(source, timeout=5)  # 捕获额外信息的语音输入
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
    # 生成摘要
    def generate_summary(text):
        # 使用 OpenAI GPT-3.5 模型生成摘要总结
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a summarizer,summarize the full text ."},
                {"role": "user", "content": text}
            ]
        )
        summary = completion.choices[0].message.content.strip()
        return summary


    # 读取文本文件
    with open('write.txt', 'r') as file:
        text = file.read()

    # 调用生成摘要函数
    summary = generate_summary(text)

    # 将摘要写入文件
    with open('write.txt', 'a') as file:
        file.write(summary)
        print('summary:', summary)
# 创建一个线程来执行面试过程
interview_thread = threading.Thread(target=process_interview)

# 添加按钮以开始面试
start_button = tk.Button(root, text="START", command=interview_thread.start)
start_button.pack(pady=5)

# 运行Tkinter事件循环
root.mainloop()


