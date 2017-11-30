import _socket
import json
from enum import Enum


class AreaType(Enum):
    UNKNOWN = 0
    FOREST = 1
    SWAMP = 2
    RAIN = 3
    CLOUD = 4


class Side(Enum):
    ALLY = -1
    NEUTRAL = 0
    ENEMY = 1


class UnitType(Enum):
    UNKNOWN = 0
    TANK = 1
    IFV = 2
    ARRV = 3
    HELICOPTER = 4
    FIGHTER = 5


class FacilityType(Enum):
    CONTROL_CENTER = 0
    VEHICLE_FACTORY = 1


class RewindClient():
    def __init__(self, host=None, port=None):
        self.socket = _socket.socket()
        self.socket.setsockopt(_socket.IPPROTO_TCP, _socket.TCP_NODELAY, True)
        if host is None:
            host = "127.0.0.1"
            port = 9111
        self.socket.connect((host, port))

    def close(self):
        self.socket.close()

    def _send(self, obj):
        if self.socket:
            self.socket.sendall(json.dumps(obj).encode('utf-8'))

    def circle(self, x, y, radius, color, layer=3):
        self._send({
            'type': 'circle',
            'x': x,
            'y': y,
            'r': radius,
            'color': color,
            'layer': layer
        })

    def rectangle(self, x1, y1, x2, y2, color, layer=3):
        self._send({
            'type': 'rectangle',
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'color': color,
            'layer': layer
        })

    def line(self, x1, y1, x2, y2, color, layer=3):
        self._send({
            'type': 'line',
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'color': color,
            'layer': layer
        })

    def living_unit(self, x, y, radius, hp, max_hp, rem_cooldown=0, cooldown=100,
                    selected=False, enemy=Side.NEUTRAL, course=0.0, unit_type=UnitType.UNKNOWN):
        self._send({
            'type': 'unit',
            'x': x,
            'y': y,
            'r': radius,
            'hp': hp,
            'max_hp': max_hp,
            'rem_cooldown': rem_cooldown,
            'cooldown': cooldown,
            'enemy': enemy.value,
            'course': course,
            'selected': selected,
            'unit_type': unit_type.value
        })

    def area_description(self, cell_x, cell_y, area_type=AreaType.UNKNOWN):
        self._send({
            'type': 'area',
            'x': cell_x,
            'y': cell_y,
            'area_type': area_type.value
        })

    def facility(self, cell_x, cell_y, type=FacilityType.CONTROL_CENTER, enemy=Side.NEUTRAL,
                 production=0, max_production=0, capture=0, max_capture=0):
        self._send({
            'type': 'facility',
            'x': cell_x,
            'y': cell_y,
            'enemy': enemy.value,
            'facility_type': type.value,
            'production': production,
            'max_production': max_production,
            'capture': capture,
            'max_capture': max_capture
        })

    def message(self, msg):
        self._send({
            'type': 'message',
            'message': msg
        })

    def end_frame(self):
        self._send({'type': 'end'})
