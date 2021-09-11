
import digitalio #type:ignore
import board      #type:ignore
import time #type: ignore
from .PiPyPS2Codes import *

def SET(x,y): x |= (1<<y)	#Set bit y in x
def CLR(x,y):   x &= (~(1<<y))  # Clear bit y in x
def CHK(x,y) : return (x & (1<<y)) #	 Check if bit y in x is set
def TOG(x,y):  x ^= (1<<y)
def sleep_us(x): time.sleep(x / 5000000)


class PIPS2:
  btnLastState = btnChangedState = [0,0]
  PS2data = [0 for _ in range(21)]
  controllerMode = 0
  commandPin = dataPin = attnPin = clkPin = readDelay = ackPin = 0
  # did this to have a non null base class value.
  commandP = clkP = attentionP = dataP = ackP = digitalio.DigitalInOut(board.GP0)
  def __init__(self) -> None:
      pass
  def initializeController(self,  _dataPin, _commandPin,_attnPin, _clkPin,_ackPin):
    #  INITIALIZE I/O
    self.commandPin = _commandPin;
    self.dataPin = _dataPin;
    self.clkPin = _clkPin;
    self.attnPin = _attnPin;
    self.ackPin = _ackPin
    self.readDelay = 1;
    self.controllerMode = ANALOGMODE;
    
    # P added to refer to the pin class for pi pico -- for circuitpython
    self.dataP = digitalio.DigitalInOut(board.GP2)
    self.commandP = digitalio.DigitalInOut(board.GP3)
    self.attentionP = digitalio.DigitalInOut(board.GP4)
    self.clkP = digitalio.DigitalInOut(board.GP5)
    self.ackP = digitalio.DigitalInOut(board.GP6)
    #  Set command pin to output
    self.commandP.direction = digitalio.Direction.OUTPUT
    #  Set data pin to input
    #Note that you can either do this with a 10k resistor (as pull up resistor) or just use the code below.
