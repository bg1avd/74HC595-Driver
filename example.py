import driver
import time


driver.setup(8)

try:
  while True:
    for x in range(0,8):
      driver.setOutput(x, True)
      time.sleep(0.1)
    for x in range(0,8):
      driver.setOutput(x, False)
      time.sleep(0.1)

except (KeyboardInterrupt):
  print 'Exiting...'

finally:
  driver.cleanup()
