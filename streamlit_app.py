# Bitwave Certification Quiz App - Streamlit Version

import streamlit as st
import time
from fpdf import FPDF
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from streamlit_autorefresh import st_autorefresh
import csv
from datetime import datetime
from quiz_data import quiz_data

ATTEMPT_LOG = "attempts_log.csv"

# ========== 1. Pre-Quiz User Info ==========
st.set_page_config(page_title="Bitwave Basics Certification Quiz", layout="wide", initial_sidebar_state="collapsed")
    
# ===== Timer at Top Right =====
css = '''
<style>
.stApp {
    background: linear-gradient(135deg, #051C2C 0%, #0B324B 100%) !important;
    background-attachment: fixed;
    color: white;
}
.timer-box {
    position: fixed;
    top: 1rem;
    right: 1rem;
    font-weight: 600;
    font-size: 1rem;
    z-index: 9999;
    background: none;
    padding: 0;
    margin: 0;
}
    header {visibility: hidden;}
    .question-box {
        border: 2px solid white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    }
    
    input[type="text"] {
        background-color: #000000;
        border: 1px solid white;
        border-radius: 6px;
        padding: 0.4rem;
        color: white;
}
    .stButton > button {
        background: linear-gradient(90deg, #02D1FF 0%, #3DF586 100%) !important;
        color: black !important;
        border: none;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 6px;
    }
    img[src*="bitwave-logo"] {
        background-color: transparent;
        padding: 0.5rem;
        border-radius: 8px;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)
st.image("assets/bitwave-logo.png", width=100)
st.image("https://uploads-ssl.webflow.com/6414c1b20a8bb758e308c685/6414c1b20a8bb716eb08c69d_Bitwave_Logo.svg", width=160)
st.markdown("# Bitwave Basics Certification Quiz")

if "user_info_submitted" not in st.session_state:
            st.session_state.user_info_submitted = False

if not st.session_state.user_info_submitted:
    st.subheader("Before you begin, please enter your details:")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    company = st.text_input("Company")

    def get_attempts(email):
        try:
            with open(ATTEMPT_LOG, newline="") as f:
                return sum(1 for row in csv.reader(f) if row and row[0] == email)
        except FileNotFoundError:
            return 0

    if st.button("Start Quiz"):
        if not name or not email or not company:
            st.warning("Please fill in all fields to begin.")
        elif "@" not in email:
            st.error("🚫 Please enter a valid email address.")
        elif get_attempts(email) >= 3:
            st.error("❌ You have reached the maximum of 3 quiz attempts. Contact support for access.")
        else:
            st.session_state.name = name
            st.session_state.email = email
            st.session_state.company = company
            st.session_state.user_info_submitted = True
            st.rerun()

# ========== 2. Initialize Quiz State ==========
if (
    st.session_state.user_info_submitted
    and "start_time" not in st.session_state
    and not st.session_state.get("submitted", False)
    and not st.session_state.get("show_results", False)
):
    st.session_state.start_time = time.time()
    st.session_state.responses = [{} for _ in quiz_data]
    st.session_state.submitted = False
    st.session_state.show_results = False



# ========== 3. Timer ==========
if st.session_state.user_info_submitted and "start_time" in st.session_state and not st.session_state.submitted:
    total_quiz_duration = 90 * 60
    elapsed = time.time() - st.session_state.start_time
    remaining = int(total_quiz_duration - elapsed)

    if remaining <= 0:
        st.warning("⏰ Time's up! Auto-submitting.")
        st.session_state.submitted = True
        st.session_state.show_results = True

    mins, secs = divmod(remaining, 60)
    st.markdown(f'<div class="timer-box">Time Left: {mins:02}:{secs:02}</div>', unsafe_allow_html=True)
  
    if (
    st.session_state.get("quiz_rendered")
    and not st.session_state.submitted
    and not st.session_state.get("show_results", False)
):
        st_autorefresh(interval=1000, key="quiz_timer_refresh")

# ========== 4. Quiz Form ==========
if st.session_state.user_info_submitted and not st.session_state.submitted and not st.session_state.get("confirm_prompt_active", False):
    st.markdown("<p style='margin-top: -3rem; font-size: 1.4rem;'>Please answer all questions below:</p>", unsafe_allow_html=True)
    
    for i, q in enumerate(quiz_data):
        with st.container():
            st.markdown(f'<strong style="font-size: 1.4rem;">Q{i + 1}:</strong> {q["question"]}', unsafe_allow_html=True)
            user_answers = []
            for j, option in enumerate(q["options"]):
                key = f"q{i}_opt{j}"
                if st.checkbox(option, key=key):
                    user_answers.append(j)
            
        st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 2px solid #888;'>", unsafe_allow_html=True)
        st.session_state.responses[i] = user_answers
    st.session_state.quiz_rendered = True
    if st.button("Submit Quiz"):
        st.session_state.pending_submit = True
        st.session_state.confirm_prompt_active = True

if st.session_state.get("confirm_prompt_active") and not st.session_state.get("confirming_done"):
    with st.container():
        unanswered = sum(1 for r in st.session_state.responses if not r)
        if unanswered:
                    st.write("")
        st.write("### Please confirm submission")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, submit"):
                st.session_state.confirmation_resolved = True
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.pending_submit = False
                st.session_state.confirm_prompt_active = False
                st.rerun()
        



# ========== 5. Show Results ==========
def generate_summary():
    results = []
    score = 0
    summary_lines = []
    for i, q in enumerate(quiz_data):
        correct = sorted(q["correct"])
        given = sorted(st.session_state.responses[i])
        is_correct = (given == correct)
        if is_correct:
            score += 1
        given_labels = [q["options"][x] for x in given]
        correct_labels = [q["options"][x] for x in correct]
        results.append((i + 1, is_correct, given_labels, correct_labels))
        if not is_correct:
            summary_lines.append(f"Q{i+1}: ❌\nYour answer: {given_labels}\nCorrect answer: {correct_labels}\n")
    return score, results, "\n\n".join(summary_lines)

def create_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        safe_line = line.encode("latin-1", "replace").decode("latin-1")
        pdf.cell(200, 10, txt=safe_line, ln=True)
    pdf_file = "/tmp/bitwave_results.pdf"
    pdf.output(pdf_file)
    return pdf_file

def send_email_with_pdf(pdf_path, score):
    sender = "your_email@example.com"
    receiver = st.session_state.email
    subject = "Bitwave Quiz Submission"
    body = f"{st.session_state.name} from {st.session_state.company} completed the quiz with a score of {score}/60. See attached."

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= results.pdf")
        msg.attach(part)

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", 587))) as server:
        server.starttls()
        server.login("your_username", "your_password")
        server.send_message(msg)

# ========== 6. Results Page ==========
if st.session_state.get("submission_confirmed") and not st.session_state.get("submitted") and not st.session_state.get("show_results"):
    st.session_state.show_results = True
    st.experimental_rerun()
if st.session_state.get("submitted") and not st.session_state.get("show_results"):
    st.session_state.show_results = True
    st.experimental_rerun()
if st.session_state.get("confirmation_resolved") and not st.session_state.get("submission_confirmed"):
    st.session_state.submission_confirmed = True
    st.rerun()

if st.session_state.get("submission_confirmed") and not st.session_state.get("submitted"):
    st.session_state.submitted = True
    st.session_state.show_results = True
    st.session_state.confirming_done = True
    st.rerun()

if st.session_state.get("show_results"):
    st.success("✅ Quiz complete!")
    score, results, summary = generate_summary()
    st.write(f"**Score: {score} / {len(quiz_data)}**")

    st.write("### Review")
    scrollable_results = []

with st.expander("🔍 Scroll to review your answers", expanded=True):
    html = '<div style="max-height: 300px; overflow-y: auto; padding-right: 1rem;">'
    for qnum, correct, given, correct_ans in results:
        status = "✅" if correct else "❌"
        html += f'''
        <div class="question-box">
            <strong style="font-size: 1.2rem;">Q{qnum} {status}</strong><br>
            <strong>Your answer:</strong> {", ".join(given) or "No answer provided"}<br>
        '''
        if not correct:
            html += f"<strong>Correct answer:</strong> {', '.join(correct_ans)}<br>"
        html += "</div><br>"
        scrollable_results.append([qnum, status, ", ".join(given), ", ".join(correct_ans)])
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)



# --- Actions Above Review ---
st.write("### Your Quiz Results")

pdf_path = create_pdf(summary)

# PDF Button
with open(pdf_path, "rb") as f:
    st.download_button(
        label="📄 Download PDF of Results",
        data=f,
        file_name="bitwave_results.pdf",
        mime="application/octet-stream"
    )

# CSV Button
import pandas as pd
df_results = pd.DataFrame(scrollable_results, columns=["Question #", "Correct", "Your Answer", "Correct Answer"])
csv_data = df_results.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Results as CSV",
    data=csv_data,
    file_name="bitwave_results.csv",
    mime="text/csv"
)

# Email warning if failed
try:
    send_email_with_pdf(pdf_path, score)
    st.info(f"📧 Results emailed to {st.session_state.email}")
except:
    st.warning("⚠️ Email not sent. Check SMTP config.")

# Restart Button
if st.button("🔁 Restart Quiz"):
    st.session_state.clear()
    st.session_state.user_info_submitted = False
    st.rerun()

    # CSV download
    import pandas as pd
    df_results = pd.DataFrame(scrollable_results, columns=["Question #", "Correct", "Your Answer", "Correct Answer"])
    csv_data = df_results.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Results as CSV", csv_data, "bitwave_results.csv", "text/csv")

    # Log the attempt
    with open(ATTEMPT_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            st.session_state.email,
            st.session_state.name,
            st.session_state.company,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            score
        ])

    try:
        send_email_with_pdf(pdf_path, score)
        st.info(f"📧 Results emailed to {st.session_state.email}")
    except:
        st.warning("⚠️ Email not sent. Check SMTP config.")

    if st.button("Restart Quiz"):
        st.session_state.clear()
        st.session_state.user_info_submitted = False
        st.rerun()
