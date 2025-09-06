// frontend/js/chat.js
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const voiceBtn = document.getElementById('voice-btn');
const languageToggle = document.getElementById('language-toggle');
const quickActionBtns = document.querySelectorAll('.quick-action-btn');

let currentLanguage = 'en';
const languages = {
    'en': 'English',
    'or': 'Odia',
    'hi': 'Hindi'
};

let recognition = null;
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        sendMessage(transcript);
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        addMessage('Sorry, I didn’t catch that. Please try again.', false);
    };
} else {
    voiceBtn.disabled = true;
    voiceBtn.title = 'Speech recognition not supported in your browser';
}

languageToggle.addEventListener('click', () => {
    const languageKeys = Object.keys(languages);
    const currentIndex = languageKeys.indexOf(currentLanguage);
    const nextIndex = (currentIndex + 1) % languageKeys.length;
    currentLanguage = languageKeys[nextIndex];
    
    languageToggle.textContent = languages[currentLanguage];
    addMessage(`Language changed to ${languages[currentLanguage]}`, false);
});

sendBtn.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        sendMessage(message);
        userInput.value = '';
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const message = userInput.value.trim();
        if (message) {
            sendMessage(message);
            userInput.value = '';
        }
    }
});

voiceBtn.addEventListener('click', () => {
    if (recognition) {
        recognition.lang = currentLanguage === 'en' ? 'en-IN' : 
                          currentLanguage === 'hi' ? 'hi-IN' : 'or-IN';
        
        try {
            recognition.start();
            voiceBtn.classList.add('bg-green-200');
            
            recognition.onend = () => {
                voiceBtn.classList.remove('bg-green-200');
            };
        } catch (error) {
            console.error('Speech recognition start failed:', error);
        }
    }
});

quickActionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-query');
        sendMessage(query);
    });
});

function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat ${isUser ? 'chat-end' : 'chat-start'}`;
    
    if (!isUser) {
        messageDiv.innerHTML = `
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img src="assets/bot-avatar.png" alt="Health Assistant" />
                </div>
            </div>
        `;
    }
    
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${isUser ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-800'}`;
    bubble.textContent = text;
    
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    if (!isUser && currentLanguage !== 'en') {
        speakText(text, currentLanguage);
    }
}

async function sendMessage(message) {
    addMessage(message, true);
    
    try {
        const typingIndicator = document.createElement('div');
        typingIndicator.id = 'typing-indicator';
        typingIndicator.className = 'chat chat-start';
        typingIndicator.innerHTML = `
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img src="assets/bot-avatar.png" alt="Health Assistant" />
                </div>
            </div>
            <div class="chat-bubble bg-gray-200 text-gray-800">
                <div class="flex items-center">
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce mr-1"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce mr-1" style="animation-delay: 0.2s"></div>
                    <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message, 
                language: currentLanguage 
            }),
        });
        
        document.getElementById('typing-indicator')?.remove();
        
        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }
        
        const data = await response.json();
        addMessage(data.response, false);
        
    } catch (error) {
        console.error('Error sending message:', error);
        
        document.getElementById('typing-indicator')?.remove();
        
        if (!navigator.onLine) {
            const cachedResponse = await getCachedResponse(message);
            if (cachedResponse) {
                addMessage(cachedResponse, false);
                return;
            }
        }
        
        addMessage('Sorry, I’m experiencing technical difficulties. Please try again later.', false);
    }
}

async function speakText(text, lang) {
    if (!text) return;
    
    try {
        // Stop any ongoing audio
        if (window.currentAudio) {
            window.currentAudio.pause();
            window.currentAudio.currentTime = 0;
            URL.revokeObjectURL(window.currentAudio.src);
            window.currentAudio = null;
        }
        
        // Call backend TTS service
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text.substring(0, 200), // Limit text length for TTS
                language: lang
            }),
        });
        
        if (!response.ok) {
            throw new Error(`TTS service failed with status ${response.status}`);
        }
        
        const audioData = await response.blob();
        const audioUrl = URL.createObjectURL(audioData);
        
        // Create and play audio
        const audio = new Audio(audioUrl);
        window.currentAudio = audio;
        
        audio.onended = () => {
            URL.revokeObjectURL(audioUrl);
            window.currentAudio = null;
        };
        
        audio.onerror = (e) => {
            console.error('Audio playback error:', e);
            URL.revokeObjectURL(audioUrl);
            window.currentAudio = null;
        };
        
        await audio.play();
        
    } catch (error) {
        console.error('TTS error:', error);
        addMessage('Sorry, I couldn’t play the audio response. Please try again.', false);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (!navigator.onLine) {
        document.getElementById('offline-indicator').classList.remove('hidden');
    }
    
    window.addEventListener('online', () => {
        document.getElementById('offline-indicator').classList.add('hidden');
    });
    
    window.addEventListener('offline', () => {
        document.getElementById('offline-indicator').classList.remove('hidden');
    });
});