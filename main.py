from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def get():
    return {"message": "Hello World"}

@app.get("/ws-client")
async def get_ws_client():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
        <head><title>Chat</title></head>
        <body>
            <h1>WebSocket Chat</h1>
            <input type="text" id="messageText" autocomplete="off"/>
            <button onclick="sendMessage()">Send</button>
            <ul id='messages'></ul>
            <script>
                var ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var data = JSON.parse(event.data);
                    message.textContent = data.text;
                    messages.appendChild(message);
                };
                function sendMessage() {
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = '';
                }
            </script>
        </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_json({"text": f"Message text was: {data}"})
