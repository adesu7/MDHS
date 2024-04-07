import streamlit as st

st.title("Dentistry Patient Examination Simulation ")
st.write("This is an experimental teaching tool. It has not been refined in detail and is prone to 'hallucinations' (providing false information). It's designed for fun and your personal interest but should not be treated as a reliable source of information. We're interested in experimenting with first-generation AI-based teaching tools in SSCS. Please note, this demo is designed to process a maximum of 20 interactions. Thank you for your understanding.")

# Wrtie an introduction of the simulation and what students need to do
st.write("You will consult Alena, a 41-year-old patient, who visits the Royal Melbourne Dental Hospital for a check-up. She has rescheduled her appointment due to concerns about pain. You may consult your supervisor for advice.")

# Explain the view of the page so that students know where to navigate to
st.write("You can navigate to the following pages: ")
st.write("- Patient's chat")
st.write("- Supervisor's chat")

st.write("At the end of each conversation save the chat history and end the conversation so it can be assessed.")

# # Take student details
# st.write("Please enter your details below: ")
# student_id = st.text_input("Student ID: ",)
# email = st.text_input("Email: ")
# subject = st.text_input("Subject: ")

# #Share above variables with other pages
# st.session_state["student_id"] = student_id
# st.session_state["email"] = email
# st.session_state["subject"] = subject

# # Add a form submission button to accept the above details
# if st.button("Submit"):
#     st.write("Thank you for submitting your details. Please navigate to the patient's chat page to begin the simulation.")
#     st.session_state["submitted"] = True
# else:
#     st.write("Please submit your details to begin the simulation.")
st.session_state["student_details_submitted"] = False
# if not st.session_state.student_details_submitted:
#     student_details_form = st.form(key="student_details_form")
#     # allow only numbers in student id
#     st.session_state["student_id"] = student_details_form.number_input("Student ID: ", value=None, step=1, format="%i")
#     st.session_state["subject"] = student_details_form.text_input("Subject Code: ")
#     submit_button = student_details_form.form_submit_button("Submit")

#     if submit_button:
#         st.session_state["student_details_submitted"] = True
#         student_details_form.empty()  # Clear the form after submission
#         st.write("Thank you for submitting your details. Please navigate to the patient's chat page to begin the simulation.")
# elif st.session_state["student_details_submitted"]:
#     st.write("Thank you for submitting your details. Please navigate to the patient's chat page to begin the simulation.")

# placeholder_form = st.empty()

# if not st.session_state["student_details_submitted"]:
#     with placeholder_form.form("Student Details"):
#         # allow only numbers in student id
#         st.session_state["student_id"] = st.number_input("Student ID: ", value=None, step=1, format="%i")
#         st.session_state["subject"] = st.text_input("Subject Code: ")
#         submit_button = st.form_submit_button("Submit")
#         if submit_button:
#             if st.session_state["student_id"] is None:
#                 st.error("A valid Student ID must be filled.")    
#             elif st.session_state["subject"] == "":
#                 st.error("A valid Subject Code must be filled.")
#             elif st.session_state["student_id"] is None and st.session_state["subject"] == "":
#                 st.error("Both Student ID and Subject Code must be filled.")

#             else:
#                 st.session_state["student_details_submitted"] = True
#                 st.write("Thank you for submitting your details. Please navigate to the patient's chat page to begin the simulation.")
#                 placeholder_form.empty()
        
#         # st.write("Thank you for submitting your details. Please navigate to the patient's chat page to begin the simulation.")
# if st.session_state["student_details_submitted"]:
#     st.write("Your student ID is ", st.session_state["student_id"])
#     st.write("Thank you for submitting your details. Please navigate to the patient's chat page to begin the simulation.")