#    self.dataP.direction = digitalio.Direction.INPUT
    self.dataP.pull = digitalio.Pull.UP
    #  Set attention pin to output
    self.attentionP.direction = digitalio.Direction.OUTPUT
    #  Set clock pin to output
    self.clkP.direction = digitalio.Direction.OUTPUT
    

	
    #  Set command pin and clock pin high, ready to initialize a transfer.
    self.commandP.value = True
    self.clkP.value = True

    #  Read controller a few times to check if it is talking.
    self.readPS2()	
    self.readPS2()
    
    #  Initialize the read delay to be 1 millisecond. 
    #  Increment read_delay until controller accepts commands.
    #  This is a but of dynamic debugging. Read delay usually needs to be about 2.
    #  But for some controllers, especially wireless ones it needs to be a bit higher.
    
    #  Try up until readDelay = MAX_READ_DELAY
    while True:
      #  Transmit the enter config command.
      self.transmitCmdString(enterConfigMode, len(enterConfigMode));      
      #  Set mode to analog mode and lock it there.
      self.transmitCmdString(set_mode_analog_lock, len(set_mode_analog_lock));
      #  Exit config mode.	
      self.transmitCmdString(exitConfigMode, len(exitConfigMode));
      #  Attempt to read the controller.
      self.readPS2()
      #  If read was successful (controller indicates it is in analog mode), break this config loop.
      if (self.PS2data[1] == self.controllerMode):
          break;
      #  If we have tried and failed 10 times. call it quits,
      if (self.readDelay == MAX_READ_DELAY):
            return 0
      

    # Otherwise increment the read delay and go for another loop
      self.readDelay	+= 1
    
    return 1

  def transmitByte(self,byte):
      #  Data byte received
      RXdata = 0;
      # Bit bang all 8 bits
      for i in range(8):
        #  If the bit to be transmitted is 1 then set the command pin to 1
        if (CHK(byte, i)): 	
          self.commandP.value = True
        else:				
          self.commandP.value = False
        #  Pull clock low to transfer bit
        self.clkP.value = False  
        # Wait for the clock delay before reading the received bit.
        sleep_us(CLK_DELAY)
        #  If the data pin is now high then save the input.
        if self.dataP.value :
          RXdata |= (1 << i)
        #  Done transferring bit. Put clock back high
        self.clkP.value = True
        # digitalWrite(clkPin, 1);
        sleep_us(CLK_DELAY)
        # delayMicroseconds(CLK_DELAY);
      #  Done transferring byte, set the command pin back high and wait.
      self.commandP.value = True
      # digitalWrite(commandPin, 1);
      sleep_us(BYTE_DELAY)
      # delayMicroseconds(BYTE_DELAY);
      return RXdata;

  def transmitCmdString(self,string,length):
    # Create a temporary buffer for receiving the response.
    tempBuffer = [0 for _ in range(length)]
	
    #  Ready to begin transmitting, pull attention low.
    self.attentionP.value = False

    #  Shift the data out, one byte at a time.
    for y in range(length):
      tempBuffer[y] = self.transmitByte(string[y]);
      

	  #  Packet finished, release attention line.
    self.attentionP.value = True
    sleep_us(self.readDelay)
  	# delay(readDelay);
  def readPS2(self):
      last_read = 0;
      timeSince = (time.monotonic() - last_read)  #type: ignore
      if (timeSince > 1500): # waited to long
        self.reInitializeController2()
      # note that readDelay is in Milliseconds
      if(timeSince < self.readDelay):  # waited too short
        time.sleep((self.readDelay - timeSince))	
      #  Ensure that the command bit is high before lowering attention.
      self.commandP.value = True
      #  Ensure that the clock is high.
      self.clkP.value = True
      #  Drop attention pin.
      self.attentionP.value = False

      #  Wait for a while between transmitting bytes so that pins can stabilize. wait in microseconds
      sleep_us(BYTE_DELAY)
      # delayMicroseconds(BYTE_DELAY);
      
      # The TX and RX buffer used to read the controller.
      TxRx1 = [0x01,0x42,0,0,0,0,0,0,0]
      TxRx2 = [0,0,0,0,0,0,0,0,0,0,0,0]
      

      #  Grab the first 9 bits
      for i in range(9):
        self.PS2data[i] = self.transmitByte(TxRx1[i]);
      # If controller is in full data return mode, get the rest of data
      if(self.PS2data[1] == 0x79):
        for i in range(12):
          self.PS2data[i+9] = self.transmitByte(TxRx2[i])

      # Done reading packet, release attention line.
      self.attentionP.value = True
      # digitalWrite(attnPin, 1);
      last_read = time.monotonic() #type:ignore
      # Detect which buttons have been changed
      self.btnChangedState[0] = self.PS2data[3] ^ self.btnLastState[0];
      self.btnChangedState[1] = self.PS2data[4] ^ self.btnLastState[1];
      #  Save the current button states as the last state for next read)
      self.btnLastState[0] = self.PS2data[3];
      self.btnLastState[1] = self.PS2data[4];

  def reInitializeController1(self,_controllerMode):
    controllerMode = _controllerMode;
    if (controllerMode != ANALOGMODE and controllerMode != ALLPRESSUREMODE):
          return -1
    for _ in range(1,MAX_INIT_ATTEMPT):	
      self.transmitCmdString(enterConfigMode,  len(enterConfigMode));
      self.transmitCmdString(set_mode_analog_lock, len(set_mode_analog_lock));
      if (controllerMode == ALLPRESSUREMODE):
        self.transmitCmdString(config_AllPressure, len(config_AllPressure));
      self.transmitCmdString(exitConfigMode, len(exitConfigMode));
      self.readPS2();
      if (self.PS2data[1] == controllerMode):
            return 1
      time.sleep(self.readDelay / 1000)
    return -2
  def reInitializeController2(self):
      return self.reInitializeController1(self.controllerMode)
  def getChangedStates(self,outputChangedStates):
    outputChangedStates[0] = self.btnChangedState[0];
    outputChangedStates[1] = self.btnChangedState[1];
