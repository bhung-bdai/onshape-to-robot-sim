
from dataclasses import dataclass, asdict

@dataclass
class JointTypeMap():
    invalid: int = 0
    ball: int = 1
    continuous: int = 2
    fixed: int = 3
    gearbox: int = 4
    prismatic: int = 5
    revolute: int = 6
    revolute2: int = 7
    screw: int = 9


@dataclass
class GeometryTypeMap():
    empty: int = 0
    box: int = 1
    cylinder: int = 2
    plane: int = 3
    sphere: int = 4
    mesh: int = 5
    height_map: int = 6
    capsule: int = 7
    ellipsoid: int = 8


_onshape_mate_type_to_gz_mate_type = {
    "REVOLUTE": JointTypeMap.revolute,
    "FASTENED": JointTypeMap.fixed,
    "SLIDER": JointTypeMap.prismatic,
    "BALL": JointTypeMap.ball,
}


def onshape_mate_to_gz_mate(onshape_mate_type: str) -> int:
    return _onshape_mate_type_to_gz_mate_type[onshape_mate_type]