import socketio

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins = [], # this is left blanck so that fastapi can handle the cors on its own
)

sio_app = socketio.ASGIApp(
    socketio_server = sio_server,
    socketio_path = 'sockets'
)

@sio_server.event
async def connect(sid , environ):
    print(f'the connection has been established for the sid {sid}')
    await sio_server.emit('join' , {'sid' : sid}) 

@sio_server.event
async def disconnect(sid):
    print(f'the sid {sid} as been disconnected')