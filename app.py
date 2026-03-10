import os
import sys

# DEPRECATION NOTICE for developers
# ---------------------------------
# The chatbot has been refactored into a modular, production-ready structure.
# All new features and security fixes are now implemented in main.py.
# ---------------------------------

# Set project root for relative imports in modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from main import create_app, AppConfig
    
    # Initialize the modular application
    app = create_app()

    if __name__ == '__main__':
        # Start the professional server entry point
        print("\n" + "="*50)
        print("    🚀 DTE Assistant v2.0 - Premium AI Engine 🚀")
        print("="*50)
        print(f"[SYSTEM] Environment: Production Ready (Modular)")
        print(f"[SYSTEM] Database: {AppConfig.DB_PATH}")
        print(f"[SYSTEM] Mode: {'Online (Gemini)' if AppConfig.GEMINI_KEY else 'Local Fallback (NLP)'}")
        print("-"*50)
        app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)

except ImportError as e:
    print(f"\n[ERROR] Missing core application modules: {e}")
    print("[ERROR] Please ensure you've ran: pip install -r requirements.txt")
