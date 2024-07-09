from dotenv import load_dotenv

load_dotenv()  ## load all the environment variables

import streamlit as st  # type: ignore
import os
import sqlite3

import google.generativeai as genai  # type: ignore

## Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Function to Load Google Gemini MODel and provide sql query as responce

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text


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

## Streamlit APP

st.set_page_config(page_title='I can Retrieve Any SQL query')
st.header("Gemini App to Retrieve SQL Data")

question = st.text_input('Input: ', key='input')

submit = st.button("Ask the Question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt[0])

    st.subheader('The Query is')
    print((response))
    st.code(response)

    data = read_sql_query(response, "student.db")

    st.subheader('The Response is')

    for row in data:

        if len(row) > 1:
            output = ''
            for i in row:
                output += str(i) + ' '
            print(output)
            st.text(output)
        else:
            print(row[0])
            st.text(row[0])
