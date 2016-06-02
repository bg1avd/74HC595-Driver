import RPi.GPIO as GPIO
import time

# setup pins
dataPin = 11
clockPin = 15
latchPin = 13
clearPin = 22
oePin = 24

# default number of outputs in use
outputCount = 8

# store the current states in memory (used when doing changes to specific output)
currentStates = []

# sets the output count, the script will update only this many outputs (starting from the beginning A)
def setOutputCount(count):
	outputCount = count
	currenStates = []
	for x in range(0,outputCount):
		currentStates.append(False)

def setup(oc):
	setOutputCount(oc)
	
	# set GPIO to the right mode
	GPIO.setmode(GPIO.BOARD)
	
	# setup pins to be outputs
	GPIO.setup(dataPin, GPIO.OUT)
	GPIO.setup(clockPin, GPIO.OUT)
	GPIO.setup(clearPin, GPIO.OUT)
	GPIO.setup(latchPin, GPIO.OUT)
	GPIO.setup(oePin, GPIO.OUT)
	
	# setup the default states of pins
	# others low, clearPin high (its active low)
	GPIO.output(dataPin, False)
	GPIO.output(clockPin, False)
	GPIO.output(latchPin, False)
	GPIO.output(clearPin, True) # active low
	GPIO.output(oePin, False) # active low


## Low level functionality ##

def cleanup():
	# clear the outputs
	resetLow()
	# set the output enabled pin high (disables output)
	GPIO.output(oePin, True)
	# clenup the GPIO
	GPIO.cleanup()

def resetLow():
	# set all outputs low
	for x in range(0,outputCount):
	        shift(False)
	latch()

# shifts data to the register
def shift(output):
	GPIO.output(dataPin, output)
	GPIO.output(clockPin, True)
	time.sleep(0.01)
	GPIO.output(clockPin, False)
	GPIO.output(dataPin, False)

# latches (activates) the data from memory to the outputs
def latch():
	GPIO.output(latchPin, True)
	time.sleep(0.01)
	GPIO.output(latchPin, False)



## Higher level stuff ##

# sets the outputs from the currentStates array
def updateFromMemory():
	for x in range(0,outputCount):
	        shift(currentStates[outputCount - x - 1])
	latch()

# sets output of a specific pin
def setOutput(outputNumber, high):
	# changes the pins state in memory
	currentStates[outputNumber] = high
	# updates the states from memory to the shift register
	updateFromMemory()

