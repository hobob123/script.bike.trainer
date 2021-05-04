##------------------------------------------------------------------------------------
#                              KODI Imports
##------------------------------------------------------------------------------------
import xmbc
import xbmcaddon
import xbmcgui


##-----------------------------------------------------------------------------------
#                             BIKE library imports
##-----------------------------------------------------------------------------------

#Required for Sensor
import RPi.GPIO as GPIO


#Used by the Stopwatch
from datetime import datetime


#Used by many parts of the code and the Timer
import time


#Used by the TV Class
import cec
# Credits for this ^^^^^^^^^^^^^^^^^^^^^^^^^^^
#Library from here- https://github.com/trainman419/python-cec


#Used by the HUD Class
from PIL import Image, ImageDraw
# Credits for this ^^^^^^^^^^^^^^^^^^^^^^^^^^^
# https://code-maven.com/create-images-with-python-pil-pillow


#Used for GUI without KODI
import easygui
# Credits for this ^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Library from - https://easygui.readthedocs.io/en/master/api.html

CODE_TYPE_LIST = ["Python GUI", "KODI GUI", "Terminal"]

Code_type = CODE_TYPE_LIST[1]


#Important Classes

#HUD Controls (Used to turn the TV on and off)
class TV_CEC:

    def __init__(self):
        """
        This method initializes the class TV_CEC.
        NO inputs
        """
        cec.init()
        self.tv = cec.Device(cec.CECDEVICE_TV)

        self.mute_val = False #False means Unmuted, True means Muted

    def turn_Off_TV(self):
        """
        Turns off the tv
        """
        self.tv.standby()

    def turn_On_TV(self):
        """
        Turns on the TV
        """
        self.tv.power_on()

    def change_mute_status(self):
        """
        Mutes/unmutes the TV
        """
        self.tv.toggle_mute()
        self.tv.toggle_mute()

        self.mute_val = bool(int(self.mute_val) - 1) # finds the opposite of the mute status and    sets itself to that.

    def test(self):
        """
        Checks to see if class is working
        """
        self.turn_On_TV()
        self.turn_Off_TV()
        self.turn_On_TV()
        self.turn_Off_TV()
        self.turn_On_TV()
        self.change_mute_status()
        self.change_mute_status()
        self.change_mute_status()
        self.change_mute_status()

#HUD Controls (Used to generate images to show the user)
class HUD_Pictures:
    def __init__(self, distance = 0, rpm = 0.0, mph = 0.0, time_biked = [0, 0, 0], name = "-1"):
        """
        Initialization
        No inputs required.
        Name should be initialized here
        """
        self.distance = distance

        self.rpm = rpm

        self.mph = mph

        self.time_biked = time_biked

        self.name = name

        self.stats = Image.new("RGB", (500, 100), color = 0)

        self.stats.save("Stats.png")

        self.warning = Image.new("RGB", (500, 100), color = (255, 0 , 0))

        self.warning.save("Warning.png")

##-----------------------------------------------------------------------------------
#   Kodi doesn't constantly update skin images, so this hasn't been incorporated yet
##-----------------------------------------------------------------------------------
    def createStatsImage(self, debug = False):
        """
        Shows the statistics in a nice little rectangle that can go at the top right of the screen
        """
        self.stats = Image.new("RGB", (500, 100), color = 0)
        d = ImageDraw.Draw(self.stats)

        if self.name == "-1":
            d.text((10,5), "Here are your biking stats:", fill=(255,255,0))

        else:
            d.text((10,5), "Here are your biking stats " + self.name + ":", fill=(255,255,0))

        #d.text((10,25), "You have traveled " + str(self.distance) + " miles", fill = (255,255,0))

        d.text((10,45), "Wheel RPM: " + str(self.rpm), fill = (255,255,0))

        d.text((10,65), "MPH: " + str(self.mph), fill = (255,255,0))

        d.text((10,85), "You have been biking for " + str(self.time_biked[0]) + " hours "  + str(self.time_biked[1]) + " minutes, and " + str(round(self.time_biked[2])) + " seconds", fill = (255,255,0))

        self.stats.save("/home/pi/Desktop/ICSoftware/Stats.jpeg")
        
        self.stats.save("/home/pi/.kodi/addons/skin.apptv/media/HUD.jpeg")
        
        if debug == True:
            self.stats.show()

    def createWarningImage(self, time_remaining = [0, 0], debug = False):
        """
        Input: A List showing how much time is left

        Shows a warnign telling the user how long they have until their TV turns off
        """
        self.warning = Image.new("RGB", (500, 100), color = (255, 0 , 0))
        draw = ImageDraw.Draw(self.warning)

        draw.text((100,45), "Shutting down in: " + str(time_remaining[0]) + " minutes and " + str (time_remaining[1]) + " seconds", fill = (255,255,255))
        draw.text((125,65), "Start biking in order to unmute TV")
        
        self.warning = self.warning.resize((1000,200), Image.ANTIALIAS)
        
        self.warning.save("/home/pi/Desktop/ICSoftware/Warning.jpeg")
        
        self.warning.save("/home/pi/.kodi/addons/skin.apptv/media/HUD.jpeg")
        
        if debug == True:
            self.warning.show()


