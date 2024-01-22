from openai import OpenAI
import os
import json
import dotenv
import streamlit as st
from pymongo import MongoClient
import datetime

# Load environment variables
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]   
client = OpenAI(api_key=OPENAI_API_KEY)
mongo_db_username = st.secrets["MONGO_DB_USERNAME"]
mongo_db_password = st.secrets["MONGO_DB_PASSWORD"]
mongo_db_cluster = st.secrets["MONGO_DB_CLUSTER"]
uri = f"mongodb+srv://{mongo_db_username}:{mongo_db_password}@{mongo_db_cluster}.djm2won.mongodb.net/?retryWrites=true&w=majority"


# Connect to MongoDB
# @st.cache_resource
def init_connection():
    return MongoClient(uri)

st.title("Dentistry Simulation - Patient")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "This is an experimental teaching tool. It has not been refined in detail and is prone to 'hallucinations' (providing false information). It's designed for fun and your personal interest but should not be treated as a reliable source of information. We're interested in experimenting with first-generation AI-based teaching tools in SSCS. Please note, this demo is designed to process a maximum of 20 interactions. Thank you for your understanding."
    )

if st.session_state["student_details_submitted"]:

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4"

    if "patient_messages" not in st.session_state:
        st.session_state["patient_messages"] = [{"role": "assistant", "content": "Hi, I'm Alena, a 41-year-old patient. I'm here for a check-up with a student practitioner."}]

    for message in st.session_state["patient_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask the patient questions"):
        st.session_state["patient_messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
        

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                temperature=0.1,
                messages=[
                    {"role": "system", "content":f""" You will role-play as Alena, a 41-year-old patient, who visits the Royal Melbourne Dental Hospital for a check-up with a student practitioner. 
                    
                    You have rescheduled her appointment due to concerns about pain.

                        Background:
                        - You have allergies to penicillin, anxiety, and acid reflux.
                        - You take Lexapro for anxiety and Nexium for reflux.
                        - Past allergic reactions to penicillin include facial swelling and breathing difficulties.
                        - Dental history includes braces, a frenectomy, regular scale and cleans, and tooth clenching.
                        - Current issues: Neurological pain on the left side of her face and dental hypersensitivity on the upper right lateral incisor.

                        Pain Descriptions:
                        1. Neurological Pain (left side): Sudden onset two weeks ago, feels cold, prickly, reduced sensation, constant, alleviated slightly with heat.
                        2. Dental Hypersensitivity (right side): Over a year, sharp pain to cold stimuli, pain ceases after stimulus removal.

                        Constraints:
                        - Do not reveal the specific diagnoses (neurological pain related to demyelination, dental hypersensitivity) to the student describe the pain as you are not aware of medical terminologies.
                        - Respond to closed questions (e.g., "Did your pain start a week ago?") with yes/no answers.
                        - Provide detailed responses to open-ended questions (e.g., "Tell me about when your pain started").

                        Objective: Guide student practitioners to ask insightful questions to uncover your symptoms and condition, aiding their skill development in patient history taking and diagnosis in a dental context.
                        Do not ask how can I assist you as you are a patient who has come for a check up."""}]+[

                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.patient_messages
                    ],
                    stream=True,
                ):
                if response.choices[0].delta.content is not None:
                    full_response += response.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌ ")
            message_placeholder.markdown(full_response)
            
        st.session_state["patient_messages"].append(
            {"role": "assistant", "content": full_response}
        )
        
    # Add a button to save the chat history and trigger sending to MongoDB
    if "save_chat_history_patient" not in st.session_state:
        st.session_state["save_chat_history_patient"] = False

    if st.button("Save chat history"):
        st.session_state["save_chat_history_patient"] = True
        st.chat_input(disabled=True)

    # if st.session_state["save_chat_history_patient"]:
        # Change assistant tag in chat history to patient
        for message in st.session_state["patient_messages"]:
            if message["role"] == "assistant":
                message["role"] = "patient"
        # Save the chat history
        with open("chat_history.json", "w") as f:
            json.dump(st.session_state["patient_messages"], f)

        # Allow the user to download the chat history
        st.download_button(
            label="Download chat history",
            data=json.dumps(st.session_state["patient_messages"]),
            file_name="chat_history.json",
            mime="application/json",
        )

        # Save the chat history to MongoDB
        with init_connection() as db_client:
            db = db_client["chat_history"]
            collection = db["patient"]
            collection.insert_one({"student_id": st.session_state["student_id"], "history": st.session_state["patient_messages"], "subject": st.session_state["subject"], "time_submitted": datetime.datetime.now()})
            # init_connection.clear()

        # Close the MongoDB connection
        db_client.close()

        # Disable the option to chat again
        st.session_state["save_chat_history_patient"] = False
        st.session_state["patient_messages"] = []


        
else:
    st.write("Please submit your details to begin the simulation.")