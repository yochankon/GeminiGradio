import gradio as gr
import google.generativeai as genai
import PIL
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()  ## load all the environment variables
# Replace with your API key
# genai.configure(api_key='Enter your authentification tokens')
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

GOOGLE_API_KEY = 'AIzaSyBmccPBmZavxweXuiRI1E4tICHsJzFMX9I'

genai.configure(api_key=GOOGLE_API_KEY)

history = []


## Function to retrieve query from the sql database

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    # for row in rows:
    #     print(row)

    return rows


# Define Your Prompt

prompt = [
    """
    You are an expert in converting English question to SQL query!
    The SQL database has the name STUDENT ans has the following columns - NAME, CLASS, SECTION and MARKS \n\n
    For Example, \nExample 1 - How many entries of records are present in the SQL command will be something this
    SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying  in Data Science class?,
    the SQL command will be something like this SELECT * FROM STUDENT where CLASS = "DATA Science";
    also the sql code should not have this ``` in beginning or at the end, sql word should not be in output and Just give sql command for the given question.
"""
]

def get_gemini_response(text, prompt):
    # global history
    model = genai.GenerativeModel('gemini-pro')
    # history.append(("User", text))
    response = model.generate_content([text,prompt])
    # history.append(("Bot", response.text))
    return response.text
    # return response.text,history


def generate_text(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(text)
    return response.text

def generate_text_from_image(image, text):
    global history
    model = genai.GenerativeModel('gemini-pro-vision')
    image = PIL.Image.fromarray(image.astype('uint8'), 'RGB')
    history.append(("User", text))
    response = model.generate_content([text, image])
    history.append(("Bot", response.text))
    return response.text, history

def interactive_chat(message, chat_history=None):
    if chat_history is None:
        chat_history = []
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat()
    response = chat.send_message(message)
    chat_history.append(("User", message))
    chat_history.append(("Bot", response.text))
    return chat_history


def greet(name):
    return "Hello " + name + "!"

with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Output Box")
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=greet, inputs=name, outputs=output)

# Using the specified Gradio theme
theme =theme = gr.themes.Soft()

# Creating interfaces with the specified theme
text_interface = gr.Interface(
    # fn=generate_text,
    fn= get_gemini_response,
    inputs=[gr.components.Textbox(label="Enter text"),gr.components.Textbox(visible=False)],
    outputs=gr.components.Textbox(label="Generated Text"),

    theme=theme
)


image_interface = gr.Interface(
    fn=generate_text_from_image,
    inputs=[gr.components.Image(label="Upload Image"), gr.components.Textbox(label="Enter text")],
    outputs=[gr.components.Textbox(label="Generated Text"), gr.components.Textbox(label="Chat History", type="text")],
    theme=theme
)

chat_interface = gr.Interface(
    fn=interactive_chat,
    inputs=gr.components.Textbox(label="Chat with the bot"),
    outputs=gr.components.Chatbot(label="Chatbot Response"),
    theme=theme
)

# Launching all interfaces together in a tabbed view
iface = gr.TabbedInterface(
    [text_interface, image_interface, chat_interface],
    tab_names=["Text", "Image", "Chat"],
    theme=theme
)




iface.launch(share=True,server_port=7865) # you can change this parametres

