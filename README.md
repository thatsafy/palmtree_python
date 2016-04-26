# Palm Beach Kings
## Raspberry Pi + PyBoard

#### Updated 26.4.2016

### Currently working features
* measure temperature as Celsius
* measure light level as lux
* save data to MySQL database
* project data to LCD screen
* Keyboard input
  * input detected and projected to LCD
  * '*' clears, '#' sends
    * if input < 4 error message
    * otherwise send 4 digit input to raspi and over to SQL as login data
* Flash detection
  * when light level over threshold (camera flash) leds turn on
  * motor turning when flash detected
    * needs some calibration, turns by itself at times
* Integration of functionality
  * Work in progress
  * flash and motor integrated to the main functionality
    * Working, LCD has temp, brigthness and keyboard input

### Planned features
* Keyboard input
  * manual configuration for the rotating platform, adjust flash threshold?
* Rotating platform
  * Rotate ONLY when flash detected, get rid of random turning
* Integrate all the features to the main functionality
  * menu

