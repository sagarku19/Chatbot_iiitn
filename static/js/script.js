document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-button');
    let isTyping = false;
    
    // Function to add a message to the chat
    function addMessage(message, isUser = false, timestamp = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const paragraph = document.createElement('p');
        paragraph.textContent = message;
        
        if (timestamp) {
            const timeSpan = document.createElement('span');
            timeSpan.className = 'message-time';
            timeSpan.textContent = new Date(timestamp).toLocaleTimeString();
            contentDiv.appendChild(timeSpan);
        }
        
        contentDiv.appendChild(paragraph);
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        if (isTyping) return;
        
        isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        isTyping = false;
    }
    
    // Function to send message to server
    async function sendMessage(message) {
        try {
            showTypingIndicator();
            
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });
            
            const data = await response.json();
            removeTypingIndicator();
            
            if (response.ok) {
                addMessage(data.response, false, data.timestamp);
                // Update conversation history if needed
                if (data.history) {
                    updateHistory(data.history);
                }
            } else {
                addMessage(data.error || 'Sorry, there was an error processing your request.', false, data.timestamp);
            }
        } catch (error) {
            removeTypingIndicator();
            console.error('Error:', error);
            addMessage('Sorry, there was an error connecting to the server.', false);
        }
    }
    
    // Function to update conversation history
    function updateHistory(history) {
        // Clear existing messages except the first welcome message
        while (chatMessages.children.length > 1) {
            chatMessages.removeChild(chatMessages.lastChild);
        }
        
        // Add messages from history
        history.forEach(entry => {
            if (entry.user) {
                addMessage(entry.user, true, entry.timestamp);
            }
            if (entry.bot) {
                addMessage(entry.bot, false, entry.timestamp);
            }
        });
    }
    
    // Function to clear conversation history
    async function clearHistory() {
        try {
            const response = await fetch('/clear', {
                method: 'POST',
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Clear chat messages except the welcome message
                while (chatMessages.children.length > 1) {
                    chatMessages.removeChild(chatMessages.lastChild);
                }
                addMessage('Conversation history cleared.', false, data.timestamp);
            } else {
                addMessage(data.error || 'Error clearing history.', false, data.timestamp);
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Error clearing conversation history.', false);
        }
    }
    
    // Function to handle message sending
    function handleSendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            sendMessage(message);
            userInput.value = '';
        }
    }
    
    // Handle send button click
    sendButton.addEventListener('click', handleSendMessage);
    
    // Handle Enter key press
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Prevent default Enter behavior
            handleSendMessage();
        }
    });
    
    // Handle clear button click
    if (clearButton) {
        clearButton.addEventListener('click', clearHistory);
    }
    
    // Focus input on load
    userInput.focus();
}); 