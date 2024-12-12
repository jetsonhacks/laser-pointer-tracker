from evdev import list_devices, InputDevice

# Function to get human-readable name for event type
def event_type_name(event_type):
    if event_type == 0x01: return "EV_KEY"
    if event_type == 0x02: return "EV_REL"
    if event_type == 0x03: return "EV_ABS"
    if event_type == 0x04: return "EV_MSC"
    if event_type == 0x11: return "EV_LED"
    if event_type == 0x12: return "EV_SND"
    if event_type == 0x14: return "EV_REP"
    if event_type == 0x15: return "EV_FF"
    if event_type == 0x16: return "EV_PWR"
    if event_type == 0x17: return "EV_FF_STATUS"
    return f"Unknown ({event_type})"

# List all input devices
devices = [InputDevice(path) for path in list_devices()]

print("Input Devices:")
for dev in devices:
    print(f"\nDevice: {dev.name}")
    print(f"Path: {dev.path}")
    print(f"Phys: {dev.phys}")
    print("Capabilities:")
    for event_type, event_codes in dev.capabilities().items():
        print(f"  - {event_type_name(event_type)}: {len(event_codes)} codes")