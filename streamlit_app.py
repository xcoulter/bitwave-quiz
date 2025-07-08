# Bitwave Certification Quiz App - Streamlit Version

import streamlit as st
import json
from datetime import datetime
import re
import csv
import os

# Email validation regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Quiz data structure
quiz_data = [
    {
        "question": "[MULTI] What are the primary use cases of Bitwave?",
        "options": [
            "Crypto accounting",
            "Crypto tax and Compliance",
            "Treasury Management",
            "Crypto Invoicing & Payments",
            "Wallet Management & Monitoring"
        ],
        "correct": [0, 1, 2, 3, 4],
        "type": "multi"
    },
    {
        "question": "[SINGLE] Which of the following best describes how Bitwave functions as a bookkeepers tool?",
        "options": [
            "a 'set-it and forget-it' accounting software that will automatically categorise and produce reports",
            "a crypto exchange",
            "a software that submits your crypto taxes for you",
            "a bridge between blockchain activity and your general ledger"
        ],
        "correct": [3],
        "type": "single"
    }
    # Add more questions as needed
]

# Function to check attempts
def check_attempts(email):
    attempts_file = "attempts_log.csv"
    max_attempts = 3
    
    # Create attempts file if it doesn't exist
    if not os.path.exists(attempts_file):
        with open(attempts_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["email", "attempts", "last_attempt"])
    
    # Check attempts
    with open(attempts_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == email:
                attempts = int(row[1])
                if attempts >= max_attempts:
                    return False, f"You have exceeded the maximum number of attempts ({max_attempts}). Please contact support@bitwave.io for assistance."
                return True, f"You have {max_attempts - attempts} attempts remaining."
    
    return True, "You have 3 attempts remaining."

# Function to update attempts
def update_attempts(email):
    attempts_file = "attempts_log.csv"
    attempts = 1
    
    # Read existing attempts
    attempts_data = []
    if os.path.exists(attempts_file):
        with open(attempts_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            attempts_data = list(reader)
    
    # Update or add new entry
    found = False
    for i, row in enumerate(attempts_data):
        if row[0] == email:
            attempts = int(row[1]) + 1
            attempts_data[i] = [email, str(attempts), datetime.now().isoformat()]
            found = True
            break
    
    if not found:
        attempts_data.append([email, "1", datetime.now().isoformat()])
    
    # Write back to file
    with open(attempts_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["email", "attempts", "last_attempt"])
        writer.writerows(attempts_data)

# Initialize session state
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = {
        'current_question': 0,
        'answers': [],
        'started': False,
        'completed': False,
        'user_info': {
            'name': '',
            'email': '',
            'company': ''
        },
        'show_confirmation': False
    }

# Page configuration
st.set_page_config(
    page_title="Bitwave Certification Quiz",
    layout="wide"
)

# Main app
st.title("Bitwave Certification Quiz")

# User info collection section
if not st.session_state.quiz_state['started']:
    st.write("Welcome to the Bitwave Certification Quiz!")
    
    # Collect user information
    with st.form("user_info_form"):
        st.subheader("Please provide your information:")
        
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        company = st.text_input("Company Name")
        
        if st.form_submit_button("Submit Information"):
            # Validate all fields are filled
            if not (name and email and company):
                st.error("Please fill in all fields")
            # Validate email format
            elif not re.match(EMAIL_REGEX, email):
                st.error("Please enter a valid email address")
            else:
                # Check attempts
                can_attempt, message = check_attempts(email)
                if not can_attempt:
                    st.error(message)
                else:
                    st.session_state.quiz_state['user_info'] = {
                        'name': name,
                        'email': email,
                        'company': company
                    }
                    st.session_state.quiz_state['show_confirmation'] = True
                    st.rerun()
    
    # Confirmation dialog
    if st.session_state.quiz_state['show_confirmation']:
        with st.form("start_quiz_form"):
            st.subheader("Quiz Information")
            st.write(f"Name: {st.session_state.quiz_state['user_info']['name']}")
            st.write(f"Email: {st.session_state.quiz_state['user_info']['email']}")
            st.write(f"Company: {st.session_state.quiz_state['user_info']['company']}")
            
            if st.form_submit_button("Start Quiz"):
                # Update attempts when starting quiz
                update_attempts(st.session_state.quiz_state['user_info']['email'])
                st.session_state.quiz_state['started'] = True
                st.session_state.quiz_state['show_confirmation'] = False
                st.rerun()
            if st.form_submit_button("Edit Information"):
                st.session_state.quiz_state['show_confirmation'] = False
                st.rerun()

# Quiz questions section
elif not st.session_state.quiz_state['completed']:
    current_question = st.session_state.quiz_state['current_question']
    
    # Display current question
    question = quiz_data[current_question]
    st.subheader(f"Question {current_question + 1}")
    st.write(question['question'])
    
    # Display options based on question type
    if question['type'] == "single":
        answer = st.radio(
            "Select your answer",
            question['options'],
            key=f"q{current_question}"
        )
    else:  # multi-select
        answer = st.multiselect(
            "Select all that apply",
            question['options'],
            key=f"q{current_question}"
        )
    
    # Next button
    if st.button("Next"):
        st.session_state.quiz_state['answers'].append(answer)
        st.session_state.quiz_state['current_question'] += 1
        
        # Check if quiz is completed
        if st.session_state.quiz_state['current_question'] >= len(quiz_data):
            st.session_state.quiz_state['completed'] = True
        st.rerun()

# Quiz completion section
else:
    st.success("Quiz Completed!")
    st.write("Thank you for completing the quiz!")
    
    # Calculate and display score
    correct_answers = 0
    for i, question in enumerate(quiz_data):
        user_answer = st.session_state.quiz_state['answers'][i]
        if question['type'] == "single":
