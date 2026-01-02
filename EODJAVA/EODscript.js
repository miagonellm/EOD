const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

/**
 * Parse code blocks from Ego's responses
 *
 * WHAT THIS DOES:
 * Looks for markdown-style code blocks: ```python\ncode\n```
 * Splits response into text chunks and code chunks
 * Returns array of {type: 'text'|'code', content: '...', language: 'python'}
 *
 * WHY REGEX:
 * ```(\w+)?[\s\n]+([\s\S]*?)```
 * - (\w+)? captures language (optional, like 'python')
 * - [\s\n]+ allows for whitespace/newlines (flexible)
 * - [\s\S]*? captures everything including newlines (non-greedy)
 * - The ? makes it match shortest possible (prevents eating multiple blocks)
 *
 * FIXED: Added [\s\n]+ to handle varying whitespace after language/backticks
 * This handles cases like:
 * - ```python\ncode```
 * - ``` python \ncode```
 * - ```\ncode``` (no language)
 */
function parseCodeBlocks(text) {
    // More flexible regex that handles whitespace variations
    const codeBlockRegex = /```(\w+)?[\s\n]+([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
        // Add text before code block
        if (match.index > lastIndex) {
            parts.push({
                type: 'text',
                content: text.slice(lastIndex, match.index)
            });
        }

        // Add code block
        parts.push({
            type: 'code',
            language: match[1] || 'python',  // Default to python if no language specified
            content: match[2].trim()  // trim() removes leading/trailing whitespace
        });

        lastIndex = match.index + match[0].length;
    }

    // Add remaining text after last code block
    if (lastIndex < text.length) {
        parts.push({
            type: 'text',
            content: text.slice(lastIndex)
        });
    }

    return parts.length > 0 ? parts : [{type: 'text', content: text}];
}

/**
 * Execute code via backend
 *
 * WHY ASYNC:
 * fetch() returns a Promise - we need to await the result
 * This lets UI stay responsive while code runs
 */
async function executeCode(code, language) {
    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, language })
        });

        const data = await response.json();
        return data;
    } catch (error) {
        return { error: 'execution failed' };
    }
}

/**
 * Create a styled code block with RUN and COPY buttons
 *
 * WHY btoa():
 * btoa() encodes to base64 - lets us store code in HTML data attributes
 * without escaping issues. atob() decodes it back when button clicked.
 *
 * STRUCTURE:
 * <div class="code-block-container">
 *   <div class="code-block-header">  // Language label + buttons
 *   <pre><code>                      // Actual code
 * </div>
 */
function createCodeBlock(code, language) {
    const codeContainer = document.createElement('div');
    codeContainer.className = 'code-block-container';

    const header = document.createElement('div');
    header.className = 'code-block-header';
    header.innerHTML = `
        <span class="code-language">${language}</span>
        <button class="code-run-btn" data-code="${btoa(code)}" data-lang="${language}">RUN</button>
        <button class="code-copy-btn" data-code="${btoa(code)}">COPY</button>
    `;

    const codeBlock = document.createElement('pre');
    const codeEl = document.createElement('code');
    codeEl.className = `language-${language}`;
    codeEl.textContent = code;
    codeBlock.appendChild(codeEl);

    codeContainer.appendChild(header);
    codeContainer.appendChild(codeBlock);

    return codeContainer;
}

/**
 * Add message to chat
 *
 * FOR EGO MESSAGES:
 * Parse for code blocks, create separate styled blocks
 *
 * FOR USER MESSAGES:
 * Just plain text
 */
function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;

    if (sender === 'ego') {
        const parts = parseCodeBlocks(text);
        parts.forEach(part => {
            if (part.type === 'text' && part.content.trim()) {
                const textNode = document.createElement('div');
                textNode.className = 'message-text';
                textNode.textContent = part.content;
                msgDiv.appendChild(textNode);
            } else if (part.type === 'code') {
                msgDiv.appendChild(createCodeBlock(part.content, part.language));
            }
        });
    } else {
        msgDiv.textContent = text;
    }

    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Event delegation for code buttons
 *
 * WHY EVENT DELEGATION:
 * Instead of adding listeners to every button, we add ONE listener
 * to the container and check what was clicked. More efficient when
 * you have many dynamically created buttons.
 */
chatContainer.addEventListener('click', async (e) => {
    // Handle RUN button
    if (e.target.classList.contains('code-run-btn')) {
        const code = atob(e.target.dataset.code);  // Decode from base64
        const lang = e.target.dataset.lang;

        e.target.textContent = 'RUNNING...';
        e.target.disabled = true;

        const result = await executeCode(code, lang);

        // Add execution result below code block
        const resultDiv = document.createElement('div');
        resultDiv.className = 'code-output';
        if (result.error) {
            resultDiv.innerHTML = `<span class="output-error">ERROR: ${result.error}</span>`;
        } else {
            resultDiv.innerHTML = `<span class="output-success">OUTPUT:</span>\n${result.output || '(no output)'}`;
        }

        e.target.closest('.code-block-container').appendChild(resultDiv);
        e.target.textContent = 'RUN';
        e.target.disabled = false;

        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Handle COPY button
    if (e.target.classList.contains('code-copy-btn')) {
        const code = atob(e.target.dataset.code);
        navigator.clipboard.writeText(code);
        e.target.textContent = 'COPIED';
        setTimeout(() => {
            e.target.textContent = 'COPY';
        }, 2000);
    }
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        const reply = data.choices[0].message.content;
        addMessage(reply, 'ego');
    } catch (error) {
        addMessage('connection failed. try again.', 'ego');
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
