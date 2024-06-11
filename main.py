from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from nltk.chat.util import Chat, reflections

# Define the patterns and responses for the chatbot
pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hey there!", "Hi! How can I help you today?"]
    ],
    [
        r"how are you ?",
        ["I'm doing well, thank you!", "I'm great, thanks for asking!"]
    ],
    [
        r"(.*) your name ?",
        ["You can call me Chatbot.", "I go by the name Chatbot."]
    ],
    [
        r"quit",
        ["Bye, take care!", "Goodbye!", "See you later!"]
    ],
]

# Create the chatbot
def create_chatbot():
         return Chat(pairs, reflections)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }

            .chat-popup {
                display: none;
                position: fixed;
                bottom: 20px;
                right: 20px;
                border-radius: 10px;
                border: 1px solid #ccc;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                background-color: #fff;
                z-index: 1000;
            }

            .open-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 50%;
                font-size: 16px;
                width: 60px;
                height: 60px;
                cursor: pointer;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                z-index: 1001;
            }

            .chat-header {
                padding: 10px;
                background-color: #007bff;
                color: #fff;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }

            .chat-body {
                max-height: 300px;
                overflow-y: auto;
                padding: 10px;
            }

            .chat-input {
                width: calc(100% - 20px);
                padding: 10px;
                border: none;
                border-top: 1px solid #ccc;
                outline: none;
            }

            .send-button {
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 0 0 10px 10px;
                width: 100%;
                padding: 10px;
                cursor: pointer;
            }

            .close-button {
                float: right;
                background-color: transparent;
                border: none;
                color: #555;
                cursor: pointer;
                font-size: 20px;
            }
        </style>
    </head>
    <body>

    <button class="open-button" onclick="openForm()">Chat</button>

    <div class="chat-popup" id="myForm">
        <div class="chat-header">
            Chatbot
            <button class="close-button" onclick="closeForm()">&times;</button>
        </div>
        <div class="chat-body" id="chat-box"></div>
        <input type="text" placeholder="Type a message..." class="chat-input" id="message" required>
        <button type="button" class="send-button" onclick="sendMessage()">Send</button>
    </div>

    <script>
        function openForm() {
            document.getElementById("myForm").style.display = "block";
        }

        function closeForm() {
            document.getElementById("myForm").style.display = "none";
        }

        function appendMessage(user, message) {
            var chatBox = document.getElementById("chat-box");
            var p = document.createElement("p");
            p.innerHTML = "<strong>" + user + ":</strong> " + message;
            chatBox.appendChild(p);
        }

        function sendMessage() {
            var messageInput = document.getElementById("message");
            var message = messageInput.value.trim();
            if (message !== "") {
                appendMessage("You", message);
                messageInput.value = "";
                // Send message to server (or process it locally)
                fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: "message=" + encodeURIComponent(message)
                })
                .then(response => response.text())
                .then(data => {
                    appendMessage("Chatbot", data);
                })
                .catch(error => {
                    console.error("Error:", error);
                });
            }
        }
    </script>

    </body>
    </html>
    """

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    chatbot = create_chatbot()
    response = chatbot.respond(message.lower())
    return response if response else "Sorry, I didn't understand that."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


#uvicorn main:app --reload --port 8001
#http://localhost:8000