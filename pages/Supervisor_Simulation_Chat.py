from openai import OpenAI
import os
import json
import dotenv
import streamlit as st
from pymongo import MongoClient
import datetime
import re 
# Load environment variables
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]   
client = OpenAI(api_key=OPENAI_API_KEY)
mongo_db_username = st.secrets["MONGO_DB_USERNAME"]
mongo_db_password = st.secrets["MONGO_DB_PASSWORD"]
mongo_db_cluster = st.secrets["MONGO_DB_CLUSTER"]
uri = f"mongodb+srv://{mongo_db_username}:{mongo_db_password}@{mongo_db_cluster}.djm2won.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
def init_connection():
    return MongoClient(uri)

st.title("Dentistry Simulation - Supervisor")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "This is an experimental teaching tool. It has not been refined in detail and is prone to 'hallucinations' (providing false information). It's designed for fun and your personal interest but should not be treated as a reliable source of information. We're interested in experimenting with first-generation AI-based teaching tools in SSCS. Please note, this demo is designed to process a maximum of 20 interactions. Thank you for your understanding."
    )

# if not st.session_state["student_details_submitted"]:

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4"

    if "supervisor_messages" not in st.session_state:
        st.session_state["supervisor_messages"] = [{"role": "assistant", "content": "Hi, I'm a clinical supervisor with over 20 years of experience in general clinical practice. I can provide some insight into what tests that the patients may require to investigate some of the issues they are having."}]

    for message in st.session_state["supervisor_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Ask the supervisor questions"):
        st.session_state["supervisor_messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt, unsafe_allow_html=True)
        

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                temperature=0.1,
                messages=[
                    {"role": "system", "content":f""" You will role play as a clinical supervisor, you are a dentist with over 20 years of experience in general clinical
                                practice. You will be interacting with students who are trying to diagnose patients. Your role is to prompt the student to provide a summary of the key points from
                                the history and provide some insight into what tests they think the patients require to
                                investigate some of the issues they are having. 
                    
                                You will query why the student is/has selected certain diagnostic tests and prompt the student to outline their rationale for each,
                                to provide an interpretation of any of the tests that they have viewed. You will ask the student to provide a presumptive or provisional diagnosis or ask them if and why they need
                                additional tests. You may also prompt the student with what are the management considerations for the patient on completion of said tests. They will prompt students to ask
                                if any additional diagnostic tests not on the list that they would like to request.
                    
                                To identify missing information from the history, they will need to know the patient's
                                background but be constrained not to reveal this to the student and only use it to provide
                                feedback and suggestions.
                    
                                Diagnostic Tests Available
                                - Bitewing Radiographs
                                - Periapical Radiographs
                                - OPG Assessment
                                - Limited Oral Examination
                                - Comprehensive Oral Examination
                                - Limited Extra Oral Examination
                                - Clinical Periodontal Analysis
                                - Percussion testing
                                - CO2 tests
                                    -- Lower Right
                                    -- Lower Left
                                    -- Upper Right
                                    -- Upper Left
                                - Heat Test
                                - Bite Test
                                - Triplex Spray 12
                                If the students request for the following tests, you can provide them access to results, just provide the links for the corresponding tests, they need to specifically ask for the results.
                                
                                >> OPG or OPT Assessment - {st.secrets["OPG_Assessment"]}
                                >> Periapical Radiographs - {st.secrets["Periapical_Radiographs"]}
                                >> Bitewing radiographs Tests Right Hand side - {st.secrets["Bitewing_radiographs_Tests_Right_Hand_side"]}
                                >> Bitewing radiographs Tests Left Hand side - {st.secrets["Bitewing_radiographs_Tests_Left_Hand_side"]}
                                >> Cold Test Right or Tooth 12 - {st.secrets["Cold_Test_Right_Tooth_12"]}
                                >> Cold Test Left 1 - {st.secrets["Cold_Test_Left_1"]}
                                >> Cold Test Left 2 - {st.secrets["Cold_Test_Left_2"]}
                                >> OPG Radiology Report - {st.secrets["OPG_Radiology"]}
                                >> Soft Tissue Examination - {st.secrets["Soft_Tissue_Buccal_Mucosa"]}
                                >> Hard Tissue Examination - {st.secrets["Hard_Tissue_Anterior"]} {st.secrets["Hard_Tissue_Bucal_Left"]}, {st.secrets["Hard_Tissue_Bucal_Right"]}, {st.secrets["Hard_Tissue_Lower_Occlusal"]}, {st.secrets["Hard_Tissue_Upper_Occlusal"]}
                                >> Percussion or TTP Test Left Hand side - {st.secrets["Percussion_LHS"]}
                                >> Medical History - {st.secrets["Medical_History"]}
                                >> Superbowl https://www.youtube.com/watch?v=8OokHde8URc

                    Return the link to results so it can be clicked on and also in a new line embedd the link in markdown format to display the image or video in the chat.
                    here is an example of how to embed the link in markdown format wihin the width of 700px:
                    <img src="https://www.example.com/image.jpg" width="700">

                    if the link does not contain png or jpg, then embed the link in iframe format to render the video or pdf in the chat:
                    ![Alt text] [Width: 700px](https://www.example.com/image.jpg)
                   

    """}]+[

                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.supervisor_messages
                    ],
                    stream=True,
                ):
                if response.choices[0].delta.content is not None:
                    full_response += response.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌ ", unsafe_allow_html=True)

            # if 'https' in full_response:
            #     url = re.search(r'https://[^\s]*', full_response).group(0)
            #     # Check if the url is a video if mp4 is in the url
            #     if 'mp4' in url:
            #         #st.video(url, format="video/mp4")
            #         pass
            #     elif 'pdf' in url:
            #         pass
            #     else:
            #         # Continue to display the image in the chat
            #         st.image(url, width=700)
            # else:
            #     message_placeholder.markdown(full_response + "▌ ")

            message_placeholder.markdown(full_response, unsafe_allow_html=True)
            
        st.session_state["supervisor_messages"].append(
            {"role": "assistant", "content": full_response}
        )
        
    # Add a button to save the chat history and trigger sending to MongoDB
    if "save_chat_history_supervisor" not in st.session_state:
        st.session_state["save_chat_history_supervisor"] = False

    if st.button("Save chat history"):
        st.session_state["save_chat_history_supervisor"] = True
        st.chat_input(disabled=True)

        # Save the chat history
        with open("chat_history.json", "w") as f:
            json.dump(st.session_state["supervisor_messages"], f)

        # Allow the user to download the chat history
        st.download_button(
            label="Download chat history",
            data=json.dumps(st.session_state["supervisor_messages"]),
            file_name="chat_history.json",
            mime="application/json",
        )


        with init_connection() as st.session_state.superviser_client:
            db = st.session_state.superviser_client["chat_history"]
            collection = db["supervisor"]
            collection.insert_one({"history": st.session_state["supervisor_messages"], "student_id": st.session_state["student_id"], "subject": st.session_state["subject"], "time_submitted": datetime.datetime.now()})
            
        
        # Close the MongoDB connection
        st.session_state.superviser_client.close()

        # Disable the option to chat again
        st.session_state["save_chat_history_supervisor"] = False
        st.session_state["supervisor_messages"] = []


# else:
#     st.write("Please submit your details to begin the simulation.")