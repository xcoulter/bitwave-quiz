# Bitwave Certification Quiz App - Streamlit Version

import streamlit as st
import json
from datetime import datetime
import re
import csv
import os
import time
from streamlit_autorefresh import st_autorefresh

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

# Function to generate CSV results
def generate_results_csv(user_info, answers, quiz_data):
    results = []
    results.append(["Question Number", "Question", "Your Answer", "Correct Answer", "Result"])
    
    for i, question in enumerate(quiz_data):
        user_answer = answers[i]
        correct_answer = question['options'][question['correct'][0]] if question['type'] == "single" else [question['options'][idx] for idx in question['correct']]
        
        if question['type'] == "single":
            result = "Correct" if user_answer == correct_answer else "Incorrect"
        else:
            result = "Correct" if set(user_answer) == set(correct_answer) else "Incorrect"
        
        results.append([
            i + 1,
            question['question'],
            ", ".join(user_answer) if isinstance(user_answer, list) else user_answer,
            ", ".join(correct_answer) if isinstance(correct_answer, list) else correct_answer,
            result
        ])
    
    # Add user info
    results.insert(1, ["User Information", "", "", "", ""])
    results.insert(2, ["Name", user_info['name'], "", "", ""])
    results.insert(3, ["Email", user_info['email'], "", "", ""])
    results.insert(4, ["Company", user_info['company'], "", "", ""])
    results.insert(5, ["", "", "", "", ""])
    
    # Create CSV file
    csv_filename = f"quiz_results_{user_info['email'].replace('@', '_')}.csv"
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)
    
    return csv_filename

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
        'show_confirmation': False,
        'start_time': None,
        'quiz_time_limit': 3600,  # 1 hour in seconds
        'time_remaining': 3600
    }

# Page configuration
st.set_page_config(
    page_title="Bitwave Certification Quiz",
    layout="wide"
)

# Main app
st.title("Bitwave Certification Quiz")

# Timer display
if st.session_state.quiz_state['started']:
    if st.session_state.quiz_state['start_time'] is None:
        st.session_state.quiz_state['start_time'] = time.time()
    
    elapsed_time = time.time() - st.session_state.quiz_state['start_time']
    st.session_state.quiz_state['time_remaining'] = max(0, st.session_state.quiz_state['quiz_time_limit'] - elapsed_time)
    
    # Convert to minutes and seconds
    minutes = int(st.session_state.quiz_state['time_remaining'] // 60)
    seconds = int(st.session_state.quiz_state['time_remaining'] % 60)
    
    st.sidebar.write("Time Remaining:")
    st.sidebar.write(f"{minutes:02d}:{seconds:02d}")
    
    # Auto-submit if time runs out
    if st.session_state.quiz_state['time_remaining'] <= 0:
        st.session_state.quiz_state['completed'] = True

# Quiz questions section
elif not st.session_state.quiz_state['completed']:
    current_question = st.session_state.quiz_state['current_question']
    
    # Ensure we have valid quiz data
    if quiz_data and current_question < len(quiz_data):
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
        
        # Next button or Submit button based on current question
        if current_question == len(quiz_data) - 1:
            if st.button("Submit Quiz"):
                st.session_state.quiz_state['answers'].append(answer)
                st.session_state.quiz_state['completed'] = True
                st.rerun()
        else:
            if st.button("Next Question"):
                st.session_state.quiz_state['answers'].append(answer)
                st.session_state.quiz_state['current_question'] += 1
                st.rerun()
    else:
        st.error("No questions available or quiz is complete")
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
            if user_answer == question['options'][question['correct'][0]]:
                correct_answers += 1
        else:  # multi-select
            correct_indices = set(question['correct'])
            user_indices = {question['options'].index(a) for a in user_answer}
            if correct_indices == user_indices:
                correct_answers += 1
    
    score = (correct_answers / len(quiz_data)) * 100
    st.write(f"Your score: {score:.1f}%")
    
    # Add CSV download button
    if st.button("Download Quiz Results"):
        csv_filename = generate_results_csv(
            st.session_state.quiz_state['user_info'],
            st.session_state.quiz_state['answers'],
            quiz_data
        )
        with open(csv_filename, 'rb') as f:
            st.download_button(
                label="Download Results",
                data=f,
                file_name=csv_filename,
                mime="text/csv"
            )
    elapsed_time = time.time() - st.session_state.quiz_state['start_time']
    st.session_state.quiz_state['time_remaining'] = max(0, st.session_state.quiz_state['quiz_time_limit'] - elapsed_time)
    
    # Convert to minutes and seconds
    minutes = int(st.session_state.quiz_state['time_remaining'] // 60)
    seconds = int(st.session_state.quiz_state['time_remaining'] % 60)
    
    st.sidebar.write("Time Remaining:")
    st.sidebar.write(f"{minutes:02d}:{seconds:02d}")
    
    # Auto-submit if time runs out
    if st.session_state.quiz_state['time_remaining'] <= 0:
        st.session_state.quiz_state['completed'] = True

# User info collection section
if not st.session_state.quiz_state['started']:
    st.write("Welcome to the Bitwave Certification Quiz!")
    
    # Collect user information
    with st.form("user_info_form"):
        st.subheader("Please provide your information:")
        
        name = st.text_input("Full Name", key="name_input")
        email = st.text_input("Email Address", key="email_input")
        company = st.text_input("Company Name", key="company_input")
        
        if st.form_submit_button("Submit Information"):
            # Get the values from the form
            name = st.session_state.get("name_input", "")
            email = st.session_state.get("email_input", "")
            company = st.session_state.get("company_input", "")
            
            # Validate all fields are filled
            if not (name and email and company):
                st.error("Please fill in all fields")
                st.stop()
            
            # Validate email format
            if not re.match(EMAIL_REGEX, email):
                st.error("Please enter a valid email address")
                st.stop()
            
            # Check attempts
            can_attempt, message = check_attempts(email)
            if not can_attempt:
                st.error(message)
                st.stop()
            
            # Update session state and show confirmation
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
