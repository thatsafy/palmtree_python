# Palm Beach Kings
## Raspberry Pi + PyBoard

### Currently working features
* measure temperature as Celsius
* measure light level as lux
* save data to mySQL database
* project data to LCD screen
* Keyboard input
  * input detected and projected to LCD
  * '*' clears, '#' sends
    * if input < 4 error message
    * otherwise send 4 digit input to raspi and over to SQL as login data
* Flash detection
  * leds turn on/off depending light level
  * when light level over threshold (camera flash) all leds turn on 

### Planned features
* Keyboard input
  * manual configuration for the rotating platform, adjust flash threshold?
* Rotating platform
  * Rotate platform when camera flash detected (light level over threshold)
* Integrate all the features to the main functionality
