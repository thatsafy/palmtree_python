# Palm Beach Kings
## Raspberry Pi + PyBoard

#### Updated 28.4.2016

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
* Rotate motor according to user inputs
* Integration of functionality
  * Work in progress
  * flash and motor integrated to the main functionality (see menu)
    * Working, LCD has temp, brigthness and keyboard input
  * Menu
    * move with '1' & '3', select with '#'
    * temperature/brightness & login, rotate motor with user input, rotate when flash detected

### Planned features
* Keyboard input
  * manual configuration for the rotating platform, adjust flash threshold?
    * configuring rotation angle and speed working
* Rotating platform
  * Rotate ONLY when flash detected, get rid of random turning
* Integrate all the features to the main functionality
  * menu
  
### Manual (final product)
Rotating platform with two modes:  
* manual rotation with user configurable angle and speed
* automatic rotation when a camera flash is detected. User can specify angle which platform rotates.

#### Main menu
Main menu can be scrolled through with keypad's buttons '1' and '3'. '#' is used for selection.  
Menu has two items: manual rotation and flash rotation which user can choose by pressing '#'.  
  
**Main menu**

| Button | Selection |
| ------ | ----------- |
| 1   | Cycle left |
| 3 | Cycle right |
| # | Enter |
  
#### Manual rotation
First row indicates current action, second row is used for additional information and keypad input.    
Default output is current angle(A) and speed(S) used and '*' is used to exit.  
Pressing '1' is used for configuring the angle (format 'XXXX' i.e. 360 degrees is 0360), '#' enters value given.  
Pressing '2' is used for configuring the speed (format 'XXXX' i.e. 35 is 0035), '#' enter value given.  
Keypad button '3' starts rotation.  
Keypad button '*' exits.  
  
**Default view**  

| Button | Selection |
| ------ | ----------- |
| 1   | Set angle |
| 2 | Set speed |
| 3    | Start rotation |
| *    | Exit |
  
**Angle/Speed configuration**  

| Button | Selection |
| ------ | ----------- |
| #   | Enter value |
| * | Clear |
  
#### Flash rotation
First row indicates current action, second row is used for additional information and keypad input.  
Default output is current angle(A).  
Pressing '1' on keypad user can change rotation angle.  
Keypad button '*' exits mode.  
Keypad button '3' starts flash detection and rotation. Platform rotates when flash is detected.  
While flash detection is active it can be stopped by pressing '*'. If platform is turning this may take few tries.  
  
**Default view**  

| Button | Selection |
| ------ | ----------- |
| 1   | Set angle |
| 3    | Start flash detection |
| *    | Exit |
  
**Angle/Speed configuration**  

| Button | Selection |
| ------ | ----------- |
| #   | Enter value |
| * | Clear |
  
**Flash detection active**  

| Button | Selection |
| ------ | ----------- |
| *   | Exit |