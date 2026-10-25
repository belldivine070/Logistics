document.addEventListener("DOMContentLoaded", function () {
    const chatToggle = document.getElementById('chat-toggle-btn');
    const chatBox = document.getElementById('chat-box');
    const chatClose = document.getElementById('chat-close-btn');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send-btn');
    const messagesContainer = document.getElementById('chat-messages');

    if (!chatToggle) return;

    let ws = null;
    let isClosedByUser = false;

    // Retrieve or generate persistent session identifier
    let conversationId = localStorage.getItem('chat_session_id') || 'session-' + Math.random().toString(36).substring(2, 9);
    localStorage.setItem('chat_session_id', conversationId);

    // Open Chat
    chatToggle.addEventListener('click', () => {
        isClosedByUser = false;
        chatBox.classList.remove('hidden');
        chatToggle.classList.add('hidden');
        initWebSocket();
    });

    // Close Chat
    chatClose.addEventListener('click', () => {
        isClosedByUser = true;
        chatBox.classList.add('hidden');
        chatToggle.classList.remove('hidden');
        if (ws) {
            ws.close();
            ws = null;
        }
    });

    function initWebSocket() {
        if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
            return;
        }

        const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = `${wsProtocol}${window.location.host}/ws/chat/${conversationId}/`;

        ws = new WebSocket(wsUrl);

        ws.onmessage = function (event) {
            try {
                const data = JSON.parse(event.data);
                appendMessage(data.message, data.sender_type);
            } catch (e) {
                console.error("Error parsing WebSocket payload:", e);
            }
        };

        ws.onclose = function () {
            // Reconnect only if the chat box is open and wasn't closed by user action
            if (!isClosedByUser) {
                console.log('WebSocket disconnected. Attempting reconnect in 3s...');
                setTimeout(initWebSocket, 3000);
            }
        };

        ws.onerror = function (err) {
            console.error('WebSocket encountered an error:', err);
        };
    }

    function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                'message': text,
                'sender_type': 'CUSTOMER'
            }));
            chatInput.value = '';
        } else {
            console.warn('Cannot send message: WebSocket connection is not open.');
        }
    }

    chatSend.addEventListener('click', sendMessage);
    
    chatInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevent default line breaks or form submit
            sendMessage();
        }
    });

    function appendMessage(text, senderType) {
        const isSupport = senderType === 'SUPPORT' || senderType === 'ADMIN';
        const div = document.createElement('div');
        div.className = `flex flex-col ${isSupport ? 'items-start' : 'items-end'}`;

        div.innerHTML = `
            <div class="max-w-[80%] px-3.5 py-2.5 rounded-xl text-xs sm:text-sm leading-relaxed ${
                isSupport 
                    ? 'bg-white text-gray-800 border border-gray-200 shadow-sm rounded-bl-none' 
                    : 'bg-blue-600 text-white rounded-br-none'
            }">
                ${escapeHtml(text)}
            </div>
        `;
        messagesContainer.appendChild(div);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function escapeHtml(string) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
        return String(string).replace(/[&<>"']/g, function (m) { return map[m]; });
    }
});