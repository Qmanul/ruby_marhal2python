from __future__ import annotations

import abc
from dataclasses import dataclass
import struct
import typing

SelfSwitchFlags = typing.Literal['A', 'B', 'C', 'D']


@dataclass(slots=True)
class RubyObject(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def load(cls, data) -> RubyObject:
        pass
    

@dataclass(slots=True)
class RPGObject(RubyObject):
    @classmethod
    def load(cls, data: dict[str, object]) -> RPGObject:
        return cls(**{k.removeprefix('@'): v for k, v in data.items()})

    
@dataclass(slots=True)
class Table(RubyObject):
    data: list[list[list[int]]]
    
    @classmethod
    def load(cls, data: bytes) -> 'Table':
        zsize, xsize, ysize, zsize, size = struct.unpack('<5L', data[:20])
    
        if zsize * xsize * ysize != size:
            raise ValueError(f'Unexpected size {zsize * xsize * ysize} != {size}')
        
        # не правильный результат т.к. байты идут от младшего к старшему (кому не похуй)
        dataview = memoryview(data[20:]).cast("H", (zsize, ysize, xsize))  # type: ignore
        return cls(dataview.tolist())
    

@dataclass(slots=True)
class Tone(RubyObject):
    red: float
    green: float
    blue: float
    alpha_or_grey: float
    
    @classmethod
    def load(cls, data: bytes) -> 'Tone':
        return cls(*(struct.unpack('<4d', data)))


@dataclass(slots=True)
class RPGAudioFile(RPGObject):
    name: str
    volume: int
    pitch: int
    
    
@dataclass(slots=True)
class RPGEventPageGraphic(RPGObject):
    tile_id: int
    character_name: str
    character_hue: int
    direction: int
    pattern: int
    opacity: int
    blend_type: int
    

@dataclass(slots=True)
class RPGEventPageCondition(RPGObject):
    switch1_valid: bool
    switch1_id: int
    switch2_valid: bool
    switch2_id: int
    variable_valid: bool
    variable_id: int
    variable_value: int
    self_switch_valid: bool
    self_switch_ch: SelfSwitchFlags


@dataclass(slots=True)
class RPGMoveCommand(RPGObject):
    code: int
    parameters: list


@dataclass(slots=True)
class RPGMoveRoute(RPGObject):
    repeat: bool
    skippable: bool
    list: list[RPGMoveCommand]


@dataclass(slots=True)
class RPGEventCommand(RPGObject):
    code: int
    indent: int
    parameters: list


@dataclass(slots=True)
class RPGEventPage(RPGObject):
    condition: RPGEventPageCondition
    graphic: RPGEventPageGraphic
    move_type: int
    move_speed: int
    move_frequency: int
    move_route: RPGMoveRoute
    walk_anime: bool
    step_anime: bool
    direction_fix: bool
    through: bool
    always_on_top: bool
    trigger: int
    list: list[RPGEventCommand]
    
    
@dataclass(slots=True)
class RPGEvent(RPGObject):
    id: int
    name: str
    x: int
    y: int
    pages: list[RPGEventPage]


@dataclass(slots=True)
class RPGMap(RPGObject):
    autoplay_bgm: bool
    autoplay_bgs: bool
    bgm: RPGAudioFile
    bgs: RPGAudioFile
    data: Table
    encounter_list: list
    encounter_step: int
    events: dict[int, RPGEvent]
    height: int
    tileset_id: int
    width:int


@dataclass(slots=True)
class RPGTileset(RPGObject):
    id: int
    name: str
    tileset_name: str
    autotile_names: list[str]
    panorama_name: str
    panorama_hue: int
    fog_name: str
    fog_hue: int
    fog_opacity: int
    fog_blend_type: int
    fog_zoom: int
    fog_sx: int
    fog_sy: int
    battleback_name: str
    passages: Table
    priorities: Table
    terrain_tags: Table


@dataclass(slots=True)
class RPGCommonEvent(RPGObject):
    id: int
    name: str
    switch_id: int
    list: list[RPGEventCommand]
                                                 
                                                 
@dataclass(slots=True)
class RPGMapInfo(RPGObject):
    name: str
    parent_id: int
    order: int
    expanded: bool
    scroll_x: int
    scroll_y: int
                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
RPGMAKER_CLASSES: dict[str, RPGObject] = {
    'RPG::Map': RPGMap,
    'RPG::Event': RPGEvent,
    'RPG::Event::Page': RPGEventPage,
    'RPG::Event::Page::Graphic': RPGEventPageGraphic,
    'RPG::Event::Page::Condition': RPGEventPageCondition,
    'RPG::EventCommand': RPGEventCommand,
    'RPG::MoveRoute': RPGMoveRoute,
    'RPG::MoveCommand': RPGMoveCommand,
    'RPG::AudioFile': RPGAudioFile,
    'RPG::Tileset': RPGTileset,
    'RPG::MapInfo': RPGMapInfo,
    'RPG::CommonEvent': RPGCommonEvent,
}

RPGMAKER_USER_DEFINED: dict[str, RubyObject] = {
    'Tone': Tone,
    'Table': Table,
}