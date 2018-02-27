from os.path import join

from solid.utils import *

from esp8266 import ESP8266

SEGMENTS = 42
NAME = "doorESPCase"


class DoorESPCase:
    length = ESP8266.length
    width = ESP8266.width
    height = ESP8266.height

    def __init__(self, extra=8):
        self.esp = ESP8266()
        self.length += extra
        self.width += extra
        self.height += extra
        self.extra = extra

    def assemble(self):
        case = cube([self.length, self.width, self.height])
        case += up(self.height / 2 - self.esp.height / 2)(forward(self.extra / 2)(hole()(ESP8266().assemble())))
        return case

    def upper_half(self):
        case = self.assemble()
        case += hole()(cube([self.length, self.width, self.height / 2]))
        return case

    def lower_half(self):
        case = self.assemble()
        case += up(self.height / 2)(hole()(cube([self.length, self.width, self.height / 2])))
        return case


if __name__ == '__main__':
    scad_render_to_file(DoorESPCase().lower_half(), join('./out/', NAME + ".scad"), file_header='$fn = %s;' % SEGMENTS)
