import RPi.GPIO as GPIO
import time


# setup pins
dataPin = 11
clockPin = 15
latchPin = 13
clearPin = 22
oePin = 24

# number of outputs in use
outputCount = 4

def setup():
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

def cleanup():
	# clear the outputs
	resetLow()
	# set the output enabled pin high (disables output)
	GPIO.output(oePin, True)
	# clenup the GPIO
	GPIO.cleanup()

def resetLow():
	# set all outputs low
	for x in range(0,8):
		shift(False)
	latch()

# shifts data to the register
def shift(output):
	GPIO.output(dataPin, output)
	GPIO.output(clockPin, True)
	time.sleep(0.01)
	GPIO.output(clockPin, False)
	GPIO.output(dataPin, False)

# laches (activates) the data from memory to the outputs	
def latch():
	GPIO.output(latchPin, True)
	time.sleep(0.01)
	GPIO.output(latchPin, False)



# testing...
setup()
try:
	while(True):
		for x in range(0,4):
			shift(True)
			latch()
			time.sleep(0.1)
		for x in range(0,4):
			shift(False)
			latch()
			time.sleep(0.1)
except (KeyboardInterrupt):
	print 'Shutting down systems...'
finally:
	cleanup()
