# GLA-rover

I've been wanting to start a "smart car" project that drives and takes gps-tagged hemispherical photos and calculates the leaf area above it. This is the proposal for the BigData&Brews meetup group.
***
## The Problem
Estimating the leaf area of a canopy holds great benefit in calculating how much water to give plants and when. Typical procedure is to mark a rectangle on the ground and estimate how much area within that rectangle is covered by shadow at solar noon. This is expressed as a % and used as the crop factor (Kc) in (ETc) calculations. An improved method is to take a hemispherical photo at ground level just before dawn and run it through [GLA](https://www.caryinstitute.org/science/our-scientists/dr-charles-d-canham/gap-light-analyzer-gla) (gap light analyzer). Both methods are fairly limiting in how many measurements can be taken during a day. GLA is a clunky executable built for Windows in 1999. 

### The Equation where LAI is useful: 

#### ETc(t) = Kc x ETo(t)
with: t = time step (days)

ETc(t) = potential crop evapotranspiration on t (mm)

ETo(t) = reference evapotranspiration on t (mm)

Kc = crop or land use factor (-)
***

## Possible Solutions

* Make the brains of the vehicle's navigation based on ardupilot. A mission of waypoints could be loaded to the rover which would drive the waypoint mission and a raspberry pi would capture pictures, add exif data to GPS tag them at the spot they were taken/possibly calculate gap light %. The pi could either capture pictures at a timed interval or use a rotary encoder against one of the vehicle's wheels to calculate distance traveled. 
* Use ROS (Robot Operating System - a collection of packages put out by the [Open Robotics](https://www.openrobotics.org/) group) to power a vehicle and take the photos. ROS would allow autonomous navigation around objects.
* Roll-your-own stack. OpenCV for image detection/object recognition/navigation. Snap photos, GPS tag, etc.
* Some other variant, possibly with more than one pi connected via SPI/I2C. 

***

## Parts on Hand

* Raspberry Pi 4 with CZH-Labs shield, DIN rail.
* Ardupilot 2.4.7
* APM 2.6
* An old 7.2v RC Car. It works! <- "Rock Shredder" from Radio Shack. 4w drive. Not sure gear ratio. Has basic steering wheel/trigger style remote. 
* FrSky Taranis Q X7 remote. 
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
