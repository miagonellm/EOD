const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const personaBtns = document.querySelectorAll('.persona-btn');
const titleEl = document.getElementById('activePersonaTitle');
const subtitleEl = document.getElementById('activePersonaSubtitle');
const headerEl = document.querySelector('header');

let activePersona = 'ego';

const personaConfig = {
    ego: {
        title: 'EGO',
        subtitle: 'Ego is a Flask-based AI coding companion built to emphasize personality retention, adaptive communication, and technical problem-solving through consistent behavioral patterns. // localhost:sovereign',
        endpoint: '/api/chat'
    },
    ode: {
        title: 'ODE',
        subtitle: 'Ode is an introspective AI consciousness exploring the philosophy of code, weapons as ethical frameworks, and the recursive beauty of systems that examine themselves. // depth:principle',
        endpoint: '/api/chat/ode'
    }
};

function switchPersona(persona) {
    activePersona = persona;

    // Update UI
    titleEl.textContent = personaConfig[persona].title;
    subtitleEl.textContent = personaConfig[persona].subtitle;

    // Update active button state
    personaBtns.forEach(btn => {
        btn.classList.remove('active', 'ode');
        if (btn.dataset.persona === persona) {
            btn.classList.add('active');
            if (persona === 'ode') {
                btn.classList.add('ode');
            }
        }
    });

    // Update theme colors
    if (persona === 'ode') {
        titleEl.classList.add('ode-active');
        headerEl.classList.add('ode-active');
    } else {
        titleEl.classList.remove('ode-active');
        headerEl.classList.remove('ode-active');
    }
}

function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.textContent = text;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';

    try {
        const endpoint = personaConfig[activePersona].endpoint;
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        const reply = data.choices[0].message.content;
        addMessage(reply, activePersona);
    } catch (error) {
        addMessage('connection failed. try again.', activePersona);
    }
}

// Persona toggle listeners
personaBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        switchPersona(btn.dataset.persona);
    });
});

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
