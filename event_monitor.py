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

    # Map of key code to modifier name
    modifier_keys = {
        evdev.ecodes.KEY_LEFTCTRL: "Ctrl",
        evdev.ecodes.KEY_RIGHTCTRL: "Ctrl",
        evdev.ecodes.KEY_LEFTSHIFT: "Shift",
        evdev.ecodes.KEY_RIGHTSHIFT: "Shift",
        evdev.ecodes.KEY_LEFTALT: "Alt",
        evdev.ecodes.KEY_RIGHTALT: "Alt",
    }

    # Track the state of pressed modifiers
    active_modifiers = set()

    # Monitor events from the devices
    print("Listening to events. Press Ctrl+C to exit.")
    while True:
        # Use select to wait for input events on multiple devices
        r, _, _ = select.select(devices, [], [])
        for dev in r:
            for event in dev.read():
                if event.type == evdev.ecodes.EV_KEY:  # Key press/release events
                    key_event = evdev.categorize(event)
                    key_code = key_event.scancode
                    key_state = key_event.keystate

                    # Handle modifier keys
                    if key_code in modifier_keys:
                        if key_state == evdev.KeyEvent.key_down:
                            active_modifiers.add(modifier_keys[key_code])
                        elif key_state == evdev.KeyEvent.key_up:
                            active_modifiers.discard(modifier_keys[key_code])

                    # Format the output with active modifiers
                    # You can check to see the keystate evdev.KeyEvent.keystate attribute
                    # This is retrieved in the key_state variable above
                    # 1. key_down (value 1) - button was pressed
                    # 2. key_up (value 0) - button release
                    # 3. key_hold (value 2) - indicates button is being held down
                    # Typically you would parse the keystroke and act on the down button action
                    modifiers = "+".join(sorted(active_modifiers))
                    if modifiers:
                        green_modifiers = f"\033[92m[{modifiers}]\033[0m"  # Wrap in green color
                        print(f"{green_modifiers} {dev.path}: {key_event}")
                    else:
                        print(f"{dev.path}: {key_event}")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Release the grab and close the devices
    for device in devices:
        device.ungrab()
        device.close()

