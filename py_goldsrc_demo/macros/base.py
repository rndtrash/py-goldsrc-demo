import os
from dataclasses import dataclass
from io import BytesIO

from py_goldsrc_demo.data_types import ClientData, NetMsg, Event, Sound
from py_goldsrc_demo.macros import BaseMacro
from py_goldsrc_demo.utils import unpack_le, read_binary_string


@dataclass
class ClientDataMacro(BaseMacro):
    client_data: ClientData

    def __str__(self):
        return 'ClientDataMacro(' \
               f'time: {self.time}, frame: {self.frame},' \
               f'client_data: {self.client_data}' \
               ')'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        return ClientDataMacro(base_macro.type, base_macro.time, base_macro.frame,
                               ClientData.from_stream(binary_stream))


@dataclass
class SoundMacro(BaseMacro):
    sound: Sound

    def __str__(self):
        return f'SoundMacro(sound: {self.sound})'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        sound = Sound.from_stream(binary_stream)

        return SoundMacro(base_macro.type, base_macro.time, base_macro.frame, sound)


@dataclass
class NetMsgMacro(BaseMacro):
    net_msg: NetMsg

    def __str__(self):
        return f'NetMsgMacro(net_msg: {self.net_msg})'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        net_msg = NetMsg.from_stream(binary_stream)

        return NetMsgMacro(base_macro.type, base_macro.time, base_macro.frame, net_msg)


@dataclass
class DemoBufferMacro(BaseMacro):
    buffer: bytes

    def __str__(self):
        return f'DemoBufferMacro(buffer: {self.buffer})'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        buffer_length, = unpack_le('i', binary_stream.read(4))
        buffer = binary_stream.read(buffer_length)

        return DemoBufferMacro(base_macro.type, base_macro.time, base_macro.frame, buffer)


@dataclass
class WeaponAnimMacro(BaseMacro):
    anim: int
    body: int

    def __str__(self):
        return f'WeaponAnimMacro(anim: {self.anim}, body: {self.body})'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        anim, body = unpack_le('ii', binary_stream.read(4 * 2))

        return WeaponAnimMacro(base_macro.type, base_macro.time, base_macro.frame, anim, body)


@dataclass
class ConsoleCommandMacro(BaseMacro):
    command: str

    def __str__(self):
        return f'ConsoleCommandMacro(command: {self.command})'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        command = read_binary_string(binary_stream, 64)

        return ConsoleCommandMacro(base_macro.type, base_macro.time, base_macro.frame, command)


@dataclass
class EventMacro(BaseMacro):
    event: Event

    def __str__(self):
        return f'EventMacro(event: {self.event})'

    @staticmethod
    def from_base_macro(base_macro: BaseMacro, binary_stream: BytesIO):
        event = Event.from_stream(binary_stream)

        return EventMacro(base_macro.type, base_macro.time, base_macro.frame, event)
