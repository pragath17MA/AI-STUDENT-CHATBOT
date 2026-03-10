import google.generativeai as genai
import os
import numpy as np

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    TfidfVectorizer = None
    cosine_similarity = None

from app_core.data.intents import INTENTS, DTE_PERSONA

class AIService:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.model = None
        self.vectorizer = None
        self.X_train = None
        self.responses = []
        
        # Initialize Gemini if key exists
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception as e:
                print(f"Gemini initialization failed: {e}")
        
        # Initialize TF-IDF Fallback Knowledge
        self._setup_fallback()

    def _setup_fallback(self):
        """Pre-processes the intent database for rapid lookup."""
        if not TfidfVectorizer:
            return
            
        corpus = []
        for intent in INTENTS:
            for pattern in intent["patterns"]:
                corpus.append(pattern.lower())
                self.responses.append(intent["response"])
        
        try:
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
            self.X_train = self.vectorizer.fit_transform(corpus)
        except Exception as e:
            print(f"Fallback setup error: {e}")

    def get_fallback_response(self, user_message):
        """Provides a response using NLP patterns if the LLM is unavailable."""
        if self.vectorizer is None or self.X_train is None:
            return ("I'm currently in basic mode. I specialize in DTE topics like admissions, "
                    "exams, and scholarships. How can I help?")
            
        msg_lower = user_message.lower().strip()
        user_vec = self.vectorizer.transform([msg_lower])
        similarities = cosine_similarity(user_vec, self.X_train)
        
        idx = np.argmax(similarities)
        score = similarities[0][idx]
        
        if score > 0.15:
            return self.responses[idx]
        return ("That's an interesting question! While I primarily focus on DTE (admissions, "
                "exams, syllabus), I'm learning more every day. Could you please "
                "rephrase or ask about specific DTE related information?")

    def generate_response(self, user_message, chat_history=[]):
        """The main entry point for generating a chatbot response."""
        # 1. Try LLM first
        if self.model:
            try:
                # Add context from history (if relevant)
                history_formatted = []
                for entry in chat_history[-6:]:
                    role = "user" if entry['role'] == "user" else "model"
                    history_formatted.append({"role": role, "parts": [entry['content']]})
                
                # Compose the intelligent prompt
                prompt = f"{DTE_PERSONA}\n\nStudent asks: {user_message}"
                response = self.model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                print(f"LLM Error encountered: {e}")
                return self.get_fallback_response(user_message)
        
        # 2. Revert to Hybrid Fallback
        return self.get_fallback_response(user_message)
