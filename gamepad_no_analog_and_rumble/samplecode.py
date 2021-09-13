#GP 2 to gp 7
from PiPyPS2.PIPS2 import *
from PiPyPS2.PiPyPS2Codes import *

import usb_hid
import time,sys
import digitalio
import board
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse
from adafruit_hid.hid_gamepad import Gamepad
gamepad = Gamepad(usb_hid.devices)

def range_map(x,in_min,in_max,out_min,out_max):  return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# led will switch on the onboard led indicating the pi is powered on. this can be commented out if prefered
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = True
 
KEYBOARD = 0
CONTROLLER = 1

# choose between KEYBOARD and CONTROLLER. note that Controller is deprecated in the libraries and will not work on most OS's 
MODE = CONTROLLER

keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

button_status = [False for _ in range(9)]
button_status2 = [False for _ in range(9)]

# Create a PIPS2 object
pips2 = PIPS2()
nextRead = READDELAYMS

# Following Code will try to initialise the controller
a = pips2.initializeController(2,3,4,5,6) # the arguments here do not change anything at the moment. but TODO is to implement GPio mapping with arguments
if not a:
    print("%s: Failed to configure gamepad\nController is not responding.\nExiting ...\n")
    sys.exit()
returnVal = pips2.reInitializeController1(ANALOGMODE);
if (returnVal == -1):
    print("%s: Invalid Mode\n",);
    sys.exit()
elif (returnVal == -2):
    print("%s: Took too many tries to reinit.\n",)
    sys.exit()
sleep_us(50)
print("Control mode {}\n".format(pips2.PS2data[1]))
prev = [0,0] #holds the previous value for joystick
while (1):
    if (time.monotonic() * 1000  > nextRead):
        # you can use the data from the left joystick {7 and 8} but here we will use only right joystick{5 and 6}
        amouse = [pips2.PS2data[5], pips2.PS2data[6],pips2.PS2data[7], pips2.PS2data[8]] 
        # check if the joystick is drifting
        move = [0,0]
        move[0] =  0 if abs(amouse[0] - prev[0]) < 2 else amouse[0] - 126
        move[1] =  0 if abs(amouse[1] - prev[1]) < 2 else amouse[1] - 126
        # move the mouse to the intended direction
        #mouse.move(x=move[0],y=move[1])
        prev = amouse
       # print(amouse)
        nextRead += READDELAYMS
        # Read the controller.
        pips2.readPS2();
        # reading each button. 
        for button in buttons:
             button_status[button] = False if (CHK(pips2.PS2data[3], button)) else True
        for button in buttons2:
             button_status2[button] = False if (CHK(pips2.PS2data[4], button)) else True
        if MODE == KEYBOARD:
            press_buttons = []
            release_buttons = []
            for x in buttons:
                if button_status[x]:
                    press_buttons.append(keyboardCodes1[x])
                else:
                    release_buttons.append(keyboardCodes1[x])
            for x in buttons2:
                if button_status2[x]:
                    press_buttons.append(keyboardCodes2[x])
                else:
                    release_buttons.append(keyboardCodes2[x])
            keyboard.press(*press_buttons)
            keyboard.release(*release_buttons)
 #TODO : finish example for windows
        elif MODE == CONTROLLER:
            for x in buttons:
                if button_status[x]:
                    gamepad.release_buttons(x + 1)
                else:
                    gamepad.press_buttons(x + 1)
            for x in buttons2:
                if button_status2[x]:
                    gamepad.release_buttons(x + 1 + 8)
                else:
                    gamepad.press_buttons(x + 1 + 8)
            
            x = range_map(amouse[0], 0, 255, -127, 127)
            y = range_map(amouse[1], 0, 255, -127, 127)
            x2 = range_map(amouse[2], 0, 255, -127, 127)
            y2 = range_map(amouse[3], 0, 255, -127, 127)
            gamepad.move_joysticks(x,y,x2,y2)
            
