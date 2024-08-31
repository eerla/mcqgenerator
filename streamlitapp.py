import os
import pandas as pd
import traceback
import json
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

#import required langchain modules
from langchain.callbacks import get_openai_callback

from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.utils import read_file, get_table_data, create_file
from src.mcqgenerator.logger import logging

# load json resonse format
with open("response.json", "r") as jsonfile:
    RESPONSE_JSON=json.load(jsonfile)

st.title("MCQs Generator with LangChain 🦜⛓️")

with st.form("user_inputs"):
    # file uploader
    uploaded_file=st.file_uploader("Upload a PDF or txt file")

    # number of questions input
    mcq_count=st.number_input("No.of MCQs", min_value=3, max_value=50)

    # Set the subject of the input data
    subject = st.text_input("Insert subject", max_chars=20, placeholder="Enter context of the file in one word")
    
    # Set the complexity level
    tone = st.text_input("Desired complexity level", max_chars=20, placeholder="Simple, Medium, Hard")

    # Add submit button
    button=st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                #Count tokens and the cost of API call
                with get_openai_callback() as cb:
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
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    #Extract the quiz data from the response
                    quiz=response.get("quiz", None)
                
                    if quiz is not None:
                        
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            print(df)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in atext box as well
                            # st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")

                else:
                    st.write(response)



@st.fragment()
def download_data():
    try:
        json_str, file_name=create_file(quiz, uploaded_file)
        st.download_button(
            label="Download data as JSON",
            data=json_str,
            file_name=file_name,
            mime='text/json',
        )
    except:
        pass

download_data()