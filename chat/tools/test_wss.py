import asyncio
import websockets

async def test_websocket():
    #uri = "wss://your-domain/ws/some_path/"
    uri = "ws://localhost:8000/ws/chat_interfon2/"
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, WebSocket!")
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(test_websocket())
