import argparse
import random
import requests
import serial
import subprocess
import threading
import time


PINS = ['2', '4', '5', '6', '7']
POURING = {p: False for p in PINS}

BUTTON = '3'
VALVES = ['2', '4', '5']
PUMPS = ['6', '7']

# Shots take 6 secs to pour from pumps, 7 from valves.
SHOT_DURATION = {p: 6 for p in PUMPS}
SHOT_DURATION.update({v: 7 for v in VALVES})

PEACH = '5'
VODKA = '7'
BLUE = '2'
CRAN = '6'
OJ = '4'


# Keys are the node server's possible responses.
# Each denotes a different cocktail.
DRINK_LIST = {
    "01000": {VODKA: 1, BLUE: 0.5, CRAN: 2},
    "02000": {BLUE: 1.25, OJ: 2.25, PEACH: 0.75},
    "03000": {VODKA: 0.75, OJ: 2, CRAN: 2, PEACH: 0.75},
    "04000": {VODKA: 1, OJ: 2, CRAN: 1, PEACH: 1},
    "05000": {VODKA: 1, OJ: 3},
    "06000": {VODKA: 1, BLUE: 0.5, OJ: 1, CRAN: 2},
    "07000": {VODKA: 1, OJ: 1, CRAN: 2},
    "08000": {VODKA: 1, CRAN: 3},
    "10000": {VODKA: 1},
    "11000": {VODKA: 0.5, PEACH: 0.5},
    "00001": {OJ: 1, CRAN: 3}
    }


ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
toggle = ser.write


def setup():
    connected = False

    while not connected:
        serin = ser.read()
        print "Connected to Arduino! read: ", serin
        connected = True


def runTests():
    """
    *** Robust unit tests ***
    Turn everything on and off to make sure this works.
    """
    print "Stop pulsing and turn on button light"
    toggle('3')
    time.sleep(0.25);
    print "Testing 2 (valve)"
    toggle('2')
    time.sleep(2)
    toggle('2')
    time.sleep(0.5)
    print "Testing 4 (valve)"
    toggle('4')
    time.sleep(2)
    toggle('4')
    time.sleep(0.5)
    print "Testing 5 (valve)"
    toggle('5')
    time.sleep(2)
    toggle('5')
    time.sleep(0.5)
    print "Testing 6 (pump)"
    toggle('6')
    time.sleep(1)
    toggle('6')
    time.sleep(0.5)
    print "Testing 7 (pump)"
    toggle('7')
    time.sleep(1)
    toggle('7')
    time.sleep(0.25);
    print "Start pulsing"
    toggle('3')


def pour(pin, duration):
    """
    Pours from a pin for a given duration.
    """
    print "pouring pin %s for %f seconds." % (pin, duration)
    POURING[pin] = True
    toggle(pin)
    time.sleep(duration)
    
    print "pouring pin %s finished." % pin
    toggle(pin)
    POURING[pin] = False


def pour_drink(drink_code):
    """
    Pours a cocktail. Turns off button PWM while pouring.
    """
    toggle(BUTTON)
    
    for ingredient,amount in DRINK_LIST[drink_code].iteritems():
        pour(ingredient, amount*SHOT_DURATION[ingredient])

    toggle(BUTTON)


def poll():
    """
    Polls the Heroku server for drink orders.
    """    
    while True:
        print "\nsleeping before request..."
        time.sleep(1.5)
        response = requests.get('http://shotbotserver.herokuapp.com/order')
        content = response.content

        if any(POURING.values()):
            print "already pouring something else!"
            continue

        if content == '00000':
            print "No drinks ordered!"
            continue

        elif content in DRINK_LIST:
            print "received: ", content
            #  Pour a standard cocktail...
            #  you peasant
            pour_drink(content)
        
        elif content == '111':
            print "Mixed drank."
            pour('6', 3)
            time.sleep(0.5)
            pour('7', 6)
            
        elif content == '99999':
            print "Random choice. Boldly go forth, my child"

            random_drink = random.choice(DRINK_LIST.keys())
            print "Random drink: ", random_drink
            pour_drink(random_drink)

        else:
            print 'Invalid response content:', content
            continue

###############################################################################

setup()
parser = argparse.ArgumentParser(description='ShotBot')
parser.add_argument('-p', '--poll',
                   dest='poll',
                   help='Poll server for drink orders.',
                   action='store_true',
                   default=False)
args = parser.parse_args()
if args.poll:
    poll()
