# $$$$$$$$$$$$ DEBUG ENABLE SECTION $$$$$$$$$$$$$$$$
# to debug ps2 controller, uncomment below to print debug messages.
from PS2XCodes import *
import board  # type:ignore
import digitalio  # type:ignore
import time
debug = False


class PS2X:
    _clk_pin = _cmd_pin = _att_pin = _dat_pin = 0  # int and byte types
    # int and byte types
    last_read = read_delay = controller_type = i = last_buttons = buttons = 0
    en_Rumble = en_Pressures = False  # boolean types
    PS2data = [0 for _ in range(21)]  # holds the data recieved
    # ****************************************************************************************/

    def __init__(self) -> None:
        pass
    # ****************************************************************************************/

    def NewButtonStateNA(self):
        return ((self.last_buttons ^ self.buttons) > 0)

    # **will be TRUE if button was JUST pressed OR released*********************************/
    def NewButtonState(self, button):
        return (((self.last_buttons ^ self.buttons) & button) > 0)

    # **will be TRUE if button was JUST pressed******************************************************/
    def ButtonPressed(self, button):
        return(self.NewButtonState(button) & self.Button(button))

    # *will be TRUE if button was JUST released*********************************************************/
    def ButtonReleased(self, button):
        return((self.NewButtonState(button)) & ((~self.last_buttons & button) > 0))

    # *will be TRUE if button is being pressed*************************************************/
    def Button(self, button):
        return ((~self.buttons & button) > 0)

    # ****************************************************************************************/
    def ButtonDataByte(self):
        return (~self.buttons)

    # ****************************************************************************************/
    def Analog(self, button):
        return self.PS2data[button]

    # ****************************************************************************************/
    def _gamepad_shiftinout(self, byte):
        tmp = 0
        for i in range(8):
            if(CHK(byte, i)):
                self.CMD_SET()
            else:
                self.CMD_CLR()
            self.CLK_CLR()
            sleep_us(CTRL_CLK)
            if self.DAT_CHK():
                tmp |= (1 << i)
            self.CLK_SET()
            if CTRL_CLK_HIGH:
                sleep_us(CTRL_CLK_HIGH)

        self.CMD_SET()
        sleep_us(CTRL_BYTE_DELAY)
        return tmp

    # ****************************************************************************************/

    def read_gamepadNA(self):
        self.read_gamepad(False, 0x00)

    # ****************************************************************************************/
    def read_gamepad(self, motor1, motor2):
        temp = (time.monotonic() * 1000) - self.last_read  # type: ignore
        if (temp > 1500):  # waited to long
            self.reconfig_gamepad()

        if(temp < self.read_delay):  # waited too short
            sleep_us((self.read_delay - temp) * 1000)

        if(motor2 != 0x00):
            # noting below 40 will make it spin
            motor2 = cmap(motor2, 0, 255, 0x40, 0xFF)
        dword = [0x01, 0x42, 0, motor1, motor2, 0, 0, 0, 0]
        dword2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Try a few times to get valid data...
        for _ in range(5):
            self.CMD_SET()
            self.CLK_SET()
            self.ATT_CLR()  # low enable joystick
            sleep_us(CTRL_BYTE_DELAY)
            for i in range(9):         # Send the command to send button and joystick data;
                self.PS2data[i] = self._gamepad_shiftinout(dword[i])
            # if controller is in full data return mode, get the rest of data
            if(self.PS2data[1] == 0x79):
                for i in range(12):
                    self.PS2data[i+9] = self._gamepad_shiftinout(dword2[i])

            self.ATT_SET()  # HI disable joystick
            # Check to see if we received valid data or not.
            # We should be in analog mode for our data to be valid (analog == 0x7_)
            if ((self.PS2data[1] & 0xf0) == 0x70):
                break
            # If we got to here, we are not in analog mode, try to recover...
            self.reconfig_gamepad()  # try to get back into Analog mode.
            sleep_us(self.read_delay * 1000)

        # If we get here and still not in analog mode (=0x7_), try increasing the read_delay...
        if ((self.PS2data[1] & 0xf0) != 0x70):
            if (self.read_delay < 10):
                self.read_delay += 1  # see if this helps out...

        if debug:
            print("OUT : IN")
            print(dword + dword2)
            print(self.PS2data)

        self.last_buttons = self.buttons  # store the previous buttons states
        # store as one value for multiple functions
        self.buttons = (self.PS2data[4] << 8) + self.PS2data[3]

        self.last_read = time.monotonic() * 1000  # type:ignore
        # 1 = OK = analog mode - 0 = NOK
        return ((self.PS2data[1] & 0xf0) == 0x70)

    # ****************************************************************************************/

    def config_gamepadNA(self, clk, cmd, att, dat):
        return self.config_gamepad(clk, cmd, att, dat, False, False)

    # ****************************************************************************************/

    def config_gamepad(self, clk, cmd, att, dat, pressures, rumble):
        temp = [0 for _ in range(len(type_read))]

        self.commandPin = cmd
        self.dataPin = dat
        self.clkPin = clk
        self.attnPin = att
        self.readDelay = 1
        # P added to refer to the pin class for pi pico -- for circuitpython
        global dp, cp, ap, clp
        dp = cp = ap = clp = None
        # type:ignore
        exec("global dp; dp =  digitalio.DigitalInOut(board.GP{})".format(dat))
        # type:ignore
        exec("global cp; cp =  digitalio.DigitalInOut(board.GP{})".format(cmd))
        # type:ignore
        exec("global ap; ap =  digitalio.DigitalInOut(board.GP{})".format(att))
        # type:ignore
        exec("global clp; clp = digitalio.DigitalInOut(board.GP{})".format(clk))

        self._dat_pin = dp  # type:ignore
        self._cmd_pin = cp  # type:ignore
        self._att_pin = ap  # type:ignore
        self._clk_pin = clp  # type:ignore

        #  Set command pin to output
        self._cmd_pin.direction = digitalio.Direction.OUTPUT  # type:ignore
        #  Set data pin to input
        # Note that you can either do this with a 10k resistor (as pull up resistor) or just use the code below.
        #    self.dataP.direction = digitalio.Direction.INPUT
        self._dat_pin.pull = digitalio.Pull.UP  # type:ignore
        #  Set attention pin to output
        self._att_pin.direction = digitalio.Direction.OUTPUT  # type:ignore
        #  Set clock pin to output
        self._clk_pin.direction = digitalio.Direction.OUTPUT  # type:ignore

        #  Set command pin and clock pin high, ready to initialize a transfer.
        self._cmd_pin.value = True  # type: ignore
        self._clk_pin.value = True  # type: ignore

        self.CMD_SET()
        self.CLK_SET()

        # new error checking. First, read gamepad a few times to see if it's talking
        self.read_gamepadNA()
        self.read_gamepadNA()

        # see if it talked - see if mode came back.
        # If still anything but 41, 73 or 79, then it's not talking
        if(self.PS2data[1] != 0x41 and self.PS2data[1] != 0x42 and self.PS2data[1] != 0x73 and self.PS2data[1] != 0x79):
            if debug:
                print("Controller mode not matched or no controller found , Expected 0x41, 0x42, 0x73 or 0x79, but got {}".format(
                    hex(self.PS2data[1])))
            return 1  # return error code 1
        # /try setting mode, increasing delays if need be.
        self.read_delay = 1

        for y in range(11):
            self.sendCommandString(enter_config, len(
                enter_config))  # start config run

            # read type
            sleep_us(CTRL_BYTE_DELAY)
            self.CMD_SET()
            self.CLK_SET()
            self.ATT_CLR()  # low enable joystick
            sleep_us(CTRL_BYTE_DELAY)
            for i in range(9):
                temp[i] = self._gamepad_shiftinout(type_read[i])
            self.ATT_SET()  # HI disable joystick
            self.controller_type = temp[3]
            self.sendCommandString(set_mode, len(set_mode))
            if(rumble):
                self.sendCommandString(enable_rumble, len(enable_rumble))
                self.en_Rumble = True
            if(pressures):
                self.sendCommandString(set_bytes_large, len(set_bytes_large))
                self.en_Pressures = True
            self.sendCommandString(exit_config, len(exit_config))
            self.read_gamepadNA()
            if(pressures):
                if(self.PS2data[1] == 0x79):
                    break
                if(self.PS2data[1] == 0x73):
                    return 3
            if(self.PS2data[1] == 0x73):
                break
            if(y == 10):
                if debug:
                    print("Controller not accepting commands" +
                          "mode still set at".format(hex(self.PS2data[1])))
                return 2  # exit function with error
            self.read_delay += 1  # add 1ms to read_delay
        return 0  # no error if here
    # ****************************************************************************************/

    def sendCommandString(self, string, length):
        if debug:
            temp = [0 for _ in range(length)]
            self.ATT_CLR()  # low enable joystick
            sleep_us(CTRL_BYTE_DELAY)

            for y in range(length):
                temp[y] = self._gamepad_shiftinout(string[y])

            self.ATT_SET()  # high disable joystick
            sleep_us(1000 * self.read_delay)  # wait a few

            print("OUT:IN Configure")
            print([hex(i) for i in string])
            print([hex(i) for i in temp])
        else:
            self.ATT_CLR()  # low enable joystick
            sleep_us(CTRL_BYTE_DELAY)
            for y in range(length):
                self._gamepad_shiftinout(string[y])
            self.ATT_SET()  # high disable joystick
            sleep_us(1000 * self.read_delay)  # wait a few

    # ****************************************************************************************/

    def readType(self):
        print("Controller_type: {}".format(hex(self.controller_type)))
        if(self.controller_type == 0x03):
            return 1
        elif(self.controller_type == 0x01 and self.PS2data[1] == 0x42):
            return 4
        elif(self.controller_type == 0x01 and self.PS2data[1] != 0x42):
            return 2
        elif(self.controller_type == 0x0C):
            return 3  # 2.4G Wireless Dual Shock PS2 Game Controller
        return 0

    # ****************************************************************************************/

    def enableRumble(self):
        self.sendCommandString(enter_config, len(enter_config))
        self.sendCommandString(enable_rumble, len(enable_rumble))
        self.sendCommandString(exit_config, len(exit_config))
        self.en_Rumble = True

    # ****************************************************************************************/

    def enablePressures(self):
        self.sendCommandString(enter_config, len(enter_config))
        self.sendCommandString(set_bytes_large, len(set_bytes_large))
        self.sendCommandString(exit_config, len(exit_config))

        self.read_gamepadNA()
        self.read_gamepadNA()

        if(self.PS2data[1] != 0x79):
            return False

        self.en_Pressures = True
        return True

    # ****************************************************************************************/

    def reconfig_gamepad(self):
        self.sendCommandString(enter_config, len(enter_config))
        self.sendCommandString(set_mode, len(set_mode))
        if (self.en_Rumble):
            self.sendCommandString(enable_rumble, len(enable_rumble))
        if (self.en_Pressures):
            self.sendCommandString(set_bytes_large, len(set_bytes_large))
        self.sendCommandString(exit_config, len(exit_config))

    # ****************************************************************************************/
    def CLK_SET(self):
        pass
        self._clk_pin.value = True  # type: ignore

    def CLK_CLR(self):
        self._clk_pin.value = False  # type: ignore

    def CMD_SET(self):
        self._cmd_pin.value = True  # type: ignore

    def CMD_CLR(self):
        self._cmd_pin.value = False  # type: ignore

    def ATT_SET(self):
        self._att_pin.value = True  # type: ignore

    def ATT_CLR(self):
        self._att_pin.value = False  # type: ignore

    def DAT_CHK(self):
        return self._dat_pin.value  # type: ignore


# Some helper functions
def CHK(x, y): return (x & (1 << y))  # Check if bit y in x is set
# trying to match 500mhz. you can change the value if you want but this should work fine.
def sleep_us(x): time.sleep(x / 5000000)
# there is no equivalent to map() in python so this function will do the job (from the arduino docs)


def cmap(x, in_min, in_max, out_min, out_max): return int(
    (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def range_map(x, in_min, in_max, out_min, out_max): return int(
    (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
