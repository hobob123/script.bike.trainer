CODE_TYPE_LIST = ["Python GUI", "KODI GUI", "Terminal"]
Code_type = CODE_TYPE_LIST[1]

##------------------------------------------------------------------------------------
#                              KODI Imports
##------------------------------------------------------------------------------------
if Code_type == CODE_TYPE_LIST[1]:
    import xbmc
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


#Used for GUI without KODI
if (Code_type == CODE_TYPE_LIST[0]):
    import easygui

# Credits for this ^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Library from - https://easygui.readthedocs.io/en/master/api.html



#Important Classes

#TVControls (Used to turn the TV on and off)
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
KODIDialog = xbmcgui.Dialog()

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
    threshold = int(KODIDialog.select("Chose an RPM Threshold", ["5", "10", "15", "20"]))
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


##------------------------------------------------------------------------------------
#                                Main loop
##------------------------------------------------------------------------------------

#Create a stopwatch to sense how long someone has been biking for


time_Started = get_now_time()

while (__name__ == "__main__"):

    #Does the RPM from the GPIO thing

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



    print (rpm)

    #If the RPM is less than the threshold, this triggers
    if rpm < threshold:
        print("Low RPM")
        TVFlag = True
        listime = [5,0]
        timeremaining = listime[:]
        #loop for the timer
        for i in range (listime[0]*60 + listime[1]):

            KODIDialog.yesno("Time Remaining", "You have " + str(timeremaining[0]) + " Minutes and " + str(timeremaining[1]) + " Seconds until the TV turns off! Start biking!", autoclose = 750)

            print(timeremaining)
            #creates a warning image

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





    #Sleeps in order for the RPM sensing to work
    time.sleep(0.1)