#Important Functions:
def get_now_time():
        """
        Used to get the current time as a list.
        """
        a = str(datetime.time(datetime.now()))

        rlis = a.split(":")

        count = 0

        #print(rlis)

        rlis[0] = int(rlis[0])
        rlis[1] = int(rlis[1])
        rlis[2] = float(rlis[2])

        #print (rlis)

        return rlis

def miles_per_hour(rpm, wheel_diameter = 26):
    """
    Takes a rpm value (int or float)
    default wheel = 26, but can be changed

    returns float of 
    """
        IN_Per_MIN = rpm * wheel_diameter * 3.1415

        IN_Per_HR = IN_Per_MIN * 60

        mph = IN_Per_HR / 63360

        return mph

##-----------------------------------------------------------------------------------
#              Initializes objects and variables used in the Main loop
##-----------------------------------------------------------------------------------

TV = TV_CEC()

HUD = HUD_Pictures()


#Variables
flag = False
rpm = 0.0

start = []
end = []

threshold = 0

Time_Started = []

name = "-1"

#Set up the GPIO ports to get sensor reading
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

MAGNET_GPIO = 26
GPIO.setup(MAGNET_GPIO,   GPIO.IN,   pull_up_down = GPIO.PUD_UP) # GPIO Assign mode



##-----------------------------------------------------------------------------------
#           gets the threshold value from user *KODI GUI Not developed yet*
##-----------------------------------------------------------------------------------
if Code_type == "Python GUI":
    threshold = int(easygui.buttonbox("Select your RPM Threshold", "Setting the RPM Threshold", ("5","10","15","20","25","30")))
    tryname   = easygui.textbox(msg="enter your name. If you don't want to enter that information don't change anything and hit ok", title="Name", text="enter your name")

    if (tryname == "enter your name"):
        name = "-1"

    else:
        name = tryname


#Needs development
if Code_type == "KODI GUI":
    threshold = 10
    name = "-1"


if Code_type == "Terminal":
    tryname = ""
    threshflag = False
    while True:
        if threshflag == True:
            break

        try:
            threshold = int(input("Enter RPM Threshold:  "))

            threshflag = True

        except ValueError:
            print("please enter a valaid int", str(threshold))
            threshflag = False



        tryname = str(input("Enter your name or enter N/A to skip this:   "))

        if (tryname == "N/A"):
            name = "-1"

        else:
            name = tryname

        print(name)


##------------------------------------------------------------------------------------
#                             Kodi Specific code
##------------------------------------------------------------------------------------

ADDON = xbmcaddon.Addon()

path = ADDON.getAddonInfo('path').decode('utf-8')


warning5min = xbmcgui.WindowXML("Custom_1198_5min.xml", path, defaultRes = "1080i", isMedia = True)

warning1min = xbmcgui.WindowXML("Custom_1197_1min.xml", path, defaultRes = "1080i", isMedia = True)

warning5sec = xbmcgui.WindowXML("Custom_1199_5sec.xml", path, defaultRes = "1080i", isMedia = True)

##------------------------------------------------------------------------------------
#                                Main loop
##------------------------------------------------------------------------------------

#Create a stopwatch to sense how long someone has been biking for


time_Started = get_now_time()

