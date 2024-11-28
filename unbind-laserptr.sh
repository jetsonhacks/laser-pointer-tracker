#!/bin/bash

# Default Vendor ID and Product ID
# 0e8f:2517 GreenAsia Inc. 
DEFAULT_VID="0e8f"
DEFAULT_PID="2517"

# Initialize VID and PID with default values
VID=$DEFAULT_VID
PID=$DEFAULT_PID

# Function to display help message
print_help() {
  echo "Usage: $0 [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  --vid <vendor_id>    Set the Vendor ID (default: $DEFAULT_VID)"
  echo "  --prod <product_id>  Set the Product ID (default: $DEFAULT_PID)"
  echo "  -h, --help           Show this help message and exit"
  echo ""
  echo "Example:"
  echo "  $0 --vid 0e8f --prod 1234"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --vid)
      VID="$2"
      shift 2
      ;;
    --prod)
      PID="$2"
      shift 2
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Use --help to see the available options."
      exit 1
      ;;
  esac
done

echo "Using Vendor ID: $VID and Product ID: $PID"

# Search for the correct USB device using Vendor ID and Product ID
for device in /sys/bus/usb/devices/*; do
  if [ -f "$device/idVendor" ] && [ -f "$device/idProduct" ]; then
    DEVICE_VID=$(cat "$device/idVendor")
    DEVICE_PID=$(cat "$device/idProduct")

    if [ "$DEVICE_VID" == "$VID" ] && [ "$DEVICE_PID" == "$PID" ]; then
      echo "Found device with Vendor ID: $DEVICE_VID and Product ID: $DEVICE_PID at $device"

      # Loop through each interface and unbind from usbhid
      for interface in "$device"/*:*; do
        DRIVER_PATH="$interface/driver"
        if [ -L "$DRIVER_PATH" ]; then
          DRIVER_NAME=$(basename "$(readlink "$DRIVER_PATH")")
          if [ "$DRIVER_NAME" == "usbhid" ]; then
            INTERFACE_NAME=$(basename "$interface")
            echo "Unbinding interface: $INTERFACE_NAME from usbhid driver"
            echo "$INTERFACE_NAME" | sudo tee /sys/bus/usb/drivers/usbhid/unbind
          fi
        fi
      done
    fi
  fi
done
