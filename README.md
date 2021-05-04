# script.bike.trainer

In order for this plugin to work, you need a few things.



Here is the hardware you need:
1) Raspberry pi - I used a 3B, but any modern model that can run Kodi will do
2) An SD card to boot the OS - I am running Raspbian, however, you can chose whatever operating sytem you like
3) A reed switch and magnet
4) Some wires
5) A small breeadboard
6) A keyboard and mouse
7) An HDMI Cable
8) A TV or Monitor that supports HDMI-CEC
9) A bike trainer. This is the one I used: https://www.amazon.com/BalanceFrom-Trainer-Bicycle-Exercise-Magnetic/dp/B0872255PS/ref=sr_1_7?dchild=1&keywords=bike+trainer&qid=1620101480&sr=8-7
10) A bike that will work with the trainer
11) A 3D printer, or some way to get 3d Printed parts



Here are the instrctions for Raspbian:
1) sudo apt-get install kodi (Enter this in the terminal)
2) pip2 install cec (Enter this in the terminal) (The script runs in python 2 so you have to use python 2)
3) pip2 install easygui (Enter this in the terminal) (The script runs in python 2 so you have to use python 2)
4) pip2 install RPi.GPIO (Enter this in the terminal)
5) Download the zip file that has been precompiled by me.
6) Open Kodi
7) Go to the addons tab
8) Click install from zip file 
9) If it prompts you about something involving unknown sources, click settings and enable unknown sources.
10) After this, go back and click Install from zip file.
11) Navigate to the directory where the zip file is located and select that.
12) The plugin should install under program addons.
13) When you want to run it, click the script and it should start running


Here are the Hardware instructions:
1) Plug one end of the reed swith to the BCM port 26 (Find more information about this convention here: https://pinout.xyz/)
2) Plug the other end of the reed switch into ground
3) Plug the hdmi cable directly into the monitor or TV and make sure to enable HDMI-CEC on the device if needed.
4) Hot glue the sensor and magnet to their respective holders that you 3d printed
5) Attach these to the bike and trainer respectively.
6) Make sure that the sensor works and you are good to go!


Here are some plugins that allow you to acceess streaming services:

**Disclaimer, I did not create these. Install and use at your own risk!**

Netflix: https://howtomediacenter.com/en/install-netflix-kodi-addon/

Disney+: https://kodibeginner.com/install-disney-plus-kodi/
