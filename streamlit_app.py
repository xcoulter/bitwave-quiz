# Bitwave Certification Quiz App - Streamlit Version

import streamlit as st
import json
from datetime import datetime

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

# Initialize session state
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = {
        'current_question': 0,
        'answers': [],
        'started': False,
        'completed': False
    }

# Page configuration
st.set_page_config(
    page_title="Bitwave Certification Quiz",
    layout="wide"
)

# Main app
st.title("Bitwave Certification Quiz")

# Quiz start section
if not st.session_state.quiz_state['started']:
    st.write("Welcome to the Bitwave Certification Quiz!")
    if st.button("Start Quiz"):
        st.session_state.quiz_state['started'] = True
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
            if user_answer == question['options'][question['correct'][0]]:
                correct_answers += 1
        else:  # multi-select
            correct_indices = set(question['correct'])
            user_indices = {question['options'].index(a) for a in user_answer}
            if correct_indices == user_indices:
                correct_answers += 1
    
    score = (correct_answers / len(quiz_data)) * 100
    st.write(f"Your score: {score:.1f}%")

# Add timer display
if st.session_state.quiz_state['started']:
    st.sidebar.write("Time elapsed:")
    start_time = st.session_state.quiz_state.get('start_time', datetime.now())
    elapsed_time = datetime.now() - start_time
    st.sidebar.write(f"{elapsed_time.seconds // 60} minutes {elapsed_time.seconds % 60} seconds")
