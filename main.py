
import usb.core
import usb.util
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class Profile:

    def __init__(self):

        self.r = 0xFF
        self.g = 0xFF
        self.b = 0x00

        self.bri = 0x03  # Brightness = 1, 2, 3
        self.mod = 0x03  # Mode: Continued, Breathing, Colourful = 1, 2, 3
        self.spe = 0x07  # Speed: Slow, Normal, Fast = 9, 7, 1
        self.dpl = 0x02  # DPI Display: Standard, Scan, Thunderbolt = 1, 2, 3


    def set_lights(self):

        print("Finding device...")

        # find the device
        dev = usb.core.find(idVendor=0x258A, idProduct=0x0012)

        # detach the kernel driver
        dev.detach_kernel_driver(1)
        usb.util.claim_interface(dev, 1)
        dev.set_interface_altsetting(interface=1, alternate_setting=0)


        # bri = 0x03  # Brightness = 1, 2, 3
        # mod = 0x01  # Mode: Continued, Breathing, Colourful = 1, 2, 3
        # spe = 0x09  # Speed: Slow, Normal, Fast = 9, 7, 1
        # dpl = 0x01  # DPI Display: Standard, Scan, Thunderbolt = 1, 2, 3

        # concatenate the colours into the expected 8 bytes
        # data = [0x07, 0x0a, 0x01, 0x00] + colors + [0x00]
        data = [0x03, 0x06, 0xbb, 0xaa,
                0x2a, 0x00, 0x0a, 0x00, self.mod, self.bri, self.spe, self.r, self.g, self.b, self.dpl, 0x01, 0x01, 0x00, 0x8f, 0x00,
                0x60, 0x91, 0x8f, 0x00, 0x58, 0x91, 0x8f, 0x00, 0x3c, 0x91, 0x8f, 0x00, 0x90, 0x91, 0x8f, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x2c, 0x92, 0x8f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00,
                0xc4, 0x41, 0x3b, 0x00, 0xf8, 0xc0, 0x2b, 0x06, 0xc0, 0xc0, 0x2b, 0x06]

        # send the data to the mouse
        dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0303, wIndex=0x0001, data_or_wLength=data,
                          timeout=1000)

        # reclaim the device
        usb.util.release_interface(dev, 1)
        dev.attach_kernel_driver(1)

profile = Profile()


class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="James Donkey 325RS Config")

        grid = Gtk.Grid(row_spacing=10, column_spacing=5)

        box = Gtk.Box()

        box.add(grid)

        self.add(box)
        self.set_border_width(30)

        button1 = Gtk.Button(label="Reset")

        label1 = Gtk.Label()
        label1.set_text("Light Mode ")
        label1.set_justify(Gtk.Justification.LEFT)
        button2 = Gtk.Button(label="Static")
        button3 = Gtk.Button(label=" Pulsing ")
        button4 = Gtk.Button(label="Multi-Colour")

        label2 = Gtk.Label()
        label2.set_text("Brightness ")
        label2.set_justify(Gtk.Justification.LEFT)
        button5 = Gtk.Button(label="Dim")
        button6 = Gtk.Button(label="Normal")
        button7 = Gtk.Button(label="Bright")

        label3 = Gtk.Label()
        label3.set_text("Pulse Speed ")
        label3.set_justify(Gtk.Justification.LEFT)
        button8 = Gtk.Button(label="Slow")
        button9 = Gtk.Button(label="Normal")
        button10 = Gtk.Button(label="Fast")

        label4 = Gtk.Label()
        label4.set_text("DPI Display  ")
        label4.set_justify(Gtk.Justification.LEFT)
        button11 = Gtk.Button(label="Standard")
        button12 = Gtk.Button(label="Scan")
        button13 = Gtk.Button(label="Thunberbolt")


        button_set_colour = Gtk.Button(label="Set Colour")

        grid.attach(button1, 0, 10, 1, 1)
        grid.attach(button_set_colour, 10, 10, 1, 1)

        grid.attach(label1, 0, 0, 1, 1)
        grid.attach(button2, 1, 0, 1, 1)
        grid.attach(button3, 2, 0, 1, 1)
        grid.attach(button4, 3, 0, 1, 1)

        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(button5, 1, 1, 1, 1)
        grid.attach(button6, 2, 1, 1, 1)
        grid.attach(button7, 3, 1, 1, 1)

        grid.attach(label3, 0, 2, 1, 1)
        grid.attach(button8, 1, 2, 1, 1)
        grid.attach(button9, 2, 2, 1, 1)
        grid.attach(button10, 3, 2, 1, 1)

        grid.attach(label4, 0, 3, 1, 1)
        grid.attach(button11, 1, 3, 1, 1)
        grid.attach(button12, 2, 3, 1, 1)
        grid.attach(button13, 3, 3, 1, 1)


        self.colorchooser = Gtk.ColorChooserWidget(show_editor=True)
        Gtk.ColorChooser.set_use_alpha(self.colorchooser, False)
        box.add(self.colorchooser)

        self.colorchooser.connect('color-activated', self.set_colour)


        button2.connect("clicked", self.set_pulse_static)
        button3.connect("clicked", self.set_pulse_breath)
        button4.connect("clicked", self.set_pulse_multi)

        button5.connect("clicked", self.set_bright_dim)
        button6.connect("clicked", self.set_bright_med)
        button7.connect("clicked", self.set_bright_max)

        button8.connect("clicked", self.set_speed_slow)
        button9.connect("clicked", self.set_speed_med)
        button10.connect("clicked", self.set_speed_fast)

        button11.connect("clicked", self.set_dpp_sta)
        button12.connect("clicked", self.set_dpp_sca)
        button13.connect("clicked", self.set_dpp_thu)

        button_set_colour.connect("clicked", self.set_colour)

    def set_pulse_static(self, button):
        profile.mod = 0x01
        profile.set_lights()

    def set_pulse_breath(self, button):
        profile.mod = 0x02
        profile.set_lights()

    def set_pulse_multi(self, button):
        profile.mod = 0x03
        profile.set_lights()

    # ---

    def set_bright_dim(self, button):
        profile.bri = 0x01
        profile.set_lights()

    def set_bright_med(self, button):
        profile.bri = 0x02
        profile.set_lights()

    def set_bright_max(self, button):
        profile.bri = 0x03
        profile.set_lights()

    # ---

    def set_speed_slow(self, button):
        profile.spe = 0x09
        profile.set_lights()

    def set_speed_med(self, button):
        profile.spe = 0x07
        profile.set_lights()

    def set_speed_fast(self, button):
        profile.spe = 0x01
        profile.set_lights()

    # ---

    def set_dpp_sta(self, button):
        profile.dpl = 0x01
        profile.set_lights()

    def set_dpp_sca(self, button):
        profile.dpl = 0x02
        profile.set_lights()

    def set_dpp_thu(self, button):
        profile.dpl = 0x03
        profile.set_lights()

    def set_colour(self, button):

        c = Gtk.ColorChooser.get_rgba(self.colorchooser)
        profile.r = int(c.red * 255)
        profile.g = int(c.green * 255)
        profile.b = int(c.blue * 255)
        print(profile.r)
        print(profile.g)
        print(profile.b)
        profile.set_lights()

win = GridWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
