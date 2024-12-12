import usb.core
import usb.util

# Find the USB device using Vendor ID and Product ID
# Replace the idVendor and idProduct with your device
dev = usb.core.find(idVendor=0x0e8f, idProduct=0x2517)

if dev is None:
    print("Device not found")
    exit(1)

try:
    # Detach the kernel driver, if it is attached
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)
        print("Detached kernel driver from Interface 0")
    if dev.is_kernel_driver_active(1):
        dev.detach_kernel_driver(1)
        print("Detached kernel driver from Interface 1")

    # Set the active configuration
    dev.set_configuration()

    # This device has two interfaces - Your device may have more or less
    # Read data from both interfaces
    interfaces = [0, 1]
    while True:
        for intf_num in interfaces:
            # Set the interface
            usb.util.claim_interface(dev, intf_num)

            # Get the IN endpoint for the interface
            cfg = dev.get_active_configuration()
            intf = cfg[(intf_num, 0)]

            in_endpoint = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
            )

            if in_endpoint is None:
                print(f"No IN endpoint found for Interface {intf_num}")
                continue

            # Attempt to read data from the endpoint
            try:
                data = dev.read(in_endpoint.bEndpointAddress, in_endpoint.wMaxPacketSize, timeout=50)
                
                if data:
                    # The first byte represents the Report ID
                    report_id = data[0]

                    if intf_num == 0:
                        print("Data read:", data)
                        # if report_id == 0:  # Assuming Report ID 0 for navigation controls
                        #     print("Data read:", data)

                    elif intf_num == 1:
                        # Interface 1 is likely for volume control
                        if report_id == 1:  # Assuming Report ID 1 for volume controls
                            consumer_code = data[1] | (data[2] << 8)
                            print("Data read:", data)
            except usb.core.USBError as e:
                # Handle timeout errors by ignoring and continuing the loop
                if e.errno == 110:  # errno 110 corresponds to a timeout
                    continue
                else:
                    print(f"USB error: {e}")
                    break

except usb.core.USBError as e:
    print(f"USB error: {e}")
finally:
    # Release the device and reattach the kernel driver if necessary
    usb.util.dispose_resources(dev)
    try:
        if dev.is_kernel_driver_active(0) is False:
            dev.attach_kernel_driver(0)
        if dev.is_kernel_driver_active(1) is False:
            dev.attach_kernel_driver(1)
    except usb.core.USBError as e:
        print(f"Could not reattach kernel driver: {e}")
