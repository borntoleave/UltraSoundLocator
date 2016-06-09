from Tkinter import *       
import RPi.GPIO as GPIO
import time
import math
import os

GPIO.setmode(GPIO.BCM)  # (1)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
pwmRed = GPIO.PWM(18, 500) # (2)
pwmBlue = GPIO.PWM(23, 500) # (2)
pwmRed.start(50)
pwmBlue.start(50)
ang1=0
ang2=0
dHorizon=60
dVertical=35
sentence ="Thief! I smeel you, I hear your breath, I feel your air. Where are you? Come now, dont be shy."
#os.system('tts.sh "Thief! I smeel you, I hear your breath, I feel your air. Where are you? Come now, dont be shy."')
try:
	while 1:
		d = math.sin( (ang1+math.pi/dHorizon) %(2*math.pi) )
		pwmRed.ChangeDutyCycle(float((d/2+0.5)*60+20))
		i=1
		while i<=5:
			d = math.cos( (ang2+math.pi/dVertical)%(2*math.pi) )
			pwmBlue.ChangeDutyCycle(float((d/2+0.5)*30+40))	
			ang2 = ang2+math.pi/dVertical
			i=i+1
			#os.system('aplay --no-show-progress --null --channel 1 synth %s sine %f' % (0.05,488))			
			time.sleep(0.005)
		ang1 = ang1+math.pi/dHorizon
		#time.sleep(0.01)
except KeyboardInterrupt:	
	os.system("tts.sh \"I'm sleepy. Good night!\"")
	print("Cleaning up")
	GPIO.cleanup()

