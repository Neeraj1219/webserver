import asyncio
import websockets

# A set to keep track of all connected clients
connected = set()

async def handle_client(websocket, path):
    # Add the client to the set of connected clients
    connected.add(websocket)
    print(f"Client {websocket.remote_address} connected.")
    
    try:
        async for message in websocket:
            # Handle incoming messages from clients
            print(f"Received message from {websocket.remote_address}: {message}")
            # Broadcast the message to all connected clients
            await asyncio.gather(*[client.send(message) for client in connected])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Remove the client from the set of connected clients
        connected.remove(websocket)
        print(f"Client {websocket.remote_address} disconnected.")

async def start_server():
    async with websockets.serve(handle_client, "0.0.0.0", 8000):
        print("WebSocket server started.")
        await asyncio.Future()  # Run forever.

asyncio.run(start_server())
