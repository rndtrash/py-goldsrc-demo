from dataclasses import dataclass
from io import BytesIO

from hl1demo.utils import unpack_le


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def __str__(self):
        return f'Vector3(x: {self.x}, y: {self.y}, z: {self.z})'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        x, y, z = unpack_le('fff', binary_stream.read(4 * 3))
        return Vector3(x, y, z)


@dataclass
class Rotation:
    pitch: float
    yaw: float
    roll: float

    def __str__(self):
        return f'Rotation(pitch: {self.pitch}, yaw: {self.yaw}, roll: {self.roll})'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        p, y, r = unpack_le('fff', binary_stream.read(4 * 3))
        return Rotation(p, y, r)


@dataclass
class Camera:
    position: Vector3
    rotation: Rotation

    def __str__(self):
        return f'Camera(position: {self.position}, rotation: {self.rotation})'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        position = Vector3.from_stream(binary_stream)
        rotation = Rotation.from_stream(binary_stream)
        # TODO: but wait, there's more!

        return Camera(position, rotation)


@dataclass
class ClientData:
    position: Vector3
    rotation: Rotation
    weapon_flags: int
    fov: float

    def __str__(self):
        return f'ClientData(position: {self.position}, rotation: {self.rotation},' \
               f'weapon_flags: {hex(self.weapon_flags)}, fov: {self.fov})'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        position = Vector3.from_stream(binary_stream)
        rotation = Rotation.from_stream(binary_stream)
        weapon_flags, fov = unpack_le('If', binary_stream.read(4 + 4))

        return ClientData(position, rotation, weapon_flags, fov)
