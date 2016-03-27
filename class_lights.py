#!/usr/bin/env python
"""
#####################################################################
#   code developed by: austinmeier                                  #
#   developed on: 03/25/2016                                        #
#   contact:austinmeier on github                                   #
#####################################################################
"""


###########################  Imports here  ##########################
from threading import Thread
import time
import os
from time import sleep
import RPi.GPIO as GPIO

#####################################################################
#                           GPIO pin set up
#####################################################################
#select one of these two modes:
GPIO.setmode(GPIO.BCM)      #for using the names of the pins
#or
#GPIO.setmode(GPIO.BOARD)   #for true pin number IDs (pin1 = 1)

GPIO.cleanup()             #shouldn't need to use this, but just in case

GPIO.setwarnings(True)      #set to false if the warnings bother you, helps troubleshooting

############################ Activating pins ########################
#GPIO.setup(<put pin number here>,GPIO.IN/OUT)  #will depend on setmode above, use "IN" for sensors, and "OUT" for LEDs

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)


########################### if pin is GPIO.OUT  ######################

#turning the pins on or off

#GPIO.output(18,GPIO.HIGH)   #on
#GPIO.output(18,GPIO.LOW)    #off


##########################  if pin is GPIO.IN  ########################




#####################################################################
#                           Classes
#####################################################################
class bcolors:                          #these are the color codes
    """
    Toggle switch for printing in color. Once activated, everything following is in color X

    This color class is completely unecessary, but it makes the output cooler, and doesn't really cause any harm
    if you remove it, you'll have to remove all uses of it in the functions
                        example:
    print(bcolors.YELLOW + "Warning" + bcolors.END)
    this prints "Warning" in yellow, then turns off colors, so everything printed after END will be normal
    """

    PURPLE = '\033[95m'                 #purple
    BLUE = '\033[94m'                   #blue
    GREEN = '\033[92m'                  #green
    YELLOW = '\033[93m'                 #yellow
    RED = '\033[91m'                    #red
    END = '\033[0m'                     #turns off color
    BOLD = '\033[1m'                    #turns on bold
    def disable(self):
        self.PURPLE = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.END = ''
        self.BOLD = ''



##########################  LED class  #############################
class LED:
    """
    Turns GPIO pins from LOW(off) to HIGH(on) and back again

    this class pretty much works for any device connected to a single GPIO pin
    as instances of LED are created, their names are added as keys in the LED.dictionary
    """
    dictionary  = {}                #a dictionary will all created LED instances' names as keys
    #state = None
    def __init__(self,pin,name,color,power):
        self.pin = int(pin)         #this is the GPIO pin number (will depend on GPIO config)
        self.color = color
        self.power = power          #enter power in miliamps
        self.state = None           #was going to use conditional loop if I could have got backgrounding to work
        LED.dictionary[name] = self #auto adds every instance of LED to the dictionary

    def on(self):
        self.state = "on"
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.GREEN + " on." + bcolors.END)
        GPIO.output(self.pin,GPIO.HIGH)
    def off(self):
        self.state = "off"
        GPIO.output(self.pin,GPIO.LOW)
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.RED + " off." + bcolors.END)
    def blink(self, *args):
        self.state = "blinking"
        print (len(args))
        print args
        try:
            repeat= int(args[0])
        except: repeat = 1
        try:
                speed = (float(args[1]))/2
        except: speed = .5
        print repeat
        print speed
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.PURPLE + " blinking." + bcolors.END)
        while repeat > 0:
            #print 'repeat: '+ str(repeat)
            GPIO.output(self.pin,GPIO.HIGH)
            time.sleep(speed)
            GPIO.output(self.pin,GPIO.LOW)
            time.sleep(speed)
            repeat -= 1


#####################################################################
greenLED= LED(17,"greenLED","green", 20)
redLED= LED(27,"redLED","red", 20)
yellowLED= LED(18,"yellowLED","yellow", 20)

#####################################################################
#                     Put code below this
#####################################################################

def main():
    print('\n\n\n\n\n[--system--] enter code for LED behavior: LEDname on/off/strobe\n')
    print('\nconnecting....')
    time.sleep(.2)
    print('....')
    time.sleep(.2)
    print('....')
    time.sleep(1)
    print('....')
    time.sleep(.5)
    print('connection established\n')
    print('----------------------------')
    print('  WELCOME TO THE LIGHTSHOW  ')
    print('----------------------------')
    print LED.dictionary
    while True:
        result = activitycode(LED.dictionary) 
        print('\nredLED: '+ str(redLED.state)+
                '\ngreenLED: '+ str(greenLED.state)+
                '\nyellowLED: '+ str(yellowLED.state)
             )
        if result == False:
            print "[--system--] powering down."
            redLED.blink()
            greenLED.blink()
            yellowLED.blink()
            time.sleep(2)
            GPIO.cleanup()
            break


########################  activityentered_code()  ###########################

def activitycode(choices):
    entered_code = [str(x) for x in raw_input('\n[--system--] enter code for LED behavior: LEDname on/off/blink..\n>>>').split()]
    for argument in entered_code:
        if argument in choices:
            behavior_choice_index = entered_code.index(argument)+1
            #print(argument, entered_code[behavior_choice_index])
            if entered_code[behavior_choice_index] == "on":
                choices[argument].on()
            elif entered_code[behavior_choice_index] == "off":
                choices[argument].off()
            elif entered_code[behavior_choice_index] == "blink":
                try:blinkrepeat = entered_code[behavior_choice_index + 1]
                except: blinkrepeat = None
                try:blinkspeed = entered_code[behavior_choice_index + 2]
                except: blinkspeed = None
                #background the call of LED.blink
                b1= Thread(target = choices[argument].blink, args = (blinkrepeat,blinkspeed))
                #choices[argument].blink(blinkrepeat,blinkspeed)
                b1.start()
        elif argument == "exit":
            return False

##############################################################################
#                       Executable code below:
##############################################################################

main()


"""

#Uncomment this whole set when you're ready to add the polish to the script
#it essentially just runs pin cleanup if for some reason the program freezes before it finishes
#I dont really understand it, but it came from this page: 
# http://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi


try:  
    main()
    

    while True:
        redLED.on()
        time.sleep(1)
        redLED.off()
        time.sleep(1)
        redLED.blink()
    # here you put your main loop or block of code  
    while counter < 9000000:  
        # count up to 9000000 - takes ~20s  
        counter += 1  
    print "Target reached: %d" % counter  
  
except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print "\n", counter # print value of counter  
  
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print "Other error or exception occurred!"  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit 


"""
