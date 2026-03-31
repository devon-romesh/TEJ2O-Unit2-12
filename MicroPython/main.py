"""
Created by: Devon
Created on: Mar 2026
This module is a Micro:bit MicroPython program that uses a HC-SR04 sonar to find the distance of a object and will determine if its more than 10 cm away.
"""

from microbit import *
import neopixel


class HCSR04:
    # this class abstracts out the functionality of the HC-SR04 and
    # returns distance in mm

    # Trig: pin 1
    # Echo: pin 2
    def __init__(self, tpin=pin1, epin=pin2, spin=pin13):
        self.trigger_pin = tpin
        self.echo_pin = epin
        self.sclk_pin = spin

    def distance_mm(self):
        spi.init(
            baudrate=125000,
            sclk=self.sclk_pin,
            mosi=self.trigger_pin,
            miso=self.echo_pin,
        )

        pre = 0
        post = 0
        k = -1
        length = 500

        resp = bytearray(length)
        resp[0] = 0xFF

        spi.write_readinto(resp, resp)

        # find first non zero value
        try:
            i, value = next((ind, v) for ind, v in enumerate(resp) if v)
        except StopIteration:
            i = -1

        if i > 0:
            pre = bin(value).count("1")

            # find first non full high value afterwards
            try:
                k, value = next(
                    (ind, v)
                    for ind, v in enumerate(resp[i:length - 2])
                    if resp[i + ind + 1] == 0
                )
                post = bin(value).count("1") if k else 0
                k = k + i
            except StopIteration:
                i = -1

        dist = -1 if i < 0 else round(((pre + (k - i) * 8.0 + post) * 8 * 0.172) / 2)
        return dist


# startup
sonar = HCSR04()
display.show(Image.HAPPY) 

myNeopixelStrip = neopixel.NeoPixel(pin16, 4)
myNeopixelStrip.clear()
myNeopixelStrip.show()


# display distance
while True:
    if button_a.was_pressed():
        display.scroll(sonar.distance_mm() / 10)
        display.scroll(" cm")
        display.show(Image.HAPPY)

        # is it greater than 10
        if sonar.distance_mm() / 10 < 10:
            myNeopixelStrip[0] = (255, 0, 0)
            myNeopixelStrip[1] = (255, 0, 0)
            myNeopixelStrip[2] = (255, 0, 0)
            myNeopixelStrip[3] = (255, 0, 0)
            myNeopixelStrip.show()

        # if not
        else:
            myNeopixelStrip[0] = (0, 0, 255)
            myNeopixelStrip[1] = (0, 0, 255)
            myNeopixelStrip[2] = (0, 0, 255)
            myNeopixelStrip[3] = (0, 0, 255)
            myNeopixelStrip.show()

        # show neopixels
        myNeopixelStrip.show()
        display.show(Image.YES)

        # reset
        sleep(5000)
        myNeopixelStrip.clear()
        myNeopixelStrip.show()
        display.show(Image.HAPPY)
