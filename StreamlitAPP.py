import os
import json
import pandas as pd
import traceback
from src.mcqgenerator.utils import read_file
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain




from src.mcqgenerator.logger import logging

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

with open(r"D:\mcqgen\Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)


#creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Uplaod a PDF or txt file")

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)

    #Subject
    subject=st.text_input("Insert Subject",max_chars=20)

    # Quiz Tone
    tone=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    #Add Button
    button=st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                #Count tokens and the cost of API call
                response=generate_evaluate_chain(
                    {
                    "text": text,
                    "number": mcq_count,
                    "subject":subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                        }
                )
                #st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                if isinstance(response, dict):
                    #Extract the quiz data from the response
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        st.write(response)