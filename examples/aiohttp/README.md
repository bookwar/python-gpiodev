aiohttp Websocket Connection example
====================================
In this example you can control the state of a some LEDs via WebSocket.

Installation
------------
You need to install aiohttp:

```pip install aiohttp```

It is not needed for the general GPIO-lib so it is not part of the installation process.

Configuration
-------------
Make sure to switch the ip address and port number in the index.html-File to the one of your raspberry pi (line 19), so the Browser can connect to it using the WebSocket.

You can configure the GPIO-pins you like to use. See GPIO_LINES in the main.py.

Note that the fedora firewall prevents access on port 8080 by default, so allow that port to be accessed by other machines in your network e.g. `firewall-cmd --zone=dmz --add-port=8080/tcp`, take a look at the [documentation](https://docs-old.fedoraproject.org/en-US/Fedora/19/html/Security_Guide/sec-Open_Ports_in_the_firewall-CLI.html)

Additional notes
----------------
aiohttp still waits for a request when you press CTRL+c to stop it, so you need to refresh the page after pressing CTRL+c to stop the server.
