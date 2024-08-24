from dataclasses import dataclass
import typing

SelfSwitchFlags = typing.Literal['A', 'B', 'C', 'D']


@dataclass
class RPGAudioFile:
    name: str
    volume: int
    pitch: int
    
    

@dataclass
class Table:
    data: list[list[list[int]]]
    

@dataclass(frozen=True, slots=True)
class Tone:
    red: float
    green: float
    blue: float
    alpha_or_grey: float


@dataclass
class RPGEventPageGraphic:
    tile_id: int
    character_name: str
    character_hue: int
    direction: int
    pattern: int
    opacity: int
    blend_type: int
    

@dataclass
class RPGEventPageCondition:
    switch1_valid: bool
    switch1_id: int
    switch2_valid: bool
    switch2_id: int
    variable_valid: bool
    variable_id: int
    variable_value: int
    self_switch_valid: bool
    self_switch_ch: SelfSwitchFlags

@dataclass
class RPGMoveCommand:
    code: int
    parameters: list


@dataclass
class RPGMoveRoute:
    repeat: bool
    skippable: bool
    list: list[RPGMoveCommand]


@dataclass
class RPGEventCommand:
    code: int
    indent: int
    parameters: list


@dataclass
class RPGEventPage:
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
    
    
@dataclass
class RPGEvent:
    id: int
    name: str
    x: int
    y: int
    pages: list[RPGEventPage]


@dataclass
class RPGMap:
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


@dataclass
class RPGTileset:
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


@dataclass
class RPGCommonEvent:
    id: int
    name: str
    switch_id: int
    list: list[RPGEventCommand]
                                                 
                                                 
@dataclass
class RPGMapInfo:
    name: str
    parent_id: int
    order: int
    expanded: bool
    scroll_x: int
    scroll_y: int
                    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
RPGMAKER_CLASSES = {
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
    'RPG::CommonEvent': RPGCommonEvent,
    'RPG::MapInfo': RPGMapInfo,
}