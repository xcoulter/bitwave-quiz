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
    {
        "question": "[SINGLE] In order to add a new user to Bitwave, which of the following do you need from the new user?",
        "options": ["Phone number", "Twitter handle", "Email address", "Name"],
        "correct": [2, 3],
        "type": "multi"
    },
    {
        "question": "[SINGLE] Which of the following user permissions would be sufficient for an auditor?",
        "options": ["User", "Admin user", "None of the above"],
        "correct": [0],
        "type": "single"
    },
    {
        "question": "[SINGLE] Users with 'Read-only' access are able to perform some tasks in Bitwave, including categorizing and adding wallets.",
        "options": ["True", "False"],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[SINGLE] Which of the two above allows users to revoke access to another user?",
        "options": ["Read-only", "Admin user"],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[SINGLE] Which currency should you select for your org?",
        "options": ["USD.", "The currency in which the legal entity is located.", "Bitwave only operates in USD.", "The same currency as your ERP."],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[SINGLE] When setting up the organization settings, which timezone should you select?",
        "options": ["The timezone where the bookkeeper is located.", "Bitwave HQ timezone.", "UTC", "The timezone where the legal entity is located."],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] The default pricing source in Bitwave is...",
        "options": ["Binance", "Kraken", "Bitwave's own pricing source", "CryptoCompare"],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] Which of the following statements is true about pricing in Bitwave?",
        "options": ["All prices are standard and cannot be updated.", "Only trade transactions are priced; all other transactions will not have pricing until the bookkeeper reviews and determines the appropriate price.", "There are multiple pricing sources available on the platform, additionally users can manually override existing pricing on a transaction by transaction basis.", "None of the above is true."],
        "correct": [2],
        "type": "single"
    },
    {
        "question": "[MULTI] Which 2 GL accounts are created for you when you first connect your ERP to Bitwave?",
        "options": ["Bitwave - Crypto Liabilities", "Bitwave - Crypto Revenue", "Bitwave - Digital Assets", "Bitwave - Crypto Fees"],
        "correct": [2, 3],
        "type": "multi"
    },
    {
        "question": "[SINGLE] What are categories and contacts in Bitwave?",
        "options": ["Categories = Transaction type (inflow/outflow/trade/internal transfer), Contacts = Vendors", "Categories = GL Accounts, Contacts = Vendors & Customers", "Categories = Transaction types, Contacts = Contacts imported from your ERP", "Categories = Exchange Types, Contacts = Wallet Owners"],
        "correct": [0],
        "type": "single"
    },
    
