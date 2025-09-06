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
async def make_move(sid , move):
    print(f'this endpoint has been reached by the sid : {sid} with the move : {move}')
    await sio_server.emit('make_move' , {'sid' : sid ,'move' : move} , skip_sid=sid)
    print(f'the move {move} has just been broadcasted to other machines right now')

@sio_server.event
async def connect(sid , environ , auth = None):
    print(f'the connection has been established for the sid {sid}')
    await sio_server.emit('join' , {'sid' : sid , 'message': 'Connected successfully'}) 

@sio_server.event
async def disconnect(sid , environ):
    print(f'the sid {sid} as been disconnected')

@sio_server.event
async def chat(sid , message):
    await sio_server.emit('chat' , {'sid' : sid , 'message' : message})