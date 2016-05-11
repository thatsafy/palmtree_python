# 360&deg; Rotating Photo & Video Platform
## Raspberry Pi + PyBoard
## Palm Beach Kings

**[MicroPython PyBoard](https://micropython.org/)**  
**[Python](https://www.python.org/)**  
**[Vexta Stepping motor PH266-02-A29](http://www.aasi.net/development/StepperMotors/vextaPH266-02.htm)**  
**[LN298N Dual Motor Controller](http://tronixlabs.com.au/robotics/motor-controllers/l298n-dual-motor-controller-module-2a-australia/)**  
  
<img src="http://i.imgur.com/1ZYc8RX.png" width="320px">
  
#### Updated 10.5.2016

### Manual (final product)
Rotating platform with two modes:
* manual rotation with user configurable angle and speed
* automatic rotation when a camera flash is detected. User can specify angle which platform rotates.

#### USB-connection
Device has an USB-connection which powers the PyBoard but also can be used for file transfer for code files or  
to troubleshoot the device with command line output.  
**Linux**  
For troubleshooting/terminal output:  
Plug in the USB-cable and open a terminal emulator of your choice.  
To open connection type: sudo screen /dev/ttyACM0  
In case of screen not installed:  
*  Debian-based (Ubuntu etc.): sudo apt-get install screen
*  Red Hat-based (such as Fedora): sudo dnf install screen or sudo yum install screen
*  For other distribution please refer to the user forums and such.

With connection now opened you can do a soft reboot with CTRL+D.  
If above does not work, try pressing CTRL+C twice to stop currently operational program.  

To transfer files memory stick on the PyBoard needs to be mounted first.  
Memory stick device/partition name is in format /dev/sdX1.  
the 'X' can be determined using either lsblk or blkid. If unsure which partition is correct,  
try unplugging the USB-cable and running previous command(s) and then compare the lists.  
To mount the memory stick type: sudo mount /dev/sdX1 /mnt/usb (latter is the mount point which can be changed if wanted).  
If mount point does not exist, create one: sudo mkdir /path/to/mountpoint e.g. sudo mkdir /mnt/usb  
Now you can start transferring files with tool you prefer. Example command for 'cp':  
sudo cp file.py /mnt/usb  
  
**Windows**  
First to get terminal view:  
Software recommended to be installed/downloaded before starting:
* [PuTTY](http://www.putty.org/)
  * we recommend the standalone executable, no need for installation

First start PuTTY and you should see the basic view.  
<!--![PuTTY Default View](http://i.imgur.com/co7yBa3.png =120x)-->
<img src="http://i.imgur.com/co7yBa3.png" width="240px">  
To get the name of the address open device manager and look for 'Ports (COM & LPT).  
There get down the name of USB Serial device (example 'USB Serial Device (COM3)).  
Next in PuTTY in address type devices e.g. COM3 and speed 115200. Connection type 'serial'.  
(Optional) Save connection in saved sessions first by giving a name and clicking 'Save'.  
Connect to device using bottom 'Open' button.  
<img src="http://i.imgur.com/cvIKQQy.png" width="240px">  
  
Currently running program can be restarted with CTRL+C and CTRL+D. CTRL+C is for cancel and CTRL+D is soft reboot.  
  
File transfer:  
Files can be transferred via windows explorer and navigating to the memory stick which is connected with USB-cable previously plugged in.  
  
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
| 0   | Stop |
