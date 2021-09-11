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

# led will switch on the onboard led indicating the pi is powered on. this can be commented out if prefered
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = True
 
KEYBOARD = 0
CONTROLLER = 1

# choose between KEYBOARD and CONTROLLER. note that Controller is deprecated in the libraries and will not work on most OS's 
MODE = KEYBOARD

keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

buttons = {BTN_SELECT : 'select', BTN_LEFT_JOY : 'left joystick button', BTN_RIGHT_JOY : 'right joystick button', BTN_START : 'start', BTN_UP : 'up', BTN_DOWN : 'down', BTN_LEFT : 'left', BTN_RIGHT : 'right'}
buttons2 = {BTN_L2 : 'L2', BTN_R2 : 'R2', BTN_L1 : 'L1',BTN_R1 : 'R1', BTN_TRIANGLE : 'triangle', BTN_CIRCLE : 'circle',BTN_X : 'X', BTN_SQUARE : 'Square'}
keyboardCodes1 = {BTN_SELECT : Keycode.SPACEBAR, BTN_LEFT_JOY : Keycode.Q, BTN_RIGHT_JOY : Keycode.E, BTN_START : Keycode.ESCAPE, BTN_UP : Keycode.W, BTN_DOWN : Keycode.S, BTN_LEFT : Keycode.A, BTN_RIGHT : Keycode.D}
keyboardCodes2 = {BTN_L2 : Keycode.R, BTN_R2 : Keycode.T, BTN_L1 : Keycode.F,BTN_R1 : Keycode.G, BTN_TRIANGLE : Keycode.I, BTN_CIRCLE : Keycode.O,BTN_X : Keycode.K, BTN_SQUARE : Keycode.L}

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
        mouse.move(x=move[0],y=move[1])
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
                if button_status[button_status[x]] == True:
                    gamepad.release_buttons(x + 1)
                else:
                    gamepad.press_buttons(x + 1)
            for x in buttons2:
                if button_status[button_status[x]] == True:
                    gamepad.release_buttons(x + 1 + 8)
                else:
                    gamepad.press_buttons(x + 1 + 8)


