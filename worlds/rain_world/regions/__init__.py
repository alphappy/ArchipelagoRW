from . import rooms, abstract, gates
from .. import RainWorldOptions


def generate(options: RainWorldOptions):
    reg1, conn1 = rooms.generate(options)
    reg2, conn2 = abstract.generate(options)
    g = gates.generate(options)

    return reg1 + reg2, conn1 + conn2, g
