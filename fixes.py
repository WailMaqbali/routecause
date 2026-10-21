# diagnosis name must match the "diagnosis" strings used in rules.json
FIXES = {
    "DHCP/IP conflict": ("Two devices were probably given the same IP address.",
                         "Restart the affected device to get a fresh address, or reserve it a fixed IP in the router settings."),
    "Undetermined":     ("No rule matched strongly.",
                         "Restart the router and device, then run a speed test and try again."),
}
DEFAULT = ("See the explanation trace below.", "Try restarting the router and affected device.")