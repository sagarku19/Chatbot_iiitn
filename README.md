# Chatbot_iiitn
# 🤖 IIIT Nagpur Virtual Assistant Chatbot

A virtual assistant chatbot designed to help prospective and current students explore and understand IIIT Nagpur. It provides helpful responses related to academics, campus facilities, student activities, and the admission process.

## 📸 Demo
![WebView](image.png)


---

## 🚀 Features

- Interactive chat interface built using **Flask** and **HTML/CSS/JS**
- Natural Language Processing using a custom-trained model
- Intent classification using a neural network
- Data-driven chatbot powered by `intents.json`
- Real-time responses with typing animation
- Personalized welcome and status indicators

---

## 🧠 Technologies Used

- Python 3
- Flask
- NLTK
- TensorFlow / PyTorch (for training the model)
- Scikit-learn
- HTML, CSS, JavaScript
- Pickle (for saving processed classes and words)


---

## 🔧 Installation

1. **Clone the repository**

git clone https://github.com/<your-username>/iiitn-chatbot.git
cd iiitn-chatbot

2. **Create and activate a virtual environment (optional but recommended)**


python -m venv venv
source venv/bin/activate    # On Linux/macOS
venv\Scripts\activate       # On Windows

3. **Install Dependencies**
pip install -r requirements.txt

4. **Run the App**
python app.py
- Then visit: http://localhost:5000 in your browser.

5. **Retrain the Medel**
python chatbot.py
- Make sure your intents.json file is updated before training.



---

Let me know if you have any Questions!
