document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const suggestedQuestions = document.querySelector('.suggested-questions');

    console.log("chatMessages:", chatMessages);
    console.log("messageInput:", messageInput);
    console.log("sendButton:", sendButton);
    console.log("suggestedQuestions:", suggestedQuestions);

    sendButton.addEventListener('click', sendMessage);

    // Add event listener for "Enter" key
    messageInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior (newline)
            sendMessage();
        }
    });

    // Event listener for suggested questions
    suggestedQuestions.addEventListener('click', function(event) {
        if (event.target.tagName === 'BUTTON') {
            messageInput.value = event.target.dataset.question;
            // Automatically send the message when a suggestion is clicked
            sendMessage();
        }
    });

    function sendMessage() {
        console.log("sendMessage function called!");
        const message = messageInput.value;
        console.log("Message value:", message);
        
        if (message.trim() === '') {
            console.log("Message is empty, returning");
            return;
        }

        appendMessage('user-message', message);
        messageInput.value = '';

        console.log("Sending request to /api/chat");
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            console.log("Response received:", response);
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);

            if (data.response) {
                appendMessage('bot-message', data.response);
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
        console.log("appendMessage function called, adding:", senderClass, message);
        const messageDiv = document.createElement('div');
        messageDiv.classList.add(senderClass);

        // Use innerHTML to render the styled HTML from the backend
        messageDiv.innerHTML = message;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});