document_id = "script_js"
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const welcomeScreen = document.getElementById('welcome-screen');
    const newChatBtn = document.getElementById('new-chat-btn');
    const clearBtn = document.getElementById('clear-btn');
    const historyList = document.getElementById('history-list');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');

    // --- Configuration ---
    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                return hljs.highlight(code, { language: lang }).value;
            }
            return hljs.highlightAuto(code).value;
        },
        breaks: true,
        gfm: true
    });

    const scrollToBottom = () => {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    };

    const toggleWelcome = (show) => {
        if (!welcomeScreen) return;
        welcomeScreen.style.display = show ? 'block' : 'none';
    };

    // --- History Management ---
    const loadHistory = async () => {
        try {
            const response = await fetch('/api/history');
            const history = await response.json();
            
            if (history.length > 0) {
                toggleWelcome(false);
                history.forEach(msg => {
                    appendMessage(msg.role, msg.content, false);
                });
            } else {
                toggleWelcome(true);
            }

            updateHistorySidebar(history);
        } catch (error) {
            console.error('Failed to load history:', error);
        }
    };

    const updateHistorySidebar = (history) => {
        if (!historyList) return;
        historyList.innerHTML = '';
        
        // Extract unique user messages as conversation titles
        const titles = history
            .filter(msg => msg.role === 'user')
            .map(msg => msg.content)
            .slice(-15) // Last 15
            .reverse();

        if (titles.length === 0) {
            const emptyHint = document.createElement('div');
            emptyHint.className = 'history-item-hint';
            emptyHint.style.cssText = 'font-size: 0.8rem; color: var(--text-muted); padding: 10px; text-align: center;';
            emptyHint.textContent = 'No recent chats';
            historyList.appendChild(emptyHint);
            return;
        }

        titles.forEach(title => {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.innerHTML = `<i class="far fa-message"></i> <span>${title}</span>`;
            div.title = title;
            div.onclick = () => {
                userInput.value = title;
                userInput.focus();
                // Optional: Auto-submit or just fill
            };
            historyList.appendChild(div);
        });
    };

    // --- UI Interactions ---
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    newChatBtn.addEventListener('click', () => {
        // Start fresh
        window.location.reload();
    });

    clearBtn.addEventListener('click', async () => {
        if (confirm('Clear all conversation history? This cannot be undone.')) {
            await fetch('/api/clear', { method: 'POST' });
            window.location.reload();
        }
    });

    // Input Auto-resize
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
    });

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // --- Chat Logic ---
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (!text) return;

        // Hide welcome on first message
        toggleWelcome(false);

        // Reset input
        userInput.value = '';
        userInput.style.height = 'auto';

        // Append User Message
        appendMessage('user', text);

        // Show Typing indicator
        const typingDiv = showTyping();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            typingDiv.remove();

            if (!response.ok) {
                appendMessage('assistant', `⚠️ **Error:** ${data.response || 'Something went wrong.'}`);
            } else {
                appendMessage('assistant', data.response);
                // Refresh history sidebar silently
                const histRes = await fetch('/api/history');
                const history = await histRes.json();
                updateHistorySidebar(history);
            }

        } catch (error) {
            if (typingDiv) typingDiv.remove();
            appendMessage('assistant', '⚠️ **Connection Error:** Failed to reach the AI server.');
        }
    });

    // --- Rendering Engine ---
    const appendMessage = (role, content, animate = true) => {
        const row = document.createElement('div');
        row.className = `message-row ${role === 'assistant' ? 'assistant' : 'user'} animate-message`;
        
        const avatarWrapper = document.createElement('div');
        avatarWrapper.className = 'avatar-wrapper';
        
        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = role === 'assistant' 
            ? '<i class="fas fa-robot"></i>' 
            : '<i class="fas fa-user"></i>';
        
        avatarWrapper.appendChild(avatar);

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        
        messageContent.appendChild(bubble);
        row.appendChild(avatarWrapper);
        row.appendChild(messageContent);
        chatMessages.appendChild(row);

        if (role === 'assistant' && animate) {
            typeWriter(bubble, content);
        } else {
            bubble.innerHTML = marked.parse(content);
            finishRendering(row);
        }

        scrollToBottom();
    };

    const typeWriter = (element, text) => {
        let i = 0;
        const speed = 8; // Speed of character reveal
        const total = text.length;
        
        const renderLoop = setInterval(() => {
            if (i < total) {
                const char = text[i];
                i++;
                
                // Smart partial rendering
                if (char === ' ' || i % 10 === 0 || i === total) {
                    element.innerHTML = marked.parse(text.substring(0, i));
                    scrollToBottom();
                }
            } else {
                clearInterval(renderLoop);
                element.innerHTML = marked.parse(text);
                finishRendering(element.closest('.message-row'));
                scrollToBottom();
            }
        }, speed);
    };

    const finishRendering = (row) => {
        row.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    };

    const showTyping = () => {
        const row = document.createElement('div');
        row.className = 'message-row assistant animate-message';
        row.innerHTML = `
            <div class="avatar-wrapper">
                <div class="avatar"><i class="fas fa-robot"></i></div>
            </div>
            <div class="message-content">
                <div class="bubble typing">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        `;
        chatMessages.appendChild(row);
        scrollToBottom();
        return row;
    };

    // Initial Load
    loadHistory();
});
