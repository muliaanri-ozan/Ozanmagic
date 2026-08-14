from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

# Jalur untuk HP Penonton (Halaman Utama / Battery)
@app.get("/")
async def get_audience_page():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Jalur untuk Halaman iPhone Storage Palsu
@app.get("/storage")
async def get_storage_page():
    with open("storage.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Jalur untuk Halaman Galeri Palsu
@app.get("/gallery")
async def get_gallery_page():
    with open("gallery.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Jalur untuk HP Controller (Remote Ozan)
@app.get("/controller")
async def get_controller_page():
    with open("controller.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Jalur Komunikasi Gaib (WebSocket)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)