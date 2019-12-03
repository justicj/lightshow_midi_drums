#! /usr/bin/python3
import sys, pygame, pygame.midi, requests
from time import sleep

# set up pygame
pygame.init()
pygame.midi.init()

# variables
apiaddress = '192.168.1.219:8080'
apitimeout = 0.2
gpiodelay = 0.1
snare = [201, 81, 0, 0]
tom = [153, 22, 0, 0]
tom_medium = [153, 23, 0, 0]
tom_floor = [153, 24, 0, 0]
hi_hat = [201, 85, 0, 0]
crash = [201, 83, 0, 0]
ride = [201, 84, 0, 0]
bass = [201, 80, 0, 0]

# list all midi devices
for x in range( 0, pygame.midi.get_count() ):
    print(pygame.midi.get_device_info(x))
# open a specific midi device
inp = pygame.midi.Input(1)

def sendtoapi(url, gpio):
    urlon = 'http://' + url + '/' + str(gpio) + '/true'
    urloff = 'http://' + url + '/' + str(gpio) + '/false'
    print(urlon, urloff)
    try:
        r = requests.get(urlon, timeout=apitimeout)
    except requests.exceptions.ReadTimeout:
        print('Turning on, didnt make it to the api')
    except requests.exceptions.ConnectionError:
        print('Turning on, didnt make it to the api')
    except:
        raise
    sleep(gpiodelay)
    try:
        r = requests.get(urloff, timeout=apitimeout)
    except requests.exceptions.ReadTimeout:
        print('Turning off, didnt make it to the api')
    except requests.exceptions.ConnectionError:
        print('Turning off, didnt make it to the api')
    except:
        raise
    return()

def listentrigger():
    # run the event loop
    while True:
        if inp.poll():
        # no way to find number of messages in queue
        # so we just specify a high max
            midi_out = inp.read(1000)
            # print(midi_out)
            if any(snare in x for x in midi_out):
                sendtoapi(apiaddress, 4)
                print('Snare')
            elif any(tom in x for x in midi_out):
                sendtoapi(apiaddress, 17)
                print('Tom')
            elif any(tom_medium in x for x in midi_out):
                sendtoapi(apiaddress, 18)
                print('Tom Medium')
            elif any(hi_hat in x for x in midi_out):
                sendtoapi(apiaddress, 22)
                print('Hit-Hat')
            elif any(tom_floor in x for x in midi_out):
                sendtoapi(apiaddress, 23)
                print('Tom Floor')
            elif any(crash in x for x in midi_out):
                sendtoapi(apiaddress, 24)
                print('Crash')
            elif any(ride in x for x in midi_out):
                sendtoapi(apiaddress, 25)
                print('Ride')
            elif any(bass in x for x in midi_out):
                sendtoapi(apiaddress, 27)
                print('Bass')
        # wait 10ms - this is arbitrary, but wait(0) still resulted
        # in 100% cpu utilization
        pygame.time.wait(10)
    return()

listentrigger()
