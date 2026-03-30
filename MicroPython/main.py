"""
Created by: Devon
Created on: Sep 2026
This module is a Micro:bit MicroPython program that uses a HC-SR04 sonar to find the distance of a object and will find if it's more than 10 cm away.
"""

from microbit import *
import neopixel


class HCSR04:
    def __init__(self, tpin=pin13, epin=pin14, spin=pin13):
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

        try:
            i, value = next((ind, v) for ind, v in enumerate(resp) if v)
        except StopIteration:
            i = -1

        if i > 0:
            pre = bin(value).count("1")
            try:
                k, value = next(
                    (ind, v)
                    for ind, v in enumerate(resp[i : length - 2])
                    if resp[i + ind + 1] == 0
                )
                post = bin(value).count("1") if k else 0
                k = k + i
            except StopIteration:
                i = -1

        dist = -1 if i < 0 else round(((pre + (k - i) * 8.0 + post) * 8 * 0.172) / 2)
        return dist


sonar = HCSR04()
display.show(Image.HAPPY)
myNeopixelStrip = neopixel.NeoPixel(pin16, 4)
myNeopixelStrip.clear()
myNeopixelStrip.show()

while True:
    if button_a.was_pressed():
        distance = sonar.distance_mm()

        if distance == -1:
            display.scroll("Err")
        else:
            distance_cm = distance / 10
            display.scroll(distance_cm)
            display.scroll(" cm")

            if distance_cm < 10:
                myNeopixelStrip[0] = (255, 0, 0)
                myNeopixelStrip[1] = (255, 0, 0)
                myNeopixelStrip[2] = (255, 0, 0)
                myNeopixelStrip[3] = (255, 0, 0)
            else:
                myNeopixelStrip[0] = (0, 255, 0)
                myNeopixelStrip[1] = (0, 255, 0)
                myNeopixelStrip[2] = (0, 255, 0)
                myNeopixelStrip[3] = (0, 255, 0)

            myNeopixelStrip.show()
            display.show(Image.YES)

        sleep(3000)
        myNeopixelStrip.clear()
        myNeopixelStrip.show()
        display.show(Image.HAPPY)
        