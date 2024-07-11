from fastapi import FastAPI
import gradio as gr
import google.generativeai as genai


app = FastAPI()

GOOGLE_API_KEY = 'AIzaSyBmccPBmZavxweXuiRI1E4tICHsJzFMX9I'
genai.configure(api_key=GOOGLE_API_KEY)




# def read_main():
#     return {"message": "This is your main app"}
#
# io = gr.Interface(lambda x: "Hello, " + x + "!", "textbox", "textbox")
# gr.mount_gradio_app(app, io, path="/gradio")
#
# # Then run `uvicorn run:app` from the terminal and navigate to http://localhost:8000/gradio.
#
#
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

@app.get("/")

def get_gemini_response(text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    # model = genai.GenerativeModel('gemini-1.0-pro-latest')

    response = model.generate_content([text, prompt])
    # print(response.text)
    return response.text



# Using the specified Gradio theme
theme = theme = gr.themes.Soft()

text_interface = gr.Interface(
    # fn=generate_text,
    fn=get_gemini_response,
    inputs=[gr.components.Textbox(label="Enter text"), gr.components.Textbox(visible=False)],
    outputs=gr.components.Textbox(label="Generated Sql"),
    theme=theme
)

gr.mount_gradio_app(app, text_interface, path="/gradio")