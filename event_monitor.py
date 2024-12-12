import os
import evdev
import select

# Initial path in /dev/input/by-id
base_by_id_path = "/dev/input/by-id/usb-0e8f_2517-event-kbd"

try:
    # Resolve the symbolic link to the actual eventX path
    base_event_path = os.path.realpath(base_by_id_path)
    print(f"Resolved {base_by_id_path} to {base_event_path}")

    # Extract the numeric part of eventX
    event_base = int(base_event_path.split('event')[-1])

    # Calculate the next event path
    next_event_path = f"/dev/input/event{event_base + 1}"
    print(f"Calculated next event path: {next_event_path}")

    # Paths to monitor
    device_paths = [base_event_path, next_event_path]

    # Open the devices
    devices = []
    for path in device_paths:
        try:
            device = evdev.InputDevice(path)
            devices.append(device)
            print(f"Monitoring and grabbing device: {device.name} at {path}")
            device.grab()  # Grab the device to intercept its input
        except FileNotFoundError:
            print(f"Device not found: {path}")

    if not devices:
        print("No devices found to monitor.")
        exit(1)

    # Monitor events from the devices
    print("Listening to events. Press Ctrl+C to exit.")
    while True:
        # Use select to wait for input events on multiple devices
        r, _, _ = select.select(devices, [], [])
        for dev in r:
            for event in dev.read():
                if event.type == evdev.ecodes.EV_KEY:  # Key press/release events
                    key_event = evdev.categorize(event)
                    print(f"Key event intercepted on {dev.path}: {key_event}")
                elif event.type == evdev.ecodes.EV_REL:  # Relative movement events
                    rel_event = evdev.categorize(event)
                    print(f"Relative event intercepted on {dev.path}: {rel_event}")
                elif event.type == evdev.ecodes.EV_ABS:  # Absolute axis events
                    abs_event = evdev.categorize(event)
                    print(f"Absolute event intercepted on {dev.path}: {abs_event}")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Release the grab and close the devices
    for device in devices:
        device.ungrab()
        device.close()
