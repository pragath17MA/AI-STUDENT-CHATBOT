document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const themeToggle = document.getElementById('theme-toggle');
    const newChatBtn = document.querySelector('.new-chat-btn');
    const historyItems = document.querySelectorAll('.history-list li');
    
    // Smooth scrolling function mapping
    const scrollToBottom = () => {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    };

    // --- Theme Management ---
    // Initialize Theme
    const initTheme = () => {
        const savedTheme = localStorage.getItem('dte-theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    };

    // Toggle Theme
    themeToggle.addEventListener('click', () => {
        let currentTheme = document.documentElement.getAttribute('data-theme');
        let newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Add rotation animation
        themeToggle.style.transform = 'rotate(180deg)';
        setTimeout(() => themeToggle.style.transform = 'none', 300);

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('dte-theme', newTheme);
        updateThemeIcon(newTheme);
    });

    const updateThemeIcon = (theme) => {
        themeToggle.innerHTML = theme === 'dark' 
            ? '<i class="fas fa-sun" style="color: #fbbf24;"></i>' 
            : '<i class="fas fa-moon"></i>';
    };

    initTheme();

    // --- Chat Functionality ---
    
    // Pre-filled questions from History
    historyItems.forEach(item => {
        item.addEventListener('click', () => {
            const topic = item.textContent.trim();
            userInput.value = `Tell me about ${topic}`;
            userInput.focus();
        });
    });

    // New Chat Button
    newChatBtn.addEventListener('click', () => {
        // Clear all messages except the first greeting
        const messages = chatMessages.querySelectorAll('.message');
        for (let i = 1; i < messages.length; i++) {
            messages[i].remove();
        }
        userInput.value = '';
        userInput.focus();
    });

    // Handle Form Submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const messageText = userInput.value.trim();
        if (!messageText) return;
        
        // 1. Clear input & Append User Message
        userInput.value = '';
        appendMessage('user', messageText);
        
        // 2. Show Typing Indicator
        const typingId = showTypingIndicator();
        
        try {
            // 3. Send Request to Flask Backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageText })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            // 4. Remove Indicator & Append Bot Response
            removeTypingIndicator(typingId);
            appendMessage('bot', data.response);

        } catch (error) {
            console.error('Chat Error:', error);
            removeTypingIndicator(typingId);
            appendMessage('bot', '⚠️ Connection lost. Please verify your network or try again later.');
        }
    });

    // Append Message to DOM
    const appendMessage = (sender, text) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        // Avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user' 
            ? '<i class="fas fa-user"></i>' 
            : '<i class="fas fa-robot"></i>';
        
        // Content
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Split by newlines for paragraph tags if necessary
        const paragraphs = text.split('\n\n');
        paragraphs.forEach(pText => {
            const p = document.createElement('p');
            p.textContent = pText;
            contentDiv.appendChild(p);
        });
        
        msgDiv.appendChild(avatarDiv);
        msgDiv.appendChild(contentDiv);
        chatMessages.appendChild(msgDiv);
        
        scrollToBottom();
    };

    // Typing Indicator UI
    const showTypingIndicator = () => {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot';
        typingDiv.id = id;
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        return id;
    };

    const removeTypingIndicator = (id) => {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    };
});
