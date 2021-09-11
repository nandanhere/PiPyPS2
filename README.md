# PiPyPS2
Circuitpython implementation of a PlayStation 2 controller adapter for Raspberry pi/ pi pico

## What is it
- This is a python implementation of the interpreters used to read the input given by playstation controllers and use them accordingly as keyboard and mouse inputs. 

## Installation - in order to run the sample code:
After installing Circuitpython on your Device (Pico in the case of the example)
- From the adafruit circuitpython libraries copy the adafruit_hid library to your lib-folder
- Copy the contents of this repo into the main directory of the device (except for the wiring image)

 ## Installation - standalone
 - Copy the PiPyPS2 folder into your directory from where you will refer to the PiPS2 class
## Circuit 
![Circuit wiring image](https://github.com/nandanhere/PiPyPs2/blob/main/wiring.png)

## How to use:
- Open game of your choice and in controller remapping press the desired ps2 key while remapping. Note that for now the analog joysticks do not work

Credits to [Vanepp](https://forum.fritzing.org/u/vanepp/summary) for the Ps2 controller wiring image


## To do:
- Implement most of the features (convert to python mostly) of [Bill Porter's PS2X library](https://github.com/madsci1016/Arduino-PS2X)