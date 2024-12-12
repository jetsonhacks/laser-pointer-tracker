import os
import sys
import glob
import subprocess

def get_usb_info(usb_id):
    """
    Retrieves USB device information in the style of `lsusb` for the given USB ID.
    """
    try:
        # Run lsusb to get USB device information
        result = subprocess.run(['lsusb'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if usb_id in line:
                return line  # Return the matching line
    except subprocess.CalledProcessError:
        print("Error: Unable to execute lsusb.")
        sys.exit(1)
    
    print(f"USB device with ID {usb_id} not found in lsusb output.")
    sys.exit(1)

def find_device_path(usb_id):
    """
    Finds the sysfs path of a USB device given its vendor:product ID.
    """
    vendor_id, product_id = usb_id.split(":")
    try:
        # Locate the path where the device is registered in sysfs
        grep_cmd = f'grep -l "{vendor_id}" /sys/bus/usb/devices/*/idVendor'
        result = subprocess.run(grep_cmd, shell=True, capture_output=True, text=True, check=True)
        paths = result.stdout.strip().splitlines()

        for path in paths:
            # Check the product ID for matching devices
            device_path = os.path.dirname(path)
            product_file = os.path.join(device_path, "idProduct")
            if os.path.exists(product_file):
                with open(product_file, "r") as f:
                    if f.read().strip() == product_id:
                        return device_path
    except subprocess.CalledProcessError:
        print(f"Device with USB ID {usb_id} not found.")
        sys.exit(1)

    print(f"Device with USB ID {usb_id} not found.")
    sys.exit(1)

def list_drivers(device_path):
    """
    Lists the drivers associated with a given sysfs device path.
    """
    interfaces = glob.glob(os.path.join(device_path, "*:*"))

    for interface in interfaces:
        if os.path.isdir(interface):
            driver_path = os.path.join(interface, "driver")
            if os.path.islink(driver_path):
                driver_name = os.path.basename(os.readlink(driver_path))
                print(f"Interface {interface} is bound to driver: {driver_name}")
            else:
                print(f"Interface {interface} is not bound to any driver.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <usb_id>")
        print("Example: python script.py 0e8f:2517")
        sys.exit(1)

    usb_id = sys.argv[1]

    # Get USB information in lsusb style
    usb_info = get_usb_info(usb_id)
    print(usb_info)

    # Find the device path in sysfs
    device_path = find_device_path(usb_id)

    # List the associated drivers
    list_drivers(device_path)

if __name__ == "__main__":
    main()

