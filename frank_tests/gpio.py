import RPi.GPIO as GPIO
import time

pin = 17
var = 0
GPIO.setmode(GPIO.BCM)
print("DOING STUFF")
GPIO.setup(pin, GPIO.OUT)
while (var < 10):

    GPIO.output(pin, GPIO.HIGH)

    time.sleep(1)

    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    var = var +1
print("END OF LOOP")
GPIO.cleanup()
