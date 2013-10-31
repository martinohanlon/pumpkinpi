import gpioRap as gpioRap
import RPi.GPIO as GPIO
import subprocess
import time
import random

#Create GpioRap class using BCM pin numbers
gpioRapper = gpioRap.GpioRap(GPIO.BCM)

#Create an LED, which should be attached to pin 17
white1 = gpioRapper.createLED(4)
white2 = gpioRapper.createLED(17)
red1 = gpioRapper.createLED(21)
red2 = gpioRapper.createLED(22)

# Define GPIO to use on Pi
GPIO_PIR = 24

# Set pir pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)

try:

    Current_State  = 0
    Previous_State = 0

    # Loop until PIR output is 0
    while GPIO.input(GPIO_PIR)==1:
        Current_State  = 0

    redeyecounter = 0

    #Loop until exception (ctrl c)
    while True:
        # Read PIR state
        Current_State = GPIO.input(GPIO_PIR)
 
        if Current_State==1 and Previous_State==0:
            # PIR is triggered
            print "  Motion detected!"
            # turn on red and white lights
            red1.on()
            red2.on()
            white1.on()
            white2.on() 
            # play random sound
            soundno = random.randint(1,6)
            subprocess.call(["mplayer","/home/pi/dev/pumpkin/"+str(soundno)+".m4a"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Record previous state
            Previous_State=1
        #elif Current_State==1 and Previous_State==1:
            
        elif Current_State==0 and Previous_State==1:
            # PIR has returned to ready state
            print "  Ready"
            # turn off red and white lights
            red1.off()
            red2.off()
            white1.off()
            white2.off()
            Previous_State=0
        elif Current_State==0 and Previous_State==0:
            #in steady state, incremenet flash red eye state
            redeyecounter+=1
 
        #every 5 seconds (ish) of steady state, flash red eyes
        if redeyecounter == 500:
            redeyecounter = 0
            for count in range(0,3):
                red1.on()
                red2.on()
                time.sleep(0.1)
                red1.off()
                red2.off()
                time.sleep(0.1)

        # Wait for 10 milliseconds
        time.sleep(0.01)


except KeyboardInterrupt:
    print "Stopped"

finally:
    #Cleanup
    gpioRapper.cleanup()
