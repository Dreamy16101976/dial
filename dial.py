'''
dial.py

3G modem watchdog

Copyright (C) 2019 Alexey 'FoxyLab' Voronin

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
'''
import time
import os
import sys
import getopt
import signal

# default settings
CONN = 'Internet' # name of Internet connection
TIMEOUT = 5*60 # timeout
HOST = '1.1.1.1' # pinged host

def type(text):
    ''' Print string

        Arguments:
            text - printed string
    '''
    sys.stdout.write(text)
    sys.stdout.flush()
    
def reconnect(conn):
    ''' Disconnect & connect

        Arguments:
            conn - name of Internet connection
    '''
    # disconnect
    type('\nDisconnect...\n'),
    while (True):
        code = os.system(r'RASDIAL %s /DISCONNECT' % conn)
        if (code == 0):
            break
        sleep(1)
    type('O.K.\n')
    # connect
    type('Connect...\n'),
    while (True):
        code = os.system(r'RASDIAL %s' % conn)
        if (code == 0):
            break
    type('O.K.\n')
    return

def quit(signum, frame):
    ''' Handling CTRL-C
    '''
    print('Program terminated by user')
    sys.exit()


def main(argv):
    type('3G modem watchdog (C) FoxyLab 2019\n')
    # OS check
    try:
        sys.getwindowsversion()
    except AttributeError:
        type('This program is intended for Microsoft Windows\n')        
    # default settings
    conn = CONN
    timeout = TIMEOUT
    host = HOST
    # arguments read
    try:
        opts, args = getopt.getopt(argv,'hc:t:i:')
    except getopt.GetoptError:
          print('python dial.py -c <connection> -t <timeout in secs> -h <host IP>')
          sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python dial.py -c <connection> -t <timeout in secs> -i <host IP>')
            sys.exit()        
        if opt == "-c":
            conn = arg         
        if opt == "-t":
            try:
                timeout = int(arg)
            except ValueError:
                print('Timeout must be number')
                sys.exit(2)
        if opt == "-i":
            host = arg
    signal.signal(signal.SIGINT, quit) # CTRL-C handler
    # main loop
    while (True):
        code = os.system('ping '+ host + ' -n 1') # ping
        if (code != 0): # ping fail
            type('Connection lost...\n')
            reconnect(conn) # disconnect & connect
        time.sleep(timeout) # pause

if __name__ == "__main__":
    main(sys.argv[1:])