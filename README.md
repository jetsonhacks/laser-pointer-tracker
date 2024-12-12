# laser-pointer-tracker

Generic laser presentation pointers are inexpensive, and a cheap way to experiment with computer vision input.

Using the code and tools here, we cobble together a laser pointer tracker using OpenCV.

This is a simple way to track a red laser pointer. It is not fully robust (there are many ideas to explore), but 
works well enough under many lighting situations.

There is also code to help in reading the buttons of a presentation pointer. Typically these buttons control Page Up,
Page Down, Tab, Volume Increment and Volume Decrement. There are usually other values available. Most of these types
of devices have little implementation documentation, so it's necessary to play with them a little to see the output.

## Dependencies
The Python dependencies are in requirements.txt. To install, pip must be installed. The scripts are written for Python 3. To install:
```
pip3 install -r requirements.txt
```
### Note
For the video tutorial, we use the pyusb module. The evdev module interface reads and translates the button events in the main script. There are many ways to interface with the USB subsystem, these may or may not meet your requirements.


## Permissions
Typically you will add yourself (the user) to the 'input' group to be able to access the device.
```
sudo usermod -aG input $USER
```
You will need to log out/in or restart for the changes to take effect.

There is an example udev rule for the demo device in 99-laser-usb.rules. You may not need it (this device does not). If you do, modify the file appropriately and copy it over to /etc/udev/rules.d and enable it.

```
sudo cp 99-laser-usb.rules /etc/udev/rules.d
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Releases
### December 2024
* Added tutorial section
  
### November 2024
* Initial Release
