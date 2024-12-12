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
There is a udev rule for the demo device in 99-laser-usb.rules. Copy it over to /etc/udev/rules.d and enable it.

```
sudo cp 99-laser-usb.rules /etc/udev/rules.d
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Note
The device is part of the 'input' group. You could add yourself to the input group instead of adding the udev rule. However, this is usually thought of as a security creep. Instead of adding just one device, there is potential for adding many using this approach and the advice is to be as specific as possible.


## Releases
### November 2024
* Initial Release
