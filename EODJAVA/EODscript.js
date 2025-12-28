async function send() {
    const input = document.getElementById("input");
    const chat = document.getElementById("chat");
   
    const msg = input.value.trim();
    if (!msg) return;
    
    chat.innerHTML += `<div class="msg user">${msg}</div>`;
    chat.scrollTop = chat.scrollHeight;
    input.value = "";
    
    try {
        const res = await fetch('/api/chat', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: msg
            })
        });
        
        const data = await res.json();
        const reply = data.choices[0].message.content;
        
        chat.innerHTML += `<div class="msg ai">${reply}</div>`;
        chat.scrollTop = chat.scrollHeight;
    } catch (error) {
        console.error('Error:', error);
        chat.innerHTML += `<div class="msg ai">Error: Could not get response</div>`;
    }
}

document.getElementById("input").addEventListener("keypress", e => {
    if (e.key === "Enter") send();
});
