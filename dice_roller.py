#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import random
import logging
import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.DEBUG)

#define pins on the display
BUTTON_PIN1 = 5
BUTTON_PIN2 = 6
BUTTON_PIN3 = 13
BUTTON_PIN4 = 19
Debounce = 0.02

#define screen resolution
h = 264
w = 176

#set up the buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#init the screen to clear it out
epd = epd2in7.EPD()
epd.init()
epd.Clear()

def DEMO():
    epd.init()
    logging.info("loading the don_doge.bmp")
    Himage = Image.open("don_doge.bmp")
    epd.display(epd.getbuffer(Himage))
    epd.sleep()

def diceroll(faces):
    epd.init()
    output = (random.randint(0,faces - 1))+1
    body = ImageFont.truetype('Oswald.ttf', 48)
    image = Image.new(mode='1', size=(w,h), color=128)
    draw = ImageDraw.Draw(image)
    draw.text((70, 80), str(output), font=body, align='center', fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()
    return output

def facecount():
    print("waiting half a second to debounce")
    time.sleep(.5)
    epd.init()
    body = ImageFont.truetype('Oswald.ttf',24)
    image = Image.new(mode='1', size=(w,h), color=255)
    draw = ImageDraw.Draw(image)
    draw.text((1,160), "Choose a dice", font=body, align='left', fill=0)
    draw.text((1,190), "20     6     10   exit", font=body, align='left', fill=0)
    epd.display(epd.getbuffer(image))
    while True:
        print("awaiting input button")
        time.sleep(Debounce)
        if not GPIO.input(BUTTON_PIN1):
            print("button 1")
            faces = 20
            print(diceroll(faces))
            return()
        if not GPIO.input(BUTTON_PIN2):
            print("button 2")
            faces = 6
            print(diceroll(faces))
            return()
        if not GPIO.input(BUTTON_PIN3):
            print("button 3")
            faces = 10
            print(diceroll(faces))
            return()
        if not GPIO.input(BUTTON_PIN4):
            print("button 4")
            return()
        
while True:
    time.sleep(Debounce)
    if not GPIO.input(BUTTON_PIN1):
        facecount()
    if not GPIO.input(BUTTON_PIN2):
        DEMO()
    if not GPIO.input(BUTTON_PIN3):
        epd.init()
        epd.Clear(0xFF)
    if not GPIO.input(BUTTON_PIN4):
        exit()
