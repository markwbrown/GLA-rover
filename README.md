# GLA-rover

I've been wanting to start a "smart car" project that drives and takes gps-tagged hemispherical photos and calculates the leaf area above it. This is the proposal for the Big Data & Brews meetup group.
***
## The Problem
Estimating the leaf area of a canopy holds great benefit in calculating how much water to give plants and when. Typical procedure is to mark a rectangle on the ground and estimate how much area within that rectangle is covered by shadow at solar noon. This is expressed as a % and used as the crop factor (Kc) in (ETc) calculations. An improved method is to take a hemispherical photo at ground level just before dawn and run it through [GLA](https://www.caryinstitute.org/science/our-scientists/dr-charles-d-canham/gap-light-analyzer-gla) (gap light analyzer). Both methods are fairly limiting in how many measurements can be taken during a day. GLA is a clunky executable built for Windows in 1999. 
![image](LAI/TSsmall.jpg)

### The Equation where LAI is useful: 

#### ETc(t) = Kc x ETo(t)
with: t = time step (days)

ETc(t) = potential crop evapotranspiration on t (mm)

ETo(t) = reference evapotranspiration on t (mm)

Kc = crop or land use factor (-)
***



## Proposal
Utilize a self-leveling gimbal (think like a ship's compass) to hold a USB camera with hemispherical lens surrounded by a neopixel ring with individually addressable LEDs to "register" North on the image. 
![image](photos/IMG_6799_.jpg)
This assembly will be mounted to the top of a small RC car equipped with GPS for use in the LAI calculation and eventually self-driving capabilities. 
![image](photos/IMG_6802_.jpg)
My neighbors have an orchard, so it'll just take me walking down the driveway to test things out. 
![image](photos/IMG_6793_.jpg)


## Possible Solutions

* Make the brains of the vehicle's navigation based on ardupilot. A mission of waypoints could be loaded to the rover which would drive the waypoint mission and a raspberry pi would capture pictures, add exif data to GPS tag them at the spot they were taken along with the relative angle the nose of the vehicle has to North/possibly calculate gap light % on board. The pi could either capture pictures at a timed interval/gps point of interest, or use a rotary encoder against one of the vehicle's wheels to calculate distance traveled.
* Use ROS (Robot Operating System - a collection of packages put out by the [Open Robotics](https://www.openrobotics.org/) group) to power a vehicle and take the photos. ROS would allow autonomous navigation around objects.
* Standard RC control - drive the car around with a remote, flip a switch to initiate the code to take a picture/calculate LAI/log to sqlite. 
* Some other variant or stack, possibly with more than one pi connected via SPI/I2C. 

***

## Parts on Hand

* Raspberry Pi 4 with CZH-Labs shield, DIN rail.
* Ardupilot 2.4.7
* APM 2.6
* An old 7.2v RC Car. It works! <- "Rock Shredder" from Radio Shack. 4w drive. Not sure gear ratio. Has basic steering wheel/trigger style remote. 
* FrSky Taranis Q X7 remote.
* FrSky X8R 8-Channel 2.4ghz ACCST&RSSI&SBus receiver (Smart port, full duplex, can also be paralleled to become a 16-Channel receiver)
* USB Hemispherical camera (ELP-USBFHD01M-180)
* USB GPS unit (G-Mouse)
* Some ABEC-5 bearings
* Some old drone LiPo batteries. 3s and 4s. 
* Various parts - Lidar lite, sonar range detectors, maybe a working usb webcam.
* Neopixel round ring - individually addressable LEDs. 
* An old prusa i3 3d printer I built back in 2014 but has been disassembled since I moved over 3 years ago. I could probably get it working again, but it is FDM and was never that great anyhow.  
* Some designs I had mocked up and 3d printed for a self-leveling gimbal (think like a ship's compass) so the hemispherical camera points straight up.
* Transistors, resistors, capacitors - I basically have a mini radio shack here. 
* Some old ESP8266 Lua chips as well as some newer NodeMCU units
* Next door neighbors have an orchard that should be a good spot to run the rover through.
* (12) 30" arrows. The arrow OD matches the ID of Abec-5 bearings. The ID of the arrows is a little over 6mm, enough room to fit the power, ground and data wires needed for the neopxel and the usb hemispherical camera. Should make for a nice axis/via in the self-leveling gimbal. I believe I will be able to cut these to length and thread the ouside to fit a M8 nut.
* Anycubic Photon Mono and 1kg resin. 

## Parts on the way

* Anycubic Wash and cure station

