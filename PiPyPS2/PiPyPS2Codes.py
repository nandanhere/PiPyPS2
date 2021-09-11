# Delays */
CLK_DELAY  		= 4
BYTE_DELAY 		= 3
CMD_DELAY 		= 1
MAX_READ_DELAY 	= 10

enterConfigMode =  [0x01,0x43,0x00,0x01,0x00]
set_mode_analog_lock = [0x01,0x44,0x00,0x01,0x03,0x00,0x00,0x00,0x00]
exitConfigMode= [0x01,0x43,0x00,0x00,0x5A,0x5A,0x5A,0x5A,0x5A]
type_read = [0x01,0x45,0x00,0x5A,0x5A,0x5A,0x5A,0x5A,0x5A]
config_AllPressure= [0x01,0x4F,0x00,0xFF,0xFF,0x03,0x00,0x00,0x00]

# Maximum number of init tries */
MAX_INIT_ATTEMPT 	= 5

# Delays */
CLK_DELAY  		= 4
BYTE_DELAY 		= 3
CMD_DELAY 		= 1
MAX_READ_DELAY 	= 10

# Maximum number of init tries */
MAX_INIT_ATTEMPT 	= 50

# Controller Modes - From: http://www.lynxmotion.com/images/files/ps2cmd01.txt */
READDELAYMS  = 10
DIGITALMODE = 	0x41
ANALOGMODE 	= 	0x73
ALLPRESSUREMODE	= 0x79
DS2NATIVEMODE	= 0xF3
# Button Masks */
# From data bit 0 (PS2data[3])
BTN_SELECT 		= 0
BTN_LEFT_JOY	= 1
BTN_RIGHT_JOY	= 2
BTN_START		= 3
BTN_UP			= 4
BTN_RIGHT		= 5
BTN_DOWN		= 6
BTN_LEFT		= 7
# From data bit 1 (PSdata[4])
BTN_L2			= 0
BTN_R2			= 1
BTN_L1			= 2
BTN_R1			= 3
BTN_TRIANGLE	= 4
BTN_CIRCLE		= 5
BTN_X		= 	6
BTN_SQUARE		= 7

# Byte Numbers of PSdata[] For Button Pressures */
PRES_RIGHT 		= 10
PRES_LEFT 	= 	11
PRES_UP 		= 12
PRES_DOWN 		= 13
PRES_TRIANGLE 	= 14
PRES_CIRCLE 	= 15
PRES_X		 = 	16
PRES_SQUARE = 	17
PRES_L1		 = 	18
PRES_R1		 = 	19
PRES_L2		 = 	20
PRES_R2		 = 	21