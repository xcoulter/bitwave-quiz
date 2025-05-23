# Bitwave Certification Quiz App - Streamlit Version

This Python script builds an interactive quiz application using Streamlit. It includes:
- 60-question multiple-choice quiz
- 45-second timer per question
- Scoring logic
- User result tracking

```python
import streamlit as st
import time

# ========== 1. Define the Quiz Data ==========
quiz_data = [
    {
        "question": "What are the primary use cases of Bitwave?",
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
        "question": "Which of the following best describes how Bitwave functions as a bookkeepers tool?",
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
        "question": "Where does Bitwave sit in the following process?",
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
st.set_page_config(page_title="Bitwave Basics Certification Quiz", layout="centered")
st.title("🧠 Bitwave Basics Certification Quiz")

if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.responses = []
    st.session_state.index = 0
    st.session_state.start_time = time.time()

# ========== 3. Timer Logic ==========
current_index = st.session_state.index
question_start_time = st.session_state.get("question_start_time", time.time())
elapsed = time.time() - question_start_time
remaining = 45 - int(elapsed)

if remaining <= 0:
    st.warning("⏰ Time's up! Moving to next question.")
    st.session_state.responses.append({"q": current_index, "answer": [], "is_correct": False})
    st.session_state.index += 1
    st.session_state.question_start_time = time.time()
    st.experimental_rerun()

# ========== 4. Question Display ==========
if current_index < len(quiz_data):
    q = quiz_data[current_index]
    st.write(f"**Q{current_index + 1}:** {q['question']}")
    
    selected = st.multiselect("Select answer(s):", q["options"])
    st.write(f"⏳ Time left: {remaining} seconds")

    if st.button("Submit"):
        correct = sorted(q["correct"])
        is_correct = sorted([q["options"].index(opt) for opt in selected]) == correct
        if is_correct:
            st.session_state.score += 1
        st.session_state.responses.append({"q": current_index, "answer": selected, "is_correct": is_correct})
        st.session_state.index += 1
        st.session_state.question_start_time = time.time()
        st.experimental_rerun()
else:
    # ========== 5. Results ==========
    st.success("✅ Quiz complete!")
    st.write(f"Your Score: **{st.session_state.score} / {len(quiz_data)}**")
    st.write("### Summary")
    for r in st.session_state.responses:
        status = "✅" if r["is_correct"] else "❌"
        st.write(f"Q{r['q']+1}: {status} - Your answer: {r['answer']}")

    if st.button("Restart Quiz"):
        for key in ["score", "responses", "index", "question_start_time"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
```
