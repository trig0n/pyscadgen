from os.path import join
from solid.utils import *

from Case import Case
from pin import Pin

SEGMENTS = 42
NAME = "esp8266"


class ESP8266:
    length = 57.5
    width = 31
    height = 1.6

    hole_diameter = 3.4

    usb_port = {
        "length": 5.7 + 5,
        "width": 7.5,
        "height": 2.7,
        "left": 5.7 - 4.65,
        "up": height,
        "forward": width / 2 - 7.5 / 2
    }

    usb_port_noose = {
        "length": usb_port["length"] - 5.05,
        "width": 7.95,
        "height": 2.95,
        "down": (2.95 - usb_port["height"]) / 2,
        "back": (7.95 - usb_port["width"]) / 2
    }

    btn = {
        "length": 4,
        "width": 3,
        "height": 3.2 - height,
        "up": height,
        "right": 2
    }

    btn_cylinder = {
        "diameter": 1.5,
        "height": 3.65 - (btn["height"] + height),
        "up": height + btn["height"],
        "right": 4,
        "forward": 1.5
    }

    rst_btn = {
        "forward": 6
    }

    flash_btn = {
        "forward": 22
    }

    esp8266_base_chip = {
        "length": 24.2,
        "width": 16.2,
        "height": 2.4 - height,
        "forward": 23.75 - 16.2,
        "right": 57.95 - 24.2,
        "up": height
    }

    esp8266_chip = {
        "length": 15.10,
        "width": 12.05,
        "height": 4.65 - (height + esp8266_base_chip["height"]),
        "forward": (esp8266_base_chip["width"] - 12.05) / 2,
        "up": height + esp8266_base_chip["height"],
        "right": (esp8266_base_chip["length"] - 22.8)
    }

    electronics_plane = {
        "length": 27.5,
        "width": width - 5,
        "height": usb_port["height"],
        "forward": 2.5,
        "right": 6,
        "up": height
    }

    hole_offsets = [
        {"right": 1.3 + hole_diameter / 2, "forward": 2},
        {"right": 1.3 + hole_diameter / 2, "forward": 29},
        {"right": length - (0.95 + hole_diameter / 2), "forward": 2},
        {"right": length - (0.95 + hole_diameter / 2), "forward": 29}
    ]

    def __init__(self, has_pins=True):
        self.has_pins = has_pins

    def assemble(self):
        base = cube([self.length, self.width, self.height])

        _hole_cylinder = hole()(cylinder(d=self.hole_diameter, h=100, center=True))
        _holes = []
        for o in self.hole_offsets:
            _holes.append(right(o["right"])(forward(o["forward"])(_hole_cylinder)))

        base += _holes

        _o = []
        _cube_port = cube([self.usb_port["length"], self.usb_port_noose["width"], self.usb_port["height"]])
        _o.append(back(self.usb_port_noose["back"])(
            down(self.usb_port_noose["down"])(cube([self.usb_port_noose["length"],
                                                    self.usb_port_noose["width"],
                                                    self.usb_port_noose["height"]]))))

        _o.append(
            forward(self.width / 2 - self.usb_port["width"] / 2)(left(self.usb_port["left"])(up(self.height - 0.4)(
                _cube_port))))

        btn = right(self.btn["right"])(
            up(self.btn["up"])(cube([self.btn["length"], self.btn["width"], self.height])))
        btn += forward(self.btn_cylinder["forward"])(right(self.btn_cylinder["right"])(up(self.btn_cylinder["up"])(
            cylinder(d=self.btn_cylinder["diameter"], h=self.btn_cylinder["height"]))))
        _o.append(forward(self.rst_btn["forward"])(btn))
        _o.append(forward(self.flash_btn["forward"])(btn))

        _esp8266_chip = up(self.height)(cube([self.esp8266_base_chip["length"],
                                              self.esp8266_base_chip["width"],
                                              self.esp8266_base_chip["height"]]))
        _esp8266_chip += forward(self.esp8266_chip["forward"])(up(self.esp8266_chip["up"])(
            right(self.esp8266_chip["right"])(cube([self.esp8266_chip["length"],
                                                    self.esp8266_chip["width"],
                                                    self.esp8266_chip["height"]]))
        ))

        _o.append(forward(self.esp8266_base_chip["forward"])(right(self.esp8266_base_chip["right"])(_esp8266_chip)))
        _o.append(forward(self.electronics_plane["forward"])(
            up(self.electronics_plane["up"])(
                right(self.electronics_plane["right"])(
                    cube([self.electronics_plane["length"],
                          self.electronics_plane["width"],
                          self.electronics_plane["height"]])
                )
            )
        ))

        if self.has_pins:
            p = Pin(pin_diameter=1, pcb_height=self.height)
            for i in range(0, 15):
                _o.append(forward(0.25)(right(10 + i * p.base_width)(down(p.base_width)(p.assemble()))))
                _o.append(back(0.25)(right(10 + i * p.base_width)(
                    down(p.base_width)(forward(self.width - p.base_width)(p.assemble())))))

        base += _o

        return base


class ESP8266Case(Case):
    positive = ESP8266

    def finish(self, base):
        base += left(self.wall_thickness)(up(ESP8266.usb_port["up"])(forward(ESP8266.usb_port["forward"])(hole()(
            cube([self.wall_thickness + ESP8266.usb_port["length"],
                  ESP8266.usb_port_noose["width"],
                  ESP8266.usb_port["height"]])))))

        base += down(1.25)(right(10)(forward(2.5)(hole()(cube([ESP8266.length - 10, ESP8266.width - 5, 1.25])))))
        base += down(self.wall_thickness)(forward(ESP8266.width / 2 - 5)(
            right(ESP8266.length)(hole()(cube([1, 10, self.wall_thickness * 2 + ESP8266.height])))))
        return base


if __name__ == '__main__':
    scad_render_to_file(ESP8266().assemble(), join('./out/', NAME + ".scad"), file_header='$fn = 42;')
    scad_render_to_file(ESP8266Case().bottom(), join('./out/', NAME + "_bottom.scad"), file_header='$fn = 42;')
    scad_render_to_file(ESP8266Case().top(), join('./out/', NAME + "_top.scad"), file_header='$fn = 42;')
