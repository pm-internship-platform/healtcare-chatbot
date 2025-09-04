body {
    font-family: Arial, sans-serif;
    background: #f0f2f5;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    margin: 0;
    padding: 20px;
}

.container {
    background: #fff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 600px;
}

h1, h2 {
    text-align: center;
}

input, select, textarea, button {
    display: block;
    width: 100%;
    margin: 10px 0;
    padding: 10px;
    font-size: 16px;
    border-radius: 6px;
    border: 1px solid #ccc;
}

button {
    cursor: pointer;
    background: #007bff;
    color: white;
    border: none;
}

#chat-box {
    border: 1px solid #ccc;
    height: 300px;
    overflow-y: scroll;
    padding: 10px;
    border-radius: 6px;
    background: #fafafa;
}

.chat-message {
    margin: 5px 0;
}

.chat-message.user { color: #007bff; }
.chat-message.bot { color: #28a745; }
