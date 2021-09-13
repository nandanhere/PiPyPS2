# PiPyPS2
Circuitpython implementation of a PlayStation 2 controller adapter for Raspberry pi/ pi pico <br>
This project also includes a Circuitpython port of [Bill Porter's PS2X library](https://github.com/madsci1016/Arduino-PS2X) in the gamepad_with_analog_and_rumble version


## What is it
- This is a python implementation of the interpreters used to read the input given by playstation controllers and use them accordingly as keyboard and mouse inputs. 

## Installation - in order to run the sample code:
After installing Circuitpython on your Device (Pico in the case of the example)
- From the adafruit circuitpython libraries copy the adafruit_hid library to your lib-folder
- Copy the contents of this repo (either one will work but with analog and rumble is reccomended ) into the main directory of the device (except for the wiring image)

 ## Installation - standalone
 - Copy the PiPyPS2  or PS2X folder into your directory from where you will refer to the PiPS2 / PS2X class
## Circuit 
![Circuit wiring image](https://github.com/nandanhere/PiPyPs2/blob/main/wiring.png)

## How to use (Keyboard mode):
- Open game of your choice and in controller remapping press the desired ps2 key while remapping. Note that for now the analog joysticks do not work and will only move the mouse pointer

## How to use (Controller mode):
- After setting up the controller, go to [Gamepad tester](https://gamepad-tester.com/) and try out all the buttons and see if they work. 
- Open game of your choice and in controller remapping press the desired ps2 key while remapping, if any tweaking is required.

## Note:
- usb_hid.gamepad is deprecated and will probably not work in the future. Also rumble will not work since the hid library does not support it. 
## Credits:
- Credits to [Vanepp](https://forum.fritzing.org/u/vanepp/summary) for the Ps2 controller wiring image
- [Bill Porter's PS2X library](https://github.com/madsci1016/Arduino-PS2X)