{
        "question": "[SINGLE] Can you use Bitwave without connecting your ERP?",
        "options": [
            "No, in order for categories and contacts to appear in Bitwave, you need to connect an ERP.",
            "Yes, but you cannot generate the gain/loss report.",
            "No, transactions will not sync to Bitwave without an ERP connected.",
            "Yes, Bitwave still allows you to categorise and generate reports without an ERP."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] You should only set up accounting defaults after you have categorised all your transactions.",
        "options": [
            "True, this is the final step you take before syncing transactions to your ERP.",
            "False, you should set this up once you have connected your ERP, created a crypto fees contact, and before adding any wallets."
        ],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[MULTI] Which of the following are considered 'exchanges' in Bitwave?",
        "options": [
            "Metamask",
            "Anchorage",
            "Bitcoin Hardware Wallet",
            "Binance",
            "Bitfinex",
            "Binance.us"
        ],
        "correct": [3, 4, 5],
        "type": "multi"
    },
    {
        "question": "[SINGLE] What is Bitwave's definition of an exchange?",
        "options": [
            "A third party custodial wallet that connects to Bitwave via API",
            "The Ethereum blockchain",
            "A metamask wallet which can be connected to Bitwave by creating a wallet and selecting 'watch wallet'",
            "A 3rd party trading platform that provides transaction data to Bitwave via API"
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] Exchanges require API keys to connect to Bitwave.",
        "options": ["True", "False"],
        "correct": [0],
        "type": "single"
    },
    {
        "question": "[SINGLE] Which of the following best describes API keys as it relates to Bitwave users?",
        "options": [
            "The keys that users need to input when syncing transactions to their ERP.",
            "A connection to an open source protocol, such as a blockchain.",
            "Your Bitwave log in credentials.",
            "A set of codes or passphrases that allows Bitwave to pull transaction data from an Exchange or custodial wallet."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[MULTI] In what ways are custodial wallets and exchanges similar?",
        "options": [
            "You only need a wallet address for Bitwave to receive transaction data.",
            "They are non-custodial services where users hold their private keys.",
            "They require API keys for Bitwave to receive transaction data.",
            "They are third-party providers where users do not hold their own private keys."
        ],
        "correct": [2, 3],
        "type": "multi"
    },
    {
        "question": "[MULTI] Which custodial wallets does Bitwave support?",
        "options": ["Binance.us", "Metamask", "FTX", "Anchorage", "Nydig", "Bitgo"],
        "correct": [0, 3, 4, 5],
        "type": "multi"
    },
    {
        "question": "[SINGLE] Bitwave requires 'read-only' access when connecting via API keys to exchanges. This means that...",
        "options": [
            "Bitwave can process transactions on behalf of the user.",
            "Only users with admin permissions in Bitwave can process transactions in the connected account.",
            "Bitwave will automatically categorize all transactions that sync from your connected external account.",
            "Bitwave will not have the ability to process transactions via the API keys."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] Custodial solutions refers to...",
        "options": [
            "Any blockchain where the user has full custody of their own digital assets.",
            "A metamask wallet on Ethereum.",
            "A third party exchange where digital assets can be bought and sold.",
            "Any third party custodial service provider that maintains the private keys for access to digital asset holdings on behalf of their customers."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] Bitwave cannot detect trades on Decentralised exchanges.",
        "options": ["True", "False"],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[SINGLE] Non-custodial solutions refers to...",
        "options": [
            "A wallet on the Ethereum network.",
            "A third party custody solution, such as Anchorage.",
            "All of the above",
            "A wallet holding digital assets for which the user maintains their own private keys."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] Metamask is a custodial wallet.",
        "options": ["True", "False"],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[SINGLE] Bitwave will only ask you to provide a non-custodial wallet or a custodial wallet, but never both.",
        "options": ["True", "False"],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[MULTI] Which of the following are examples of non custodial wallets?",
        "options": ["FTX account", "Binance Account", "Metamask ETH wallet", "BTC wallet on ledger hardware device"],
        "correct": [2, 3],
        "type": "multi"
    },
    {
        "question": "[SINGLE] Non-custodial wallets need to be connected via an API key.",
        "options": ["True", "False"],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[MULTI] What sources of crypto transactions can be imported?",
        "options": ["Internal databases", "Txn data on non integrated networks", "Non-integrated exchanges", "All of the above"],
        "correct": [3],
        "type": "multi"
    },
    {
        "question": "[SINGLE] The image above shows all of the columns (headers) in the Bitwave import tool. Which of the above are mandatory fields?",
        "options": ["A, E, F, I, L, M, P", "B, E, F, H, L, P", "A, B, C, D, E, F, G, H, I", "A, C, D, I, L, M, P"],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] It is possible to categorise transactions directly from the import tool.",
        "options": ["True", "False"],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[MULTI] Which of the following would cause problems when importing data into bitwave?",
        "options": [
            "User enters a negative number in the amount column of the import file.",
            "User enters a wallet address in the accountid column of the import file.",
            "User enters a previously used value in the \"id\" column of the import file.",
            "User enters a token that does not exist in bitwave into the amountticker column of the import file."
        ],
        "correct": [0, 2, 3],
        "type": "multi"
    },
    {
        "question": "[SINGLE] I want to create a new GL account to book a transaction and sync it to my ERP, how would I do this?",
        "options": [
            "I would need to create the category in Bitwave, book the transaction, and sync it to my ERP.",
            "Using the import tool, you would upload the GL accounts into Bitwave, book the transaction and sync it to your ERP.",
            "All GL accounts must be in your ERP when you first make the connection. You must disconnect your ERP, create the GL account in your ERP, reconnect your ERP to Bitwave, book the transactions and sync it to your ERP.",
            "I would need to create the GL account in my ERP, sync it through to Bitwave, book the transaction and sync it to my ERP."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] What is wallet hygiene?",
        "options": [
            "Making sure you connect all relevant wallets and exchanges to Bitwave.",
            "Ensuring that there are no spam airdrop transactions in your wallet",
            "Ensuring that no other party has access to your Bitwave account.",
            "Maintaining an organized list of wallets that each have a dedicated business purpose."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] A customer paid my company for an open invoice using crypto, how do I categorise that transaction in Bitwave?",
        "options": [
            "Using the standard categorization type and ensuring to add the invoice # in the description field.",
            "Using the 'ignore' function as the invoice is already in your ERP, so there is no need to book this.",
            "Using the trade categorization type.",
            "Using the invoice/bill payment treatment and select the relevant customer and invoice."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] In the scenario screenshot above, what would be the most likely way that I would categorize this transaction?",
        "options": [
            "I would categorize this as a trade, resulting in no journal entry.",
            "I would book the 0.12 ETH to an expense account and add Ethereum Network as the vendor contact.",
            "I would book the ETH to a revenue account and select the relevant customer.",
            "I would book the ETH to an ETH asset account and credit my revenue account."
        ],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[SINGLE] What type of transaction is this?",
        "options": [
            "This is an internal transfer between wallets.",
            "This is an inflow of assets into my wallet.",
            "This is an invoice payment.",
            "This is a trade."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] Wrapping treatment allows you to treat token wrapping transactions (such as ETH --> WETH) avoiding a gain/loss scenario.",
        "options": ["True", "False"],
        "correct": [0],
        "type": "single"
    },
    {
        "question": "[SINGLE] Getting transactions coded and synced to your ERP involves two steps, what are they called in Bitwave?",
        "options": [
            "Importing and Syncing",
            "Updating and Accounting",
            "Connecting and Finishing",
            "Categorization and Reconciliation"
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[MULTI] In the transactions tab, which of the following can you filter transactions by?",
        "options": [
            "Reconciliation status",
            "Wallet",
            "Categorization status",
            "Ignored status"
        ],
        "correct": [0, 1, 2, 3],
        "type": "multi"
    },
    {
        "question": "[SINGLE] Bitwave does not allow you to search using a transaction hash.",
        "options": ["True", "False"],
        "correct": [1],
        "type": "single"
    },
    {
        "question": "[SINGLE] What does 'ignoring' a transaction achieve?",
        "options": [
            "Ignoring a transactions allows you to hide the transaction in the UI, but it will still show up in all reports and sync to your ERP if it's categorized.",
            "Ignoring a transaction means to delete the transaction completely.",
            "Ignoring a transaction omits it from all reports, but still allows you to sync it to your ERP.",
            "Ignoring a transaction allows you to omit the transaction from all reports while not deleting it entirely."
        ],
        "correct": [3],
        "type": "single"
    },
    {
        "question": "[SINGLE] The rules engine allows users to...",
        "options": [
            "Categorise trades",
            "Ignore transactions",
            "Categorise transactions based on certain transaction commonalities.",
            "All of the above"
        ],
        "correct": [2],
        "type": "single"
    },
    {
        "question": "[SINGLE] Bitwave rules can be applied on a wallet per wallet basis.",
        "options": ["True", "False"],
        "correct": [1],
        "type": "single"
    }
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
