#!/usr/bin/env python3.5

# The GPIO's you want to control, in BCM numbers
GPIO_LIST = [4, 17, 18, 22, 23, 24, 25, 27,]
# Which port the server should operate at
PORT = 8080


from RPi import GPIO
import asyncio
from aiohttp import web

# Set the gpios for output
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_LIST, GPIO.OUT, initial=0)

# The part that handles the http request
def handle_request(req):
    # Fetching the gpio number and state with error checking
    try:
        gpio = int(req.match_info['gpio'])
    except ValueError:
        return web.Response(text="This GPIO is not a number")
    if gpio not in GPIO_LIST:
        return web.Response(text="This GPIO has not been set up")

    true_vals = ["1", "true", "on"]
    false_vals = ["0", "false", "off"]
    if req.match_info['state'].lower() in true_vals:
        state = True
    elif req.match_info['state'].lower() in false_vals:
        state = False
    else:
        return web.Response(text="This state is not a boolean")

    # Update the actual gpio
    print("Setting GPIO {} to {}".format(gpio, state))
    GPIO.output(gpio, state)
    return web.Response(text="GPIO change successfull")

# Set up the webserver
app = web.Application()
app.router.add_get("/{gpio}/{state}", handle_request)
loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, "0.0.0.0", PORT)
print("Server is waiting for requests")

# Run until ctrl+c
asyncio.ensure_future(f)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

