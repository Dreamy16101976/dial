# 3G modem watchdog

This program is designed to reconnect the modem to the Internet through a dial-up connection if it is violated.
I have observed cases where a long-existing connection (for example, a modem in a smart home system) is formally supported, but data is not transmitted. This little program will help correct the situation.

## Usage
```
python dial.py [-t timeout] [-h host] [-c connection]
```
* timeout - pause between pings in seconds
* host - host IP for ping
* connection - name of Internet connection

*Example:*
```
python dial.py -t 1000 -h 8.8.8.8 -c Internet
```

By default timeout is 5 minutes, host IP is 1.1.1.1, connection name is Internet.