while (__name__ == "__main__"):
    warning5min = xbmcgui.WindowXML("Custom_1198_5min.xml", path, defaultRes = "1080i", isMedia = True)

    warning1min = xbmcgui.WindowXML("Custom_1197_1min.xml", path, defaultRes = "1080i", isMedia = True)

    warning5sec = xbmcgui.WindowXML("Custom_1199_5sec.xml", path, defaultRes = "1080i", isMedia = True)


    #Does the RPM from the GPIO thing
    lastrpm = rpm

    if (GPIO.input(MAGNET_GPIO) == 0):
        if (flag == False):
            print("start")
            start = get_now_time()
            flag = True

    if (GPIO.input(MAGNET_GPIO) == 1):
        if (flag == True):
            print("stop")
            end = get_now_time()
            flag = False

            dtimelis = [end[0]-start[0], end[1] - start[1], end[2]- start[2]]

            dtime = dtimelis[0]*3600 + dtimelis[1]*60 + dtimelis[2]

            rpm = 60/dtime

    rpm = (rpm + lastrpm)/2

    print (rpm)

    #If the RPM is less than the threshold, this triggers
    if rpm < threshold:
        print("Low RPM")
        TVFlag = True
        listime = [5,0]
        timeremaining = listime.copy()
        #loop for the timer
        for i in range (listime[0]*60 + listime[1]):
            

            #This is the display for the warning images
            if ((timeremaining[0] == 5) or (timeremaining[0] == 4)  or (timeremaining[0] == 3) or (timeremaining[0] == 2)):
                warning5min.doModal()

            else:
                try:
                    del warning5min
                except:
                    pass

            
            if (timeremaining[0] == 1):
                warning1min.doModal()

            else:
                try:
                    del warning1min
                except:
                    pass

            
            if ((timeremaining[0] == 0) and (timeremaining[1] <= 5)):
                warning5sec,doModal()

            else:
                try:
                    del warning5sec
                except:
                    pass


            print(timeremaining)
            #creates a warning image
            HUD.createWarningImage(time_remaining = timeremaining)

            #does some stuff that allows the timer to be displayed in the warning
            if timeremaining[1] == 0:
                if timeremaining[0] == 0:
                    TVFlag = False
                else:
                    timeremaining[0] -= 1
                    timeremaining[1] = 59
            else:
                timeremaining[1] -= 1



            #checks the RPM so that the program can see if the user has picked up speed to unpause
            if (GPIO.input(MAGNET_GPIO) == 0):
                if (flag == False):
                    print("start")
                    start = get_now_time()
                    flag = True


            if (GPIO.input(MAGNET_GPIO) == 1):
                if (flag == True):
                    print("stop")
                    end = get_now_time()
                    flag = False

                    dtimelis = [end[0]-start[0], end[1] - start[1], end[2]- start[2]]

                    dtime = dtimelis[0]*3600 + dtimelis[1]*60 + dtimelis[2]

                    rpm = 60/dtime
            rpm = (rpm + lastrpm)/2


            if rpm > threshold:
                #If they have picked up, the program will leave the timer loop and go back to the main if statement
                print("User sped up")
                TVFlag = False
                TV.turn_On_TV()

                #Creates an image with stats

                current_time = get_now_time()

                time_elapsed = [current_time[0] - time_Started[0],
                                current_time[1] - time_Started[1],
                                current_time[2] - time_Started[2]]


                HUD.rpm = rpm
                HUD.mph = miles_per_hour(rpm)
                HUD.time_biked = time_elapsed
                HUD.name = name
                HUD.createStatsImage()
                break

            time.sleep(1)


        #If the loop ends without a break or other condition, it turns off the TV
        if TVFlag == True:
            print("TV OFF")
            TV.turn_Off_TV()

    else:
        #Turns on the TV
        TV.turn_On_TV()

        #Creates an image with stats

        current_time = get_now_time()

        time_elapsed = [current_time[0] - time_Started[0],
                        current_time[1] - time_Started[1],
                        current_time[2] - time_Started[2]]


        HUD.rpm = rpm
        HUD.mph = miles_per_hour(rpm)
        HUD.time_biked = time_elapsed
        HUD.name = name
        HUD.createStatsImage()


    #Sleeps in order for the RPM sensing to work
    time.sleep(0.1)