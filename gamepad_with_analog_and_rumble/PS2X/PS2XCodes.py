
# These codes are for the program to give gamepad/keyboard

from adafruit_hid.keycode import Keycode

# I have moved these to another file to keep the code easy to navigate through.


CTRL_CLK = 5
CTRL_BYTE_DELAY = 4
CTRL_CLK_HIGH = 5
# These are our button constants
PSB_SELECT = 0x0001
PSB_L3 = 0x0002
PSB_R3 = 0x0004
PSB_START = 0x0008
PSB_PAD_UP = 0x0010
PSB_PAD_RIGHT = 0x0020
PSB_PAD_DOWN = 0x0040
PSB_PAD_LEFT = 0x0080
PSB_L2 = 0x0100
PSB_R2 = 0x0200
PSB_L1 = 0x0400
PSB_R1 = 0x0800
PSB_GREEN = 0x1000
PSB_RED = 0x2000
PSB_BLUE = 0x4000
PSB_PINK = 0x8000
PSB_TRIANGLE = 0x1000
PSB_CIRCLE = 0x2000
PSB_CROSS = 0x4000
PSB_SQUARE = 0x8000

# Guitar  button constants
UP_STRUM = 0x0010
DOWN_STRUM = 0x0040
LEFT_STRUM = 0x0080
RIGHT_STRUM = 0x0020
STAR_POWER = 0x0100
GREEN_FRET = 0x0200
YELLOW_FRET = 0x1000
RED_FRET = 0x2000
BLUE_FRET = 0x4000
ORANGE_FRET = 0x8000
WHAMMY_BAR = 8

# These are stick values
PSS_RX = 5
PSS_RY = 6
PSS_LX = 7
PSS_LY = 8

# These are analog buttons
PSAB_PAD_RIGHT = 9
PSAB_PAD_UP = 11
PSAB_PAD_DOWN = 12
PSAB_PAD_LEFT = 10
PSAB_L2 = 19
PSAB_R2 = 20
PSAB_L1 = 17
PSAB_R1 = 18
PSAB_GREEN = 13
PSAB_RED = 14
PSAB_BLUE = 15
PSAB_PINK = 16
PSAB_TRIANGLE = 13
PSAB_CIRCLE = 14
PSAB_CROSS = 15
PSAB_SQUARE = 16


enter_config = [0x01, 0x43, 0x00, 0x01, 0x00]
set_mode = [0x01, 0x44, 0x00, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00]
set_bytes_large = [0x01, 0x4F, 0x00, 0xFF, 0xFF, 0x03, 0x00, 0x00, 0x00]
exit_config = [0x01, 0x43, 0x00, 0x00, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A]
enable_rumble = [0x01, 0x4D, 0x00, 0x00, 0x01]
type_read = [0x01, 0x45, 0x00, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A]


#  These maps are for the keyboard / gamepad hid objects.
buttons = {PSB_SELECT: 'select', PSB_L3: 'left joystick button', PSB_R3: 'right joystick button',
           PSB_START: 'start', PSB_PAD_UP: 'up', PSB_PAD_DOWN: 'down', PSB_PAD_LEFT: 'left', PSB_PAD_RIGHT: 'right'}
buttons2 = {PSB_L2: 'L2', PSB_R2: 'R2', PSB_L1: 'L1', PSB_R1: 'R1',
            PSB_TRIANGLE: 'triangle', PSB_CIRCLE: 'circle', PSB_CROSS: 'X', PSB_SQUARE: 'Square'}
keyboardCodes1 = {PSB_SELECT: Keycode.SPACEBAR, PSB_L3: Keycode.Q, PSB_R3: Keycode.E, PSB_START: Keycode.X,
                  PSB_PAD_UP: Keycode.W, PSB_PAD_DOWN: Keycode.S, PSB_PAD_LEFT: Keycode.A, PSB_PAD_RIGHT: Keycode.D}
keyboardCodes2 = {PSB_L2: Keycode.R, PSB_R2: Keycode.T, PSB_L1: Keycode.F, PSB_R1: Keycode.G,
                  PSB_TRIANGLE: Keycode.I, PSB_CIRCLE: Keycode.O, PSB_CROSS: Keycode.K, PSB_SQUARE: Keycode.L}
analogbuttons = {PSAB_PAD_RIGHT: 'Right', PSAB_PAD_UP: 'Up', PSAB_PAD_DOWN: 'Down', PSAB_PAD_LEFT: 'Left', PSAB_L2: 'L2', PSAB_R2: 'R2', PSAB_L1: 'L1', PSAB_R1: 'R1',
                 PSAB_GREEN: 'GREEN', PSAB_RED: 'RED', PSAB_BLUE: 'BLUE', PSAB_PINK: 'PINK', PSAB_TRIANGLE: 'Triangle', PSAB_CIRCLE: 'Circle', PSAB_CROSS: 'Cross', PSAB_SQUARE: 'Square'}
guitarControls = {GREEN_FRET: "Green fret", RED_FRET: "Red Fret", YELLOW_FRET: "Yellow Fret", BLUE_FRET: "Blue Fret",
                  ORANGE_FRET: "Orange Fret", STAR_POWER: "Star Power", UP_STRUM: "Up Strum", DOWN_STRUM: "Down Strum", PSB_START: "start", PSB_SELECT: "select"}
