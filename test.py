import signal
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

GPIO.output(17, GPIO.HIGH)

time.sleep(5)

GPIO.output(17, GPIO.LOW)

time.sleep(5)

GPIO.output(17, GPIO.HIGH)

time.sleep(5)

GPIO.output(17, GPIO.LOW)

GPIO.cleanup()
