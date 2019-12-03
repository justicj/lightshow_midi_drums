#! /usr/bin/python3
import sys, pygame, pygame.midi

# set up pygame
pygame.init()
pygame.midi.init()

# list all midi devices
for x in range( 0, pygame.midi.get_count() ):
    print(pygame.midi.get_device_info(x))
'''
(b'MMSystem', b'Microsoft MIDI Mapper', 0, 1, 0)
(b'MMSystem', b'Alesis DM6', 1, 0, 0)
(b'MMSystem', b'Microsoft GS Wavetable Synth', 0, 1, 0)
(b'MMSystem', b'Alesis DM6', 0, 1, 0)
'''

snare = [201, 81, 0, 0]
tom = [153, 22, 0, 0]
tom_medium = [153, 23, 0, 0]
tom_floor = [153, 24, 0, 0]
hi_hat = [201, 85, 0, 0]
crash = [201, 83, 0, 0]
ride = [201, 84, 0, 0]
bass = [201, 80, 0, 0]
# open a specific midi device
inp = pygame.midi.Input(1)

# run the event loop
while True:
    if inp.poll():
    # no way to find number of messages in queue
    # so we just specify a high max
        midi_out = inp.read(1000)
        # print(midi_out)
        if any(snare in x for x in midi_out):
            print('Snare')
        elif any(tom in x for x in midi_out):
            print('Tom')
        elif any(tom_medium in x for x in midi_out):
            print('Tom Medium')
        elif any(hi_hat in x for x in midi_out):
            print('Hit-Hat')
        elif any(tom_floor in x for x in midi_out):
            print('Tom Floor')
        elif any(crash in x for x in midi_out):
            print('Crash')
        elif any(ride in x for x in midi_out):
            print('Ride')
        elif any(bass in x for x in midi_out):
            print('Bass')

    # wait 10ms - this is arbitrary, but wait(0) still resulted
    # in 100% cpu utilization
    pygame.time.wait(10)
