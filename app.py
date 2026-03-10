from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import sys
from dotenv import load_dotenv

# Robust imports to prevent total crash if deps are missing
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError:
    print("Warning: ML dependencies (Scikit-learn/Numpy) missing. Re-installing might be needed.")

load_dotenv()

app = Flask(__name__)

# --- Absolute Path Configuration ---
# This ensures the database is always found regardless of where you start the app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'chatbot.db')

# --- Machine Learning NLP Setup ---
INTENTS = [
    {
        "patterns": ["hello", "hi", "hey", "greetings", "good morning", "help"],
        "response": "Hello! I am your DTE Student Assistant. I can help you with admissions, syllabus, exams, results, scholarships, and career guidance. How can I assist you today?"
    },
    {
        "patterns": ["how to apply for admission", "admission process", "eligibility", "enroll", "admission requirements", "application form"],
        "response": "To apply for diploma courses, participate in the Centralized Admission Process (CAP) via the official DTE portal. Application dates are generally announced in May-June."
    },
    {
        "patterns": ["syllabus", "curriculum", "subjects", "computer science syllabus"],
        "response": "You can find the latest curriculum for all branches on the DTE website under 'Academics' -> 'Syllabus'. It's available as a downloadable PDF."
    },
    {
        "patterns": ["exams", "timetable", "test schedule", "semester exams"],
        "response": "Odd semester exams are in Nov/Dec, and even semesters in April/May. Check the 'Examination' section of the DTE portal for details."
    },
    {
        "patterns": ["results", "marks card", "revaluation"],
        "response": "Results are announced 30-45 days after exams. Check the DTE results portal with your Register Number."
    },
    {
        "patterns": ["scholarship", "financial aid", "SSP", "NSP"],
        "response": "Apply via State Scholarship Portal (SSP) or National Scholarship Portal (NSP). Ensure your Aadhaar is linked to your bank account."
    },
    {
        "patterns": ["career", "higher education", "lateral entry", "jobs"],
        "response": "You can join B.E./B.Tech via Lateral Entry (2nd year) or seek Junior Engineer roles in govt/private sectors."
    },
    {
        "patterns": ["thank you", "thanks", "thanks for the help"],
        "response": "You're very welcome! Feel free to ask more questions!"
    }
]

# Initialize training data
corpus = []
responses = []
for intent in INTENTS:
    for pattern in intent["patterns"]:
        corpus.append(pattern.lower())
        responses.append(intent["response"])

# Train the TF-IDF Vectorizer
# Only perform if imports succeeded
vectorizer = None
X_train = None
if 'TfidfVectorizer' in globals():
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_train = vectorizer.fit_transform(corpus)

def get_nlp_response(user_message):
    if not vectorizer:
        return "I'm having trouble loading my intelligence module right now, but I'm basically a DTE Assistant!"
        
    message_lower = user_message.lower().strip()
    user_vec = vectorizer.transform([message_lower])
    similarities = cosine_similarity(user_vec, X_train)
    max_sim_index = np.argmax(similarities)
    max_sim_score = similarities[0][max_sim_index]
    
    if max_sim_score > 0.15:
        return responses[max_sim_index]
    else:
        return "I specialize in DTE topics like admissions and exams. Could you please rephrase your question?"

# --- Database Setup ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Initialize on startup
init_database()

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    # Robust JSON check
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"response": "I didn't hear you clearly. Could you repeat that?"}), 400
    
    response_text = get_nlp_response(user_message)
    
    # Save conversation
    try:
        with get_db_connection() as conn:
            conn.execute('INSERT INTO chats (role, content) VALUES (?, ?)', ('user', user_message))
            conn.execute('INSERT INTO chats (role, content) VALUES (?, ?)', ('assistant', response_text))
            conn.commit()
    except Exception as e:
        print(f"Database Logging Error: {e}")
        
    return jsonify({"response": response_text})

if __name__ == '__main__':
    # Using port 5000 as default
    app.run(debug=True, port=5000)

