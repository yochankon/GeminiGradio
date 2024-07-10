import gradio as gr
import os
from dotenv import load_dotenv
import google.generativeai as genai
import random
import time

load_dotenv()

# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')


chat = model.start_chat(history=[])

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])


    def respond(msg, chat_history):
        user_message = msg
        bot_message = chat.send_message(user_message)
        print(type(bot_message))
        chat_history.append((user_message, bot_message.text))
        time.sleep(2)
        return "", chat_history


    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch(share=True)