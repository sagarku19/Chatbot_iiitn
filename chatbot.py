import json
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader
import google.generativeai as genai
from interface import ChatInterface
from colors import Colors
from typing import List, Dict, Any
import os
from datetime import datetime

class EnhancedChatbot:
    def __init__(self):
        self.interface = ChatInterface()
        self.use_pdf = False
        self.use_gemini = False
        self.pdf_processor = None
        self.gemini_ai = None
        self.intents = self._load_intents()
        self.vectorizer = TfidfVectorizer(tokenizer=self._simple_tokenizer)
        self.conversation_history = []
        self.context = {}
        self.last_intent = None
        self.pdf_data = {}
        self.gemini_model = None
        self._prepare_training_data()
        self.setup_interface()
    
    def _load_intents(self) -> Dict[str, Any]:
        with open('intents.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def _simple_tokenizer(self, text: str) -> List[str]:
        return text.lower().split()
    
    def _prepare_training_data(self):
        self.patterns = []
        self.tags = []
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                self.patterns.append(pattern)
                self.tags.append(intent['tag'])
        self.X = self.vectorizer.fit_transform(self.patterns)
    
    def _update_context(self, user_input: str, intent_tag: str):
        self.context['last_interaction'] = datetime.now().isoformat()
        self.context['last_intent'] = intent_tag
        self.context['user_input'] = user_input
        self.conversation_history.append({
            'user': user_input,
            'bot': None,
            'timestamp': datetime.now().isoformat(),
            'intent': intent_tag
        })
    
    def _get_contextual_response(self, intent_tag: str) -> str:
        intent = next((i for i in self.intents['intents'] if i['tag'] == intent_tag), None)
        if not intent:
            return "I'm not sure how to respond to that."

        # Check if we have context from previous interactions
        if self.context.get('last_intent') == intent_tag:
            # If same intent, provide a different response
            responses = intent['responses']
            if len(responses) > 1:
                used_responses = [h['bot'] for h in self.conversation_history[-3:] if h['bot']]
                available_responses = [r for r in responses if r not in used_responses]
                if available_responses:
                    return random.choice(available_responses)
        
        return random.choice(intent['responses'])
    
    def _enhance_response(self, response: str, user_input: str) -> str:
        # Add contextual information if available
        if self.context.get('last_intent'):
            if 'courses' in self.context['last_intent'] and 'admission' in response.lower():
                response += "\nWould you like to know more about the admission process?"
            elif 'facilities' in self.context['last_intent'] and 'hostel' in response.lower():
                response += "\nWould you like to know about other campus facilities?"
        
        # Add follow-up questions based on context
        if len(self.conversation_history) > 0:
            last_interaction = self.conversation_history[-1]
            if 'courses' in last_interaction['intent']:
                response += "\nWould you like to know about the curriculum or faculty?"
            elif 'facilities' in last_interaction['intent']:
                response += "\nWould you like to know about the sports facilities or library?"

        return response
    
    def setup_interface(self):
        self.interface.clear_screen()
        self.interface.show_header()
        self.interface.show_welcome()
        self.interface.show_footer()
        self.interface.show_help()
    
    def configure_pdf_support(self, pdf_paths: List[str]):
        for path in pdf_paths:
            if os.path.exists(path):
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                self.pdf_data[path] = text
    
    def configure_gemini_support(self, api_key: str):
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    
    def get_response(self, user_input: str) -> str:
        # Vectorize user input
        user_vector = self.vectorizer.transform([user_input])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(user_vector, self.X).flatten()
        
        # Get the most similar pattern
        best_match_idx = np.argmax(similarity_scores)
        best_match_score = similarity_scores[best_match_idx]
        
        # Get the corresponding tag
        intent_tag = self.tags[best_match_idx]
        
        # Update context
        self._update_context(user_input, intent_tag)
        
        # Check if the question is about other institutes
        other_institutes = ['iit', 'nit', 'bits', 'vit', 'mit']
        is_about_other = any(inst in user_input.lower() for inst in other_institutes) and 'iiit' not in user_input.lower()
        
        # If asking about other institutes, provide a redirect response
        if is_about_other:
            redirect_response = (
                "I specialize in providing information about IIIT Nagpur. While I can't provide details about other "
                "institutes, I'd be happy to tell you about IIIT Nagpur's programs, including:\n\n"
                "- B.Tech in CSE with specializations in AI/ML, Data Science, and Gaming Technology\n"
                "- B.Tech in ECE with IoT specialization\n"
                "- M.Tech and Ph.D. programs\n\n"
                "Would you like to know more about any of these programs?"
            )
            self.conversation_history[-1]['bot'] = redirect_response
            return redirect_response
        
        # If similarity score is low, use intent-based response
        if best_match_score < 0.7:
            try:
                # Get base response
                response = self._get_contextual_response(intent_tag)
                
                # Enhance with follow-up
                if 'courses' in intent_tag:
                    response += "\n\nWould you like to know more about our specializations or admission process?"
                elif 'facilities' in intent_tag:
                    response += "\n\nWould you like to know more about our hostels or research facilities?"
                elif 'about' in intent_tag:
                    response += "\n\nWhat specific aspect of IIIT Nagpur would you like to learn more about?"
                
                # Update conversation history
                self.conversation_history[-1]['bot'] = response
                return response
                
            except Exception as e:
                print(f"Error in response generation: {e}")
                # Fallback response
                fallback = ("I'm here to help you learn about IIIT Nagpur. I can provide information about our "
                          "academic programs, campus facilities, admission procedures, and more. What would you like to know?")
                self.conversation_history[-1]['bot'] = fallback
                return fallback
        
        # Get base response for high similarity matches
        response = self._get_contextual_response(intent_tag)
        enhanced_response = self._enhance_response(response, user_input)
        self.conversation_history[-1]['bot'] = enhanced_response
        return enhanced_response
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        return self.conversation_history
    
    def clear_context(self):
        self.context = {}
        self.conversation_history = []
        self.last_intent = None

class PDFProcessor:
    def __init__(self, pdf_paths):
        self.pdf_paths = pdf_paths
        self.documents = self.load_pdfs()
    
    def load_pdfs(self):
        documents = []
        for pdf_path in self.pdf_paths:
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    documents.append(page.extract_text())
            except Exception as e:
                print(f"Error loading PDF {pdf_path}: {str(e)}")
        return documents
    
    def search_in_pdfs(self, query):
        # Simple keyword-based search
        query = query.lower()
        for doc in self.documents:
            if query in doc.lower():
                # Return the relevant paragraph
                paragraphs = doc.split('\n\n')
                for para in paragraphs:
                    if query in para.lower():
                        return para
        return None 