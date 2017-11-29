A basic GUI for configuring mouse **James Donkey 325RS** on Linux
___

Not thoroughly tested. Use at your own risk.

Currently can set colour, pulse mode and pulse speed.


Requires: `python-pyusb` and GTK3

To start run `python3 run.py`

___

Note: Not tested on the non 'RS' version. I assume it won't work since the offical driver recognises it as a different mouse.

Note: Changing settings seems to cause DPI display animations to loop continuously, as does the official driver. You can reset to default by clicking 'Reset Device' or you could leave the DPI display mode as 'static'.
