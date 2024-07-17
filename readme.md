# Dental Simulation Chatbot System

## Overview
This repository contains the code for an innovative dental simulation system comprising two interconnected chatbots designed to enhance dental education. The system simulates a dental consultation scenario with a patient chatbot and a clinical supervisor chatbot, providing an interactive learning environment for dental students.

## Repository Structure
This repository contains two main Python scripts:
1. `patient_chatbot.py`: Implements the patient chatbot simulation
2. `supervisor_chatbot.py`: Implements the clinical supervisor chatbot simulation

## Features
- **Streamlit-based UI**: Both chatbots are implemented using Streamlit for a user-friendly interface.
- **OpenAI GPT Integration**: Utilizes GPT-4 (initially GPT-3.5 Turbo) for generating responses.
- **MongoDB Integration**: Stores chat histories for later analysis.
- **Diagnostic Tests Simulation**: The supervisor chatbot provides access to simulated diagnostic test results.

## Requirements
- Python 3.6+
- Streamlit
- OpenAI Python Client
- PyMongo
- python-dotenv

## Setup and Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dental-simulation-chatbot.git
   cd dental-simulation-chatbot
   ```

2. Install required packages:
   ```
   pip install streamlit openai pymongo python-dotenv
   ```

3. Set up environment variables:
   Create a `.streamlit/secrets.toml` file in the project directory and add the following:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key"
   MONGO_DB_USERNAME = "your_mongodb_username"
   MONGO_DB_PASSWORD = "your_mongodb_password"
   MONGO_DB_CLUSTER = "your_mongodb_cluster"
   ```
   
   Also add any other secret keys used in the code, such as:
   ```toml
   OPG_Assessment = "link_to_opg_assessment"
   Bitewing_radiographs_Tests_Right_Hand_side = "link_to_right_bitewing"
   Bitewing_radiographs_Tests_Left_Hand_side = "link_to_left_bitewing"
   # ... add all other diagnostic test links here
   ```

## Usage
1. Run the command to start the simulation.
   ```
   streamlit run Background.py`
   ```

## Key Components

### Patient Chatbot (`patient_chatbot.py`)
- Simulates a 41-year-old patient named Alena.
- Responds to student inquiries about symptoms and medical history.
- Uses GPT-4 with a temperature setting of 0.1 for slightly varied but consistent responses.

### Supervisor Chatbot (`supervisor_chatbot.py`)
- Represents a dental professional with over 20 years of experience.
- Guides students in diagnosis and provides access to diagnostic test results.
- Uses GPT-4 with a temperature setting of 0 for highly deterministic guidance.
- Includes functionality to embed diagnostic test results (images/videos) in the chat.

## Limitations
- The system is designed to process a maximum of 20 interactions per session.
- Ongoing work is needed to optimize prompts for more realistic patient-like responses.

## Contributing
We welcome contributions to improve this educational tool. Please feel free to submit issues or pull requests.

## Disclaimer
This is an experimental teaching tool and should not be treated as a reliable source of medical or dental information. It is designed for educational purposes only.