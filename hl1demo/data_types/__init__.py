from dataclasses import dataclass
from io import BytesIO

from hl1demo.exceptions import InvalidNetMsgLength
from hl1demo.utils import unpack_le, unpack_be, read_binary_string

NET_MESSAGE_LENGTH_MIN = 0
NET_MESSAGE_LENGTH_MAX = 65536


@dataclass
class Rect:
    a: int
    b: int
    c: int
    d: int

    def __str__(self):
        return f'Rect(a: {self.a}, b: {self.b}, c: {self.c}, d: {self.d})'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        a, b, c, d = unpack_le('iiii', binary_stream.read(4 * 4))
        return Rect(a, b, c, d)


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
class RefParams:
    view_org: Vector3
    view_angles: Rotation
    forward: Vector3
    right: Vector3
    up: Vector3
    frame_time: float
    time: float
    intermission: int
    paused: int
    spectator: int
    on_ground: int
    water_level: int
    sim_vel: Vector3
    sim_org: Vector3
    view_height: Vector3
    ideal_pitch: float
    cl_viewangles: Rotation
    health: int
    crosshair_angle: Rotation
    view_size: float
    punch_angle: Rotation
    max_clients: int
    view_entity: int
    player_num: int
    max_entities: int
    demo_playback: int
    hardware: int
    smoothing: int
    ptr_cmd: int
    ptr_movevars: int
    viewport: Rect
    next_view: int
    only_client_draw: int

    def __str__(self):
        return 'RefParams(' \
               f'view_org: {self.view_org}, ' \
               f'view_angles: {self.view_angles}, ' \
               f'forward: {self.forward}, ' \
               f'right: {self.right}, ' \
               f'up: {self.up}, ' \
               f'frame_time: {self.frame_time}, ' \
               f'time: {self.time}, ' \
               f'intermission: {self.intermission}, ' \
               f'paused: {self.paused}, ' \
               f'spectator: {self.spectator}, ' \
               f'on_ground: {self.on_ground}, ' \
               f'water_level: {self.water_level}, ' \
               f'sim_vel: {self.sim_vel}, ' \
               f'sim_org: {self.sim_org}, ' \
               f'view_height: {self.view_height}, ' \
               f'ideal_pitch: {self.ideal_pitch}, ' \
               f'cl_viewangles: {self.cl_viewangles}, ' \
               f'health: {self.health}, ' \
               f'crosshair_angle: {self.crosshair_angle}, ' \
               f'view_size: {self.view_size}, ' \
               f'punch_angle: {self.punch_angle}, ' \
               f'max_clients: {self.max_clients}, ' \
               f'view_entity: {self.view_entity}, ' \
               f'player_num: {self.player_num}, ' \
               f'max_entities: {self.max_entities}, ' \
               f'demo_playback: {self.demo_playback}, ' \
               f'hardware: {self.hardware}, ' \
               f'smoothing: {self.smoothing}, ' \
               f'ptr_cmd: {self.ptr_cmd}, ' \
               f'ptr_movevars: {self.ptr_movevars}, ' \
               f'viewport: {self.viewport}, ' \
               f'next_view: {self.next_view}, ' \
               f'only_client_draw: {self.only_client_draw}' \
               ')'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        view_org = Vector3.from_stream(binary_stream)
        view_angles = Rotation.from_stream(binary_stream)
        forward = Vector3.from_stream(binary_stream)
        right = Vector3.from_stream(binary_stream)
        up = Vector3.from_stream(binary_stream)
        frame_time, time = unpack_le('ff', binary_stream.read(4 * 2))
        intermission, paused, spectator, on_ground, water_level = unpack_le('iiiii', binary_stream.read(4 * 5))
        sim_vel = Vector3.from_stream(binary_stream)
        sim_org = Vector3.from_stream(binary_stream)
        view_height = Vector3.from_stream(binary_stream)
        ideal_pitch, = unpack_le('f', binary_stream.read(4))
        cl_viewangles = Rotation.from_stream(binary_stream)
        health, = unpack_le('i', binary_stream.read(4))
        crosshair_angle = Rotation.from_stream(binary_stream)
        view_size, = unpack_le('f', binary_stream.read(4))
        punch_angle = Rotation.from_stream(binary_stream)
        max_clients, view_entity, player_num, max_entities, demo_playback, hardware, smoothing, ptr_cmd, ptr_movevars \
            = unpack_le('iiiiiiiii', binary_stream.read(4 * 9))
        viewport = Rect.from_stream(binary_stream)
        next_view, only_client_draw = unpack_le('ii', binary_stream.read(4 * 2))

        return RefParams(
            view_org,
            view_angles,
            forward,
            right,
            up,
            frame_time,
            time,
            intermission,
            paused,
            spectator,
            on_ground,
            water_level,
            sim_vel,
            sim_org,
            view_height,
            ideal_pitch,
            cl_viewangles,
            health,
            crosshair_angle,
            view_size,
            punch_angle,
            max_clients,
            view_entity,
            player_num,
            max_entities,
            demo_playback,
            hardware,
            smoothing,
            ptr_cmd,
            ptr_movevars,
            viewport,
            next_view,
            only_client_draw
        )


