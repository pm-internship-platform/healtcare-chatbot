const apiBase = "http://127.0.0.1:8000/api";
let token = null;
let userEmail = null;

// --- Auth ---
document.getElementById("register-btn").onclick = async () => {
    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const res = await fetch(`${apiBase}/auth/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, username, password})
    });
    const data = await res.json();
    document.getElementById("auth-message").innerText = JSON.stringify(data);
}

document.getElementById("login-btn").onclick = async () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const res = await fetch(`${apiBase}/auth/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });
    const data = await res.json();
    if (data.access_token) {
        token = data.access_token;
        userEmail = data.user.email;
        document.getElementById("auth-section").style.display = "none";
        document.getElementById("chat-section").style.display = "block";
        document.getElementById("survey-section").style.display = "block";
    } else {
        document.getElementById("auth-message").innerText = JSON.stringify(data);
    }
}

// --- Chat ---
document.getElementById("send-btn").onclick = async () => {
    const message = document.getElementById("chat-input").value;
    const provider = document.getElementById("provider").value;
    const res = await fetch(`${apiBase}/chat/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message, provider})
    });
    const data = await res.json();
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class="chat-message user"><b>You:</b> ${message}</div>`;
    chatBox.innerHTML += `<div class="chat-message bot"><b>Bot:</b> ${data.reply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
    document.getElementById("chat-input").value = "";
}

// --- Survey ---
document.getElementById("submit-survey").onclick = async () => {
    let answers;
    try { answers = JSON.parse(document.getElementById("survey-answers").value); }
    catch { 
        document.getElementById("survey-message").innerText = "Invalid JSON!";
        return;
    }
    const res = await fetch(`${apiBase}/survey/submit`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({user_id: userEmail, answers})
    });
    const data = await res.json();
    document.getElementById("survey-message").innerText = JSON.stringify(data);
}

// --- Logout ---
document.getElementById("logout-btn").onclick = () => {
    token = null;
    userEmail = null;
    document.getElementById("auth-section").style.display = "block";
    document.getElementById("chat-section").style.display = "none";
    document.getElementById("survey-section").style.display = "none";
    document.getElementById("auth-message").innerText = "";
}
