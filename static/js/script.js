const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

console.log("chatMessages:", chatMessages); //Check if elements are being targeted correctly
console.log("messageInput:", messageInput);
console.log("sendButton:", sendButton);


sendButton.addEventListener('click', sendMessage);

function sendMessage() {
    console.log("sendMessage function called!"); //Check if function is called
    const message = messageInput.value;
    console.log("Message value:", message); //Check message value
    if (message.trim() === '') {
        console.log("Message is empty, returning");  // Check if it returns due to empty
        return;
    }

    appendMessage('user-message', message);
    messageInput.value = '';

    fetch('/chat', {  // Your Flask backend endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data); //Log the response

        if (data.response) {
            appendMessage('bot-message', data.response);  // Use the styled response
        } else if (data.error) {
            appendMessage('bot-message', `Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('bot-message', 'Sorry, an error occurred.');
    });
}

function appendMessage(senderClass, message) {
    console.log("appendMessage function called!");//Check if append message is called
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(senderClass);

    // Use innerHTML to render the styled HTML from the backend
    messageDiv.innerHTML = message;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
}