@dataclass
class UserCmd:
    lerp_msec: int
    msec: int
    view_angles: Rotation
    forward_move: float
    side_move: float
    up_move: float
    light_level: int
    buttons: int
    impulse: int
    weapon_select: int
    impact_index: int
    impact_position: Vector3

    def __str__(self):
        return 'UserCmd(' \
               f'lerp_msec: {self.lerp_msec}, ' \
               f'msec: {self.msec}, ' \
               f'view_angles: {self.view_angles}, ' \
               f'forward_move: {self.forward_move}, ' \
               f'side_move: {self.side_move}, ' \
               f'up_move: {self.up_move}, ' \
               f'light_level: {self.light_level}, ' \
               f'buttons: {self.buttons}, ' \
               f'impulse: {self.impulse}, ' \
               f'weapon_select: {self.weapon_select}, ' \
               f'impact_index: {self.impact_index}, ' \
               f'impact_position: {self.impact_position}, ' \
               ')'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        lerp_msec, = unpack_le('h', binary_stream.read(2))
        msec, = unpack_be('Bx', binary_stream.read(2))
        view_angles = Rotation.from_stream(binary_stream)
        forward_move, side_move, up_move = unpack_le('fff', binary_stream.read(4 * 3))
        light_level, = unpack_be('bx', binary_stream.read(2))
        buttons, = unpack_le('H', binary_stream.read(2))
        impulse, weapon_select = unpack_be('bbxx', binary_stream.read(4))
        impact_index, = unpack_le('i', binary_stream.read(4))
        impact_position = Vector3.from_stream(binary_stream)

        return UserCmd(
            lerp_msec,
            msec,
            view_angles,
            forward_move,
            side_move,
            up_move,
            light_level,
            buttons,
            impulse,
            weapon_select,
            impact_index,
            impact_position)


@dataclass
class MoveVars:
    gravity: float
    stop_speed: float
    max_speed: float
    spectator_max_speed: float
    accelerate: float
    air_accelerate: float
    water_accelerate: float
    friction: float
    edge_friction: float
    water_friction: float
    ent_gravity: float
    bounce: float
    step_size: float
    max_velocity: float
    z_max: float
    wave_height: float
    footsteps: float
    sky_name: str
    roll_angle: float
    roll_speed: float
    sky_color: Vector3
    sky_vec: Vector3

    def __str__(self):
        return 'MoveVars(' \
               f'gravity: {self.gravity}, ' \
               f'stop_speed: {self.stop_speed}, ' \
               f'max_speed: {self.max_speed}, ' \
               f'spectator_max_speed: {self.spectator_max_speed}, ' \
               f'accelerate: {self.accelerate}, ' \
               f'air_accelerate: {self.air_accelerate}, ' \
               f'water_accelerate: {self.water_accelerate}, ' \
               f'friction: {self.friction}, ' \
               f'edge_friction: {self.edge_friction}, ' \
               f'water_friction: {self.water_friction}, ' \
               f'ent_gravity: {self.ent_gravity}, ' \
               f'bounce: {self.bounce}, ' \
               f'step_size: {self.step_size}, ' \
               f'max_velocity: {self.max_velocity}, ' \
               f'z_max: {self.z_max}, ' \
               f'wave_height: {self.wave_height}, ' \
               f'footsteps: {self.footsteps}, ' \
               f'sky_name: {self.sky_name}, ' \
               f'roll_angle: {self.roll_angle}, ' \
               f'roll_speed: {self.roll_speed}, ' \
               f'sky_color: {self.sky_color}, ' \
               f'sky_vec: {self.sky_vec}, ' \
               ')'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        gravity, stop_speed, max_speed, spectator_max_speed, \
            accelerate, air_accelerate, water_accelerate, friction, \
            edge_friction, water_friction, ent_gravity, bounce, \
            step_size, max_velocity, z_max, wave_height, footsteps \
            = unpack_le('f' * 17, binary_stream.read(4 * 17))
        sky_name = read_binary_string(binary_stream, 32)
        roll_angle, roll_speed = unpack_le('ff', binary_stream.read(4 * 2))
        sky_color = Vector3.from_stream(binary_stream)
        sky_vec = Vector3.from_stream(binary_stream)

        return MoveVars(
            gravity,
            stop_speed,
            max_speed,
            spectator_max_speed,
            accelerate,
            air_accelerate,
            water_accelerate,
            friction,
            edge_friction,
            water_friction,
            ent_gravity,
            bounce,
            step_size,
            max_velocity,
            z_max,
            wave_height,
            footsteps,
            sky_name,
            roll_angle,
            roll_speed,
            sky_color,
            sky_vec)


