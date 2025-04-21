from flask import Flask, render_template, request, jsonify, session
from chatbot import EnhancedChatbot
import os
from datetime import datetime
from typing import Dict, Any
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Initialize chatbot
chatbot = EnhancedChatbot()

# Configure chatbot with environment variables
pdf_paths = os.getenv('PDF_PATHS', '').split(',') if os.getenv('PDF_PATHS') else []
gemini_api_key = os.getenv('GEMINI_API_KEY')

if pdf_paths:
    chatbot.configure_pdf_support(pdf_paths)
if gemini_api_key:
    chatbot.configure_gemini_support(gemini_api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                'error': 'No message provided',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Get chatbot response
        response = chatbot.get_response(user_message)
        
        # Get conversation history
        history = chatbot.get_conversation_history()
        
        return jsonify({
            'response': response,
            'history': history,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        history = chatbot.get_conversation_history()
        return jsonify({
            'history': history,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    try:
        chatbot.clear_context()
        return jsonify({
            'message': 'Conversation history cleared',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 