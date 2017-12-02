
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

    def set_dpi(self, value, name):

        value = max(50, value)
        value = int(value / 7200 * 144)
        value = min(value, 144)

        print("Finding device...")

        # find the device
        dev = usb.core.find(idVendor=0x258A, idProduct=0x0012)

        # detach the kernel driver
        dev.detach_kernel_driver(1)
        usb.util.claim_interface(dev, 1)
        dev.set_interface_altsetting(interface=1, alternate_setting=0)

        # prepare data block
        data = [0x02, 0x06, 0xbb, 0xaa, 50 + name, 0x00, 0x08, 0x00, 0x01, value, 0x00, value, 0x00, 0xff, 0xff, 0xff]

        # send the data to the mouse
        dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0302, wIndex=0x0001, data_or_wLength=data,
                          timeout=1000)

        # reclaim the device
        usb.util.release_interface(dev, 1)
        dev.attach_kernel_driver(1)


    def set_lights(self):

        print("Finding device...")

        # find the device
        dev = usb.core.find(idVendor=0x258A, idProduct=0x0012)

        # detach the kernel driver
        dev.detach_kernel_driver(1)
        usb.util.claim_interface(dev, 1)
        dev.set_interface_altsetting(interface=1, alternate_setting=0)

        # prepare data block
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

    def reset(self):

        # find the device
        dev = usb.core.find(idVendor=0x258A, idProduct=0x0012)

        # detach the kernel driver
        dev.detach_kernel_driver(1)
        usb.util.claim_interface(dev, 1)
        dev.set_interface_altsetting(interface=1, alternate_setting=0)

        # Reset data command block
        data = [0x02, 0x03, 0xbb, 0xaa, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        # send the data to the mouse
        dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0302, wIndex=0x0001, data_or_wLength=data,
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

        button1 = Gtk.Button(label="Reset Device")
        button1.connect("clicked", self.reset_device)

        label1 = Gtk.Label()
        label1.set_text("Light Mode ")

        radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "Static")
        radio1.connect("toggled", self.toggle_light_mode, "1")

        radio2 = Gtk.RadioButton.new_from_widget(radio1)
        radio2.set_label("Pulsing")
        radio2.connect("toggled", self.toggle_light_mode, "2")

        radio3 = Gtk.RadioButton.new_from_widget(radio2)
        radio3.set_label("Multi-Colour")
        radio3.connect("toggled", self.toggle_light_mode, "3")

        label2 = Gtk.Label()
        label2.set_text("Brightness ")

        radio4 = Gtk.RadioButton.new_with_label_from_widget(None, "Dim")
        radio4.connect("toggled", self.toggle_light_lumi, "1")

        radio5 = Gtk.RadioButton.new_from_widget(radio4)
        radio5.set_label("Normal")
        radio5.connect("toggled", self.toggle_light_lumi, "2")

        radio6 = Gtk.RadioButton.new_from_widget(radio5)
        radio6.set_label("Bright")
        radio6.connect("toggled", self.toggle_light_lumi, "3")

        label3 = Gtk.Label()
        label3.set_text("Pulse Speed ")

        radio7 = Gtk.RadioButton.new_with_label_from_widget(None, "Slow")
        radio7.connect("toggled", self.toggle_light_speed, "1")

        radio8 = Gtk.RadioButton.new_from_widget(radio7)
        radio8.set_label("Normal")
        radio8.connect("toggled", self.toggle_light_speed, "2")

        radio9 = Gtk.RadioButton.new_from_widget(radio8)
        radio9.set_label("Fast")
        radio9.connect("toggled", self.toggle_light_speed, "3")

        label4 = Gtk.Label()
        label4.set_text("DPI Display  ")
        label4.set_justify(Gtk.Justification.LEFT)

        radio10 = Gtk.RadioButton.new_with_label_from_widget(None, "Standard")
        radio10.connect("toggled", self.toggle_light_dpi, "1")

        radio11 = Gtk.RadioButton.new_from_widget(radio10)
        radio11.set_label("Scan")
        radio11.connect("toggled", self.toggle_light_dpi, "2")

        radio12 = Gtk.RadioButton.new_from_widget(radio11)
        radio12.set_label("Thunberbolt")
        radio12.connect("toggled", self.toggle_light_dpi, "3")

        button_set_colour = Gtk.Button(label="Apply")

        grid.attach(button1, 0, 20, 1, 1)
        grid.attach(button_set_colour, 10, 10, 1, 1)

        grid.attach(label1, 0, 0, 1, 1)
        grid.attach(radio1, 1, 0, 1, 1)
        grid.attach(radio2, 2, 0, 1, 1)
        grid.attach(radio3, 3, 0, 1, 1)

        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(radio4, 1, 1, 1, 1)
        grid.attach(radio5, 2, 1, 1, 1)
        grid.attach(radio6, 3, 1, 1, 1)

        grid.attach(label3, 0, 2, 1, 1)
        grid.attach(radio7, 1, 2, 1, 1)
        grid.attach(radio8, 2, 2, 1, 1)
        grid.attach(radio9, 3, 2, 1, 1)

        grid.attach(label4, 0, 3, 1, 1)
        grid.attach(radio10, 1, 3, 1, 1)
        grid.attach(radio11, 2, 3, 1, 1)
        grid.attach(radio12, 3, 3, 1, 1)

        self.colorchooser = Gtk.ColorChooserWidget(show_editor=True)
        Gtk.ColorChooser.set_use_alpha(self.colorchooser, False)
        box.add(self.colorchooser)

        self.colorchooser.connect('color-activated', self.set_colour)

        button_set_colour.connect("clicked", self.set_colour)

        dp1a = Gtk.Adjustment(1000, 50, 7200, 1, 10, 0)
        dp1 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=dp1a)
        dp1.set_value(1000)
        Gtk.Scale.set_digits(dp1, 0)
        dp1.connect('button-release-event', self.set_dpi, "1")
        grid.attach(dp1, 1, 11, 3, 1)
        self.dp1 = dp1

        dp1a = Gtk.Adjustment(1000, 50, 7200, 1, 10, 0)
        dp1 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=dp1a)
        dp1.set_value(2000)
        Gtk.Scale.set_digits(dp1, 0)
        dp1.connect('button-release-event', self.set_dpi, "2")
        grid.attach(dp1, 1, 12, 3, 1)
        self.dp2 = dp1

        dp1a = Gtk.Adjustment(1000, 50, 7200, 1, 10, 0)
        dp1 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=dp1a)
        dp1.set_value(3600)
        Gtk.Scale.set_digits(dp1, 0)
        dp1.connect('button-release-event', self.set_dpi, "3")
        grid.attach(dp1, 1, 13, 3, 1)
        self.dp3 = dp1

        dp1a = Gtk.Adjustment(1000, 50, 7200, 1, 10, 0)
        dp1 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=dp1a)
        dp1.set_value(7200)
        Gtk.Scale.set_digits(dp1, 0)
        dp1.connect('button-release-event', self.set_dpi, "4")
        grid.attach(dp1, 1, 14, 3, 1)
        self.dp4 = dp1

        self.radio11 = radio11
        self.radio3 = radio3
        self.radio6 = radio6
        self.radio8 = radio8

        self.set_defaults()

    def set_dpi(self, scale, event, name):

        profile.set_dpi(int(scale.get_value()), int(name) - 1)

    def set_defaults(self):

        Gtk.RadioButton.set_active(self.radio11, True)
        Gtk.RadioButton.set_active(self.radio3, True)
        Gtk.RadioButton.set_active(self.radio6, True)
        Gtk.RadioButton.set_active(self.radio8, True)

        self.dp1.set_value(1000)
        self.dp2.set_value(2000)
        self.dp3.set_value(3600)
        self.dp4.set_value(7300)

    def reset_device(self, button):
        self.set_defaults()
        profile.reset()

    def toggle_light_mode(self, button, name):

        if button.get_active():
            if name == '1':
                profile.mod = 0x01
            elif name == '2':
                profile.mod = 0x02
            elif name == '3':
                profile.mod = 0x03

    def toggle_light_lumi(self, button, name):

        if button.get_active():
            if name == '1':
                profile.bri = 0x01
            elif name == '2':
                profile.bri = 0x02
            elif name == '3':
                profile.bri = 0x03

    def toggle_light_speed(self, button, name):

        if button.get_active():
            if name == '1':
                profile.spe = 0x09
            elif name == '2':
                profile.spe = 0x07
            elif name == '3':
                profile.spe = 0x01

    def toggle_light_dpi(self, button, name):

        if button.get_active():
            if name == '1':
                profile.dpl = 0x01
            elif name == '2':
                profile.dpl = 0x02
            elif name == '3':
                profile.dpl = 0x03

    def set_colour(self, button):

        c = Gtk.ColorChooser.get_rgba(self.colorchooser)
        profile.r = int(c.red * 255)
        profile.g = int(c.green * 255)
        profile.b = int(c.blue * 255)
        profile.set_lights()


win = GridWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