@dataclass
class NetMsgInfo:
    timestamp: float
    ref_params: RefParams
    user_cmd: UserCmd
    move_vars: MoveVars
    view: Vector3
    view_model: int

    def __str__(self):
        return 'NetMsgInfo(' \
               f'timestamp: {self.timestamp}' \
               f'ref_params: {self.ref_params}, ' \
               f'user_cmd: {self.user_cmd}, ' \
               f'move_vars: {self.move_vars}, ' \
               f'view: {self.view}, ' \
               f'view_model: {self.view_model}' \
               ')'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        timestamp, = unpack_le('f', binary_stream.read(4))
        ref_params = RefParams.from_stream(binary_stream)
        user_cmd = UserCmd.from_stream(binary_stream)
        move_vars = MoveVars.from_stream(binary_stream)
        view = Vector3.from_stream(binary_stream)
        view_model, = unpack_le('i', binary_stream.read(4))
        return NetMsgInfo(timestamp, ref_params, user_cmd, move_vars, view, view_model)


@dataclass
class NetMsg:
    net_msg_info: NetMsgInfo
    incoming_sequence: int
    incoming_acknowledged: int
    incoming_reliable_acknowledged: int
    incoming_reliable_sequence: int
    outgoing_sequence: int
    reliable_sequence: int
    last_reliable_sequence: int
    msg_length: int
    msg: bytes

    def __str__(self):
        return 'NetMsg(' \
               f'net_msg_info: {self.net_msg_info}' \
               f'incoming_sequence: {self.incoming_sequence}, ' \
               f'incoming_acknowledged: {self.incoming_acknowledged}, ' \
               f'incoming_reliable_acknowledged: {self.incoming_reliable_acknowledged}, ' \
               f'incoming_reliable_sequence: {self.incoming_reliable_sequence}, ' \
               f'outgoing_sequence: {self.outgoing_sequence}, ' \
               f'reliable_sequence: {self.reliable_sequence}, ' \
               f'last_reliable_sequence: {self.last_reliable_sequence}, ' \
               f'msg_length: {self.msg_length}, ' \
               f'msg: {self.msg}' \
               ')'

    @staticmethod
    def from_stream(binary_stream: BytesIO):
        net_msg_info = NetMsgInfo.from_stream(binary_stream)
        incoming_sequence, incoming_acknowledged, incoming_reliable_acknowledged, incoming_reliable_sequence, \
            outgoing_sequence, reliable_sequence, last_reliable_sequence, msg_length \
            = unpack_le('iiiiiiii', binary_stream.read(4 * 8))

        if msg_length < NET_MESSAGE_LENGTH_MIN or msg_length > NET_MESSAGE_LENGTH_MAX:
            raise InvalidNetMsgLength(NET_MESSAGE_LENGTH_MIN, NET_MESSAGE_LENGTH_MAX + 1, msg_length)

        msg = binary_stream.read(msg_length)

        return NetMsg(net_msg_info,
                      incoming_sequence,
                      incoming_acknowledged,
                      incoming_reliable_acknowledged,
                      incoming_reliable_sequence,
                      outgoing_sequence,
                      reliable_sequence,
                      last_reliable_sequence,
                      msg_length,
                      msg)


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
