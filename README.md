# Palm Beach Kings
## Raspberry Pi + PyBoard
  
**[MicroPython PyBoard](https://micropython.org/)**  
**[Python](https://www.python.org/)**  
**[Vexta Stepping motor PH266-02-A29](http://www.aasi.net/development/StepperMotors/vextaPH266-02.htm)**  
  
#### Updated 3.5.2016
  
### Final product - Features
* Keyboard input and navigation
* Stepping motor
  * Rotates platform
    * manual rotation
    * flash detection
* LCD screen/ouput
* TODO
  * fine tune motor rotation
  * tune flash detection
  
### Manual (final product)
Rotating platform with two modes:
* manual rotation with user configurable angle and speed
* automatic rotation when a camera flash is detected. User can specify angle which platform rotates.

#### Main menu
Main menu can be scrolled through with keypad"s buttons "1" and "3". "#" is used for selection.  
Menu has two items: manual rotation and flash rotation which user can choose by pressing "#".  
  
**Main menu**

| Button | Selection |
| ------ | ----------- |
| 1   | Cycle left |
| 3 | Cycle right |
| # | Enter |
  
#### Manual rotation
First row indicates current action, second row is used for additional information and keypad input.    
Default output is current angle(A) and speed(S) used and "\*" is used to exit.  
Pressing "1" is used for configuring the angle (format "XXXX" i.e. 360 degrees is 0360), "#" enters value given.  
Pressing "2" is used for configuring the speed (format "XXXX" i.e. 35 is 0035), "#" enter value given.  
Keypad button "3" starts rotation.  
Keypad button "\*" exits.  
  
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
Pressing "1" on keypad user can change rotation angle.  
Keypad button "\*" exits mode.  
Keypad button "3" starts flash detection and rotation. Platform rotates when flash is detected.  
While flash detection is active it can be stopped by pressing "\*". If platform is turning this may take few tries.  
  
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