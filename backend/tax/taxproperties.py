from enum import Enum


class Canton(Enum):
    BE = 0
    BS = 1


class Confession(Enum):
    keine_andere = 0
    roem_kath = 1
    ev_rev = 2

class CivilStatus(Enum):
    alleinstehend = 0 #includes ledig, getrennt, geschieden, verwitwet
    verheiratet = 1


