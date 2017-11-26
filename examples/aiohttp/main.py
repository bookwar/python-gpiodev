import os
import json
import asyncio
from aiohttp.web import (Application, Response, WebSocketResponse, WSMsgType,
                         run_app, FileResponse)

from gpiodev import GPIOHandle


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

# GPIO pin numbers for your board
GPIO_LINES = (18, 4)

gpio_led = GPIOHandle(GPIO_LINES, mode="out")


async def index_handler(request):
    '''
    send static index file
    '''
    return FileResponse('./static/index.html')


async def websocket_handler(request):
    '''
    use websocket to handle button clicks/LED changes
    '''
    resp = WebSocketResponse()
    ok, protocol = resp.can_prepare(request)
    if not ok:
        with open(WS_FILE, 'rb') as fp:
            return Response(body=fp.read(), content_type='text/html')
    await resp.prepare(request)
    try:
        # new connection - send current GPIO configuration
        led_states = gpio_led.get_values()
        resp.send_str(json.dumps({
            'states': led_states, 
            'lines': GPIO_LINES
        }))
        request.app['sockets'].append(resp)

        # async wait for new WebSocket messages
        async for msg in resp:
            if msg.type == WSMsgType.TEXT:
                led_states = gpio_led.get_values()
                data = json.loads(msg.data)
                
                # switch selected GPIO by its pin number
                if 'switch_gpio' in data:
                    led_nr = GPIO_LINES.index(data['switch_gpio'])
                    led_states[led_nr] = int(not led_states[led_nr]) 
                    gpio_led.set_values(tuple(led_states))
                
                # update LED states to all connected clients
                for ws in request.app['sockets']:
                    await ws.send_str(json.dumps({'states': led_states}))
        return resp
    finally:
        # remove disconnected connections.
        # we do not need to send them the state update anymore
        request.app['sockets'].remove(resp)


async def on_shutdown(app):
    '''
    close all connections on shutdown
    '''
    for ws in app['sockets']:
        await ws.close()


async def init(loop):
    app = Application(loop=loop)
    app['sockets'] = []
    app.router.add_route('GET', '/ws', websocket_handler)
    app.router.add_route('GET', '/', index_handler)
    app.on_shutdown.append(on_shutdown)
    return app


def main():
    # aiohttp setup
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    
    run_app(app)


if __name__ == '__main__':
    main()