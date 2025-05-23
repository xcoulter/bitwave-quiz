# Bitwave Certification Quiz App - Streamlit Version

# This Python script builds an interactive quiz application using Streamlit. It includes:
# - 60-question multiple-choice quiz
# - 90-minute total timer for the quiz
# - Scoring logic
# - User result tracking

import streamlit as st
import time

# ========== 1. Define the Quiz Data ==========
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
    },
    {
        "question": "[SINGLE] Where does Bitwave sit in the following process?",
        "options": [
            "ERP --> Blockchain --> Bitwave",
            "Blockchain --> ERP --> Bitwave",
            "ERP --> Bitwave --> Blockchain",
            "Blockchain --> Bitwave --> ERP"
        ],
        "correct": [3],
        "type": "single"
    },
    # ... [PLACEHOLDER: All remaining 57 questions would go here, following the same format] ...
]

# ========== 2. App Initialization ==========
st.set_page_config(page_title="Bitwave Basics Certification Quiz", layout="wide")
st.title("🧠 Bitwave Basics Certification Quiz")

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.responses = [{} for _ in quiz_data]
    st.session_state.submitted = False

# ========== 3. Timer Display ==========
total_quiz_duration = 90 * 60  # 90 minutes in seconds
elapsed = time.time() - st.session_state.start_time
remaining = int(total_quiz_duration - elapsed)

if remaining <= 0:
    st.warning("⏰ Time's up! Auto-submitting your responses.")
    st.session_state.submitted = True

st.sidebar.write(f"🕒 Time Remaining: {remaining // 60} minutes {remaining % 60} seconds")

# ========== 4. Full Quiz Display ==========
st.write("Please answer all questions below. Use checkboxes for multiple choice.")

for i, q in enumerate(quiz_data):
    st.markdown(f"### Q{i + 1}: {q['question']}")
    user_answers = []
    for j, option in enumerate(q["options"]):
        key = f"q{i}_opt{j}"
        if st.checkbox(option, key=key):
            user_answers.append(j)
    st.session_state.responses[i] = user_answers

# ========== 5. Submit and Scoring ==========
if not st.session_state.submitted:
    if st.button("Submit Quiz"):
        st.session_state.submitted = True

if st.session_state.submitted:
    score = 0
    results = []
    for i, q in enumerate(quiz_data):
        correct = sorted(q["correct"])
        given = sorted(st.session_state.responses[i])
        is_correct = (given == correct)
        if is_correct:
            score += 1
        results.append((i + 1, is_correct, [q["options"][x] for x in given]))

    st.success("✅ Quiz complete!")
    st.write(f"Your Score: **{score} / {len(quiz_data)}**")

    st.write("### Summary")
    for qnum, correct, answers in results:
        status = "✅" if correct else "❌"
        st.write(f"Q{qnum}: {status} - Your answer: {answers}")

    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
