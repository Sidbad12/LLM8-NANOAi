let chatHistory = [];
let isWaitingForResponse = false;

// Initialize the application
async function initializeApp() {
    await loadChatHistory();
    await checkServerStatus();
    
    // Set up event listeners
    document.getElementById('messageInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Focus input field
    document.getElementById('messageInput').focus();
}

// Check server status
async function checkServerStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        updateStatusIndicator(data.model_loaded);
        updateModelInfo(data.model_type);
        
    } catch (error) {
        console.error('Status check failed:', error);
        updateStatusIndicator(false);
    }
}

// Update status indicator
function updateStatusIndicator(modelLoaded) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.getElementById('statusText');
    const systemStatus = document.getElementById('systemStatus');
    
    if (modelLoaded) {
        statusDot.style.background = '#22c55e';
        statusText.textContent = 'AI Model Ready';
        systemStatus.textContent = 'Online';
        systemStatus.className = 'status-online';
    } else {
        statusDot.style.background = '#ef4444';
        statusText.textContent = 'Knowledge Base Only';
        systemStatus.textContent = 'Limited';
        systemStatus.className = 'status-offline';
    }
}

// Update model information
function updateModelInfo(modelType) {
    const modelTypeElement = document.getElementById('modelType');
    const responseSourceElement = document.getElementById('responseSource');
    
    modelTypeElement.textContent = modelType;
    responseSourceElement.textContent = modelType === 'Heart-Specialized DistilGPT2' 
        ? 'AI Model & Knowledge Base' 
        : 'Knowledge Base Only';
}

// Send message to server
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isWaitingForResponse) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    input.value = '';
    isWaitingForResponse = true;
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.response) {
            addMessage(data.response, 'ai', data.source);
            updateSourceBadge(data.source);
        } else if (data.error) {
            addMessage('Sorry, I encountered an error. Please try again.', 'ai', 'error');
        }
        
    } catch (error) {
        addMessage('Connection error. Please check your internet connection and try again.', 'ai', 'error');
    } finally {
        isWaitingForResponse = false;
        hideTypingIndicator();
    }
}

// Add message to chat
function addMessage(text, sender, source = null) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Remove welcome message if it's the first real message
    if (chatHistory.length === 0) {
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const timestamp = new Date().toLocaleTimeString();
    
    messageDiv.innerHTML = `
        <div class="message-content">${formatMessage(text)}</div>
        <div class="message-meta">
            ${sender === 'user' ? 'You' : 'AI Assistant'} • ${timestamp}
            ${source ? ` • via ${formatSource(source)}` : ''}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Add to history
    chatHistory.push({ text, sender, timestamp, source });
}

// Format message text
function formatMessage(text) {
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    // Format lists
    text = text.replace(/\d+\.\s/g, '<br>$&');
    
    return text;
}

// Format response source
function formatSource(source) {
    const sourceMap = {
        'model': 'AI Model',
        'knowledge_base': 'Knowledge Base',
        'error': 'System'
    };
    
    return sourceMap[source] || source;
}

// Update source badge
function updateSourceBadge(source) {
    const badge = document.getElementById('sourceBadge');
    badge.textContent = formatSource(source);
}

// Show typing indicator
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message';
    typingDiv.id = 'typingIndicator';
    
    typingDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Load chat history
async function loadChatHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            data.history.forEach(item => {
                addMessage(item.question, 'user');
                addMessage(item.answer, 'ai', item.source);
            });
        }
    } catch (error) {
        console.log('Could not load chat history');
    }
}

// Quick question function
function askQuickQuestion(question) {
    document.getElementById('messageInput').value = question;
    sendMessage();
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initializeApp);