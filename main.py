from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import sys
from dotenv import load_dotenv

# Ensure the root directory is in the path for modular imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modular services
from app_core.services.db_service import DatabaseService
from app_core.services.ai_service import AIService

# Load configuration from Environment
load_dotenv()

class AppConfig:
    """Centralized configuration for the application."""
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_FILE = os.getenv("DB_FILE", "chatbot.db")
    DB_PATH = os.path.join(BASE_DIR, DB_FILE)
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")

def create_app():
    """Application Factory to initialize Flask with all required services."""
    app = Flask(__name__)
    
    # Enable API rate limiting for security
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

    # Initialize Core Shared Services
    db = DatabaseService(AppConfig.DB_PATH)
    ai = AIService(AppConfig.GEMINI_KEY)

    # --- Core Application Routes ---
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/history', methods=['GET'])
    @limiter.limit("5 per minute") # Extra protection for history route
    def get_history():
        """Returns the last 20 messages for the conversation session."""
        try:
            history = db.get_history(limit=20)
            return jsonify(history)
        except Exception as e:
            app.logger.error(f"Error fetching history: {e}")
            return jsonify([]), 500

    @app.route('/api/chat', methods=['POST'])
    @limiter.limit("10 per minute") # Prevent brute force bot interactions
    def handle_chat_query():
        """Processes user input, generates AI response, and saves to database."""
        data = request.get_json(silent=True) or {}
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"response": "I'm listening! Ask me anything about DTE."}), 400
        
        try:
            # 1. Provide Context to the AI (Recent conversation history)
            recent_context = db.get_history(limit=6)
            
            # 2. Get intelligent AI response
            response_text = ai.generate_response(user_message, recent_context)
            
            # 3. Securely Log the interaction
            db.save_message('user', user_message)
            db.save_message('assistant', response_text)
            
            return jsonify({"response": response_text})
            
        except Exception as e:
            app.logger.error(f"Chat processing failed: {e}")
            return jsonify({"response": "Something went wrong. Please try again later."}), 500

    @app.route('/api/clear', methods=['POST'])
    def clear_all_history():
        """Resets the conversation history for a fresh start."""
        try:
            db.clear()
            return jsonify({"status": "success", "message": "History cleared successfully."})
        except Exception as e:
            app.logger.error(f"Error clearing history: {e}")
            return jsonify({"status": "error", "message": "Internal error."}), 500

    @app.route('/api/health')
    def health_check():
        """Simple health check endpoint for monitoring."""
        return jsonify({"status": "healthy", "service": "DTE-AI-Assistant"})

    return app

if __name__ == '__main__':
    dte_bot = create_app()
    # In professional environments, use Waitress for production serving
    print(f"Server starting on http://{AppConfig.HOST}:{AppConfig.PORT} (Debug: {AppConfig.DEBUG})")
    dte_bot.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)
