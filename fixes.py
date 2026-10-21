FIXES = {
 "Router power/hardware fault": ("The router isn't getting or holding power properly.", "Check the power adapter and socket, try another outlet, and replace the adapter or router if the light stays off or red."),
 "WAN link down": ("The router has lost its connection to the internet.", "Check the cable from modem to router, power-cycle the modem, then check your ISP's outage page."),
 "Router needs restart": ("The router's software has probably hung.", "Unplug the router for 30 seconds, plug it back in and wait 2 minutes."),
 "Faulty firmware update": ("A recent firmware update may have broken something.", "Reboot, then check the vendor site for a fixed version or roll back to the previous firmware."),
 "DHCP/IP conflict": ("Two devices were probably given the same IP address.", "Restart the affected device to get a fresh address, or reserve it a fixed IP in the router settings."),
 "DNS failure": ("Your devices can't translate site names into addresses reliably.", "Change DNS to 1.1.1.1 or 8.8.8.8 in the router or device settings, then restart."),
 "Weak signal/distance": ("The device is too far from the router or blocked by walls.", "Move the router or device closer, or add a mesh node or access point."),
 "Channel congestion": ("Neighbouring networks are crowding your Wi-Fi channel.", "Switch to 5GHz and change the router's Wi-Fi channel to a less busy one."),
 "2.4GHz interference": ("Other household devices are interfering with the 2.4GHz band.", "Move to 5GHz, keep the router away from microwaves and cordless phones."),
 "Bandwidth saturation": ("Too many devices are using the connection at once.", "Pause large downloads or streams, or enable QoS in the router settings."),
 "Device adapter/settings fault": ("The affected device's Wi-Fi adapter or settings are the problem.", "Forget and rejoin the network, update the Wi-Fi driver, or restart the device."),
 "Plan/speed mismatch": ("The line is delivering less than your plan promises.", "Test with a wired connection directly to the router and contact your ISP with the results."),
 "Undetermined": ("No rule matched strongly.", "Restart the router and device, then run a speed test and try again."),
}
DEFAULT = ("See the explanation trace below.", "Try restarting the router and affected device.")