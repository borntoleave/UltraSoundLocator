from Tkinter import *       
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)  # (1)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


pwmRed = GPIO.PWM(18, 500) # (2)
pwmRed.start(50)

pwmGreen = GPIO.PWM(23, 500)
pwmGreen.start(50)

pwmBlue = GPIO.PWM(24, 500)
pwmBlue.start(50)

class App:
    
    def __init__(self, master): #(3)
        frame = Frame(master)  #(4)
        frame.pack()
        
        Label(frame, text='Red').grid(row=0, column=0) # (5)
        Label(frame, text='Green').grid(row=1, column=0)
        Label(frame, text='Blue').grid(row=2, column=0)
        
        scaleRed = Scale(frame, from_=20, to=80,     # (6)
              orient=HORIZONTAL, command=self.updateRed)
        scaleRed.grid(row=0, column=1)
        scaleGreen = Scale(frame, from_=20, to=80,
              orient=HORIZONTAL, command=self.updateGreen)
        scaleGreen.grid(row=1, column=1)
        scaleBlue = Scale(frame, from_=20, to=80,
              orient=HORIZONTAL, command=self.updateBlue)
        scaleBlue.grid(row=2, column=1)

    def updateRed(self, duty):     # (7)
        # change the led brightness to match the slider
        pwmRed.ChangeDutyCycle(float(duty))

    def updateGreen(self, duty):
        pwmGreen.ChangeDutyCycle(float(duty))
    
    def updateBlue(self, duty):
        pwmBlue.ChangeDutyCycle(float(duty))
	
  #  os.system("tts.sh \"Where's my eye?\"")

root = Tk()  # (8)
root.wm_title('RGB LED Control')
app = App(root)
root.geometry("200x150+800+500")
try:
    root.mainloop()
finally:  
    print("Cleaning up")
    GPIO.cleanup()
