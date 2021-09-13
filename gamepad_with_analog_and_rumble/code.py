# This is the sample code for the unofficial Circuitpython port of billporter's PS2 controller library for arduino. All credits go to
# Bill porter, Shutter and anyone who has contributed to this project. If you have an arduino check out
# https://github.com/madsci1016/Arduino-PS2X for the orignal source code
# this Project was made in personal interest. i have an old ps2 controller laying around, and i was too lazy to get an adapter. i figured
# i could create an adapter with a raspberry pi pico.
# The aim of this project was :
# - To create an adapter which will give input to games (mostly done. both joystick and buttons work but no analog functionality)
# - Implement the rumble feature onto the controller (this is pretty confusing since the usb_hid gamepad library is deprecated and does not support
#   rumble.)

# imports :
from PS2X.PS2X import *
import time
# Below imports need to be in the library of the microcontroller board
import digitalio
import board
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.mouse import Mouse
from adafruit_hid.hid_gamepad import Gamepad


# select desired pins according to your wiring
PS2_DAT = 2
PS2_CMD = 3
PS2_SEL = 4
PS2_CLK = 5

#Set to true if you want debug prints
DEBUG = False

KEYBOARD = 0
CONTROLLER = 1

# choose between KEYBOARD and CONTROLLER. note that Controller is deprecated in the libraries and will not work on most OS's 
MODE = KEYBOARD
# /******************************************************************
#  * select modes of PS2 controller:
#  *   - pressures = analog reading of push-butttons
#  *   - rumble    = motor rumbling
#  * change to False if you prefer them to be disabled. i leave both on since i want full functionality
#  ******************************************************************/
pressures = True
rumble = True


# right now, the library does NOT support hot pluggable controllers, meaning
# you must always either restart your Arduino after you connect the controller,
# or call config_gamepad(pins) again after connecting the controller.

ps2x = PS2X()  # create PS2 Controller Class object

# HID stuff
keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
gamepad = Gamepad(usb_hid.devices)  # initialising gamepad object

error = 0
type = 0

# The controller will measure how hard you press the L2 and R2 buttons and vibrate Left or Right based on how hard you press said side.
global vibrate1,vibrate2
vibrate1 = 0  # for left motor
vibrate2 = 0  # for right motor .

# Try configuring the gamepad and see if an error occurs.
error = ps2x.config_gamepad(
    PS2_CLK, PS2_CMD, PS2_SEL, PS2_DAT, pressures, rumble)
if(error == 0):
    print("Found Controller, configured successful, Pressures = {}, rumble = {}".format(
        pressures, rumble))
    print("Try out all the buttons, X will vibrate the controller, faster as you press harder;")
elif(error == 1):
    print("No controller found, check wiring, Set debug to True in PS2X.py. Try visiting www.billporter.info for troubleshooting tips")
elif(error == 2):
    print("Controller found but not accepting commands. Set debug to True in PS2X.py. Try visiting www.billporter.info for troubleshooting tips")
elif(error == 3):
    print("Controller refusing to enter Pressures mode, may not support it.")

# Prints the type of controller.
type = ps2x.readType()
responses = ["Unknown Controller type found", "DualShock Controller found ",
             "GuitarHero Controller found ", "Wireless Sony DualShock Controller found "]
print(responses[type])

prev = [0,0,0,0] #holds the previous value for joystick
pressed = []
def sendInputToPC(arr, jstick):
    if MODE == CONTROLLER:
        for i in range(len(arr)):
            if arr[i]:
                gamepad.press_buttons(1 + i)
            else:
                gamepad.release_buttons(1 + i)
        x = range_map(jstick[0], 0, 255, -127, 127)
        y = range_map(jstick[1], 0, 255, -127, 127)
        x2 = range_map(jstick[2], 0, 255, -127, 127)
        y2 = range_map(jstick[3], 0, 255, -127, 127)
        gamepad.move_joysticks(x, y, x2, y2)
    else:
        global prev
        move = [0,0]
        move[0] =  0 if abs(jstick[2] - prev[2]) < 2 else jstick[2] - 126
        move[1] =  0 if abs(jstick[3] - prev[3]) < 2 else jstick[3] - 126
         # move the mouse to the intended direction. Mouse is really bad in use but its included here as example.
        mouse.move(x=move[1],y=move[0])
        prev = jstick
        d = dict()
        i = 0
        press = []
        release = []
        for button in buttons:
            if arr[i]:press.append(keyboardCodes1[button])
            else:release.append(keyboardCodes1[button])
            i += 1
        for button in buttons2:
            if arr[i]:press.append(keyboardCodes2[button])
            else:release.append(keyboardCodes2[button])
            i += 1
        keyboard.press(*press)
        keyboard.release(*release)
        
        
tlioklawdsfrtfgqeeeeeeeeeeeeeeeeeeeddddaaaaaadrgftgilitod
def main():
    global vibrate1,vibrate2
    while True:
        if(error == 1):  # / skip loop if no controller found
            break
        if(type == 2):  # Guitar Hero Controller
            ps2x.read_gamepadNA()          # read controller
            status = []
            for button in guitarControls:
                if ps2x.Button(button):
                    status.append("{}".format(guitarControls[button]))
            s = "Wammy Bar Position:{} , ".format(ps2x.Analog(WHAMMY_BAR))
            s = s + str(status)
            print('                                                                                                                                            ', end='\r')
            print(s, end='\r')
        else:  # DualShock Controller
            ps2x.read_gamepad(vibrate1, vibrate2)
            status  = []
            pressed = []
            for button in buttons:
                val = ps2x.Button(button)
                if val:
                    status.append("{}".format(buttons[button]))
                pressed.append(val)
            for button in buttons2:
                val = ps2x.Button(button)
                if val:
                    status.append("{}".format(buttons2[button]))
                pressed.append(val)
            for button in analogbuttons:
                val = ps2x.Analog(button)
                if val > 2:
                    status.append("{}:{}".format(analogbuttons[button], val))
            jstick = [ps2x.Analog(PSS_LY), ps2x.Analog(
                PSS_LX), ps2x.Analog(PSS_RX), ps2x.Analog(PSS_RY)]
            s = "Stick Values:{},{},{},{}".format(
                jstick[0], jstick[1], jstick[2], jstick[3])
            sendInputToPC(pressed, jstick)
            string = s + " " + str(status)
            if DEBUG:
                print('                                                                                                                                                                                                    ', end='\r')
                print(string, end='\r')
            # This will set the Left and right vibration motor values
            vibrate1 = ps2x.Analog(PSAB_R2)
            vibrate2 = ps2x.Analog(PSAB_L2)

        time.sleep(50/1000)
main()
