# Measuring part is modified from Matt Hawkin's code.
#
# Author : Matt Hawkins
# Date   : 28/01/2013

from Tkinter import *       
import RPi.GPIO as GPIO
import time
import math
from random import randint
import os

# -----------------------
# Define some functions
# -----------------------

def measure():
  # This function measures a distance
  GPIO.output(gpio_trigger, True)
  time.sleep(0.00001)
  GPIO.output(gpio_trigger, False)
  start = time.time()
  stop  = start
  while GPIO.input(gpio_echo)==0:
    start = time.time()

  while GPIO.input(gpio_echo)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.
  i=0
  times=2
  distance=0
  while i<times:
  	distance=distance+measure()
  	i=i+1
  	time.sleep(0.0001)
  distance = distance / times
  return distance


GPIO.setmode(GPIO.BCM)  # (1)
gpio_trigger=17
gpio_echo=27

GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(gpio_trigger,GPIO.OUT)
GPIO.setup(gpio_echo,GPIO.IN)

GPIO.output(gpio_trigger,False)

pwmRed = GPIO.PWM(18, 500) # (2)
pwmBlue = GPIO.PWM(23, 500) # (2)
pwmRed.start(50)
pwmBlue.start(50)
duty1=50
duty2=50
dStep1=1
dStep2=2
distThres=8
sts=['I hear you!','Where are you?','Don\'t be shy!']
s=0
i=0

while i<2:
	distance = measure_average()
	print "Distance : %.1f" % distance
	time.sleep(0.01)
	i=i+1
try:
	while 1:
		distance = measure_average()
	    	print "Distance : %.1f" % distance
    		if distance >distThres:
    			if duty1+dStep1>80 or duty1+dStep1<20:
				dStep1=-dStep1
				os.system("tts.sh "+'\"'+sts[s]+'\"')
				s=(s+1)%3
			duty1 = duty1+dStep1			
			pwmRed.ChangeDutyCycle(duty1)
			pwmBlue.ChangeDutyCycle(duty2+randint(-9,9))
			#print "Duty1 : %.1f" % duty1
			time.sleep(0.002)
		elif distance<=distThres: 
			os.system('tts.sh \"I find you!\"')
			i=1
			while 1:
				if duty2+dStep2>70 or duty2+dStep2<30:
					dStep2=-dStep2
				duty2 = duty2+dStep2
				pwmBlue.ChangeDutyCycle(duty2)	
				new_dist= measure_average()
				print "Distance : %.1f" % distance
				if new_dist>distance:
					#os.system("tts.sh "+'i find you')	
					time.sleep(0.5)
					#pwmBlue.ChangeDutyCycle(50)
					break		
				distance=new_dist
				time.sleep(0.001)
except KeyboardInterrupt:	
	
	print("Cleaning up")
	GPIO.cleanup()

