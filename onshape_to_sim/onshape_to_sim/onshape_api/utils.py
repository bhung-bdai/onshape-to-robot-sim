'''
utils
=====

Handy functions for API key sample app
'''

from dataclasses import dataclass, asdict
import logging
from logging.config import dictConfig
import os

import openmesh as om

__all__ = [
    'log'
]


@dataclass
class API:
    accept: str = "accept"
    active: str = "ACTIVE"
    assemblies: str = "assemblies"
    coarse: str = "coarse"
    computed_properties: str = "includeComputedProperties"
    config: str = "configuration"
    default: str = "default"
    documents: str = "documents"
    done: str = "DONE"
    elements: str = "elements"
    external_data: str = "externaldata"
    fine: str = "fine"
    mass_properties: str = "massproperties"
    mass_override: str = "useMassPropertyOverrides"
    mate_connectors: str = "includeMateConnectors"
    mate_features: str = "includeMateFeatures"
    medium: str = "med"
    metadata: str = "metadata"
    metadata_part: str = "p"
    microversion: str = "m"
    obj: str = "obj"
    part_id: str = "partid"
    parts: str = "parts"
    partstudios: str = "partstudios"
    request_state: str = "requestState"
    stl: str = "stl"
    translations: str = "translations"
    translation_id: str = "id"
    version: str = "v"
    workspace: str = "w"
    get_request: str = "get"
    post_request: str = "post"


@dataclass
class APIAttributes():
    features: str = "features"
    instances: str = "instances"
    occurrences: str = "occurrences"
    rootAssembly: str = "rootAssembly"
    subassemblies: str = "subAssemblies"


@dataclass
class CommonAttributes:
    name: str = "name"
    suppressed: str = "suppressed"
    idNum: str = "id"
    isStandardContent: str = "isStandardContent"
    fullConfiguration: str = "fullConfiguration"
    documentVersion: str = "documentVersion"
    configuration: str = "configuration"
    documentId: str = "documentId"
    elementId: str = "elementId"
    elementType: str = "type"
    documentMicroversion: str = "documentMicroversion"
    root: str = "root"
    transform: str = "transform"
    version: str = "documentVersion"
    workspace: str = "documentWorkspace"


@dataclass
class ElementAttributes:
    part: str = "Part"
    assembly: str = "Assembly"


@dataclass
class FeatureAttributes():
    children: str = "children"
    is_parent: str = "is_parent"
    featureData: str = "featureData"
    mateType: str = "mateType"
    matedEntities: str = "matedEntities"
    matedOccurrence: str = "matedOccurrence"
    matedCS: str = "matedCS"
    origin: str = "origin"
    parent: str = "parent"
    transform: str = "transform"
    xAxis: str = "xAxis"
    yAxis: str = "yAxis"
    zAxis: str = "zAxis"


@dataclass
class MassAttributes():
    bodies: str = "bodies"
    centroid: str = "centroid"
    hasMass: str = "hasMass"
    inertia: str = "inertia"
    mass: str = "mass"
    volume: str = "volume"

@dataclass
class OccurrenceAttributes():
    path: str = "path"
    hidden: str = "hidden"


@dataclass
class PartAttributes():
    partId: str = "partId"
    bodyType: str = "bodyType"

def add_d_wvm_ids(api_request: str, did: str, wvm: str, wvmid: str) -> str:
    """Wraps an API call with the document and workspace/version/microversion ids

    Args:
        api_request: beginning of the api request
        did: document id 
        wvm: the type of document we want to draw from (workspace, version, or microversion)
        wvmid: workspace/version/microversion id
    Returns:
        The properly formatted api request and calls.
    """
    return api_request + "/d/" + did + "/" + wvm + "/" + wvmid

def add_d_wvm_e_ids(api_request: str, did: str, wvm: str, wvmid: str, eid: str) -> str:
    """Wraps an API call with the document, workspace/version/microversion, and element ids

    Args:
        api_request: beginning of the api request
        did: document id 
        wvm: the type of document we want to draw from (workspace, version, or microversion)
        wvmid: workspace/version/microversion id
        eid: element id
    Returns:
        The properly formatted api request and calls.
    """
    request = add_d_wvm_ids(api_request, did, wvm, wvmid)
    return request + "/e/" + eid


def wrap_in_quotes(string_to_wrap: str) -> str:
    """Wraps a string in quotation marks to make it acceptable by JSON."""
    return f"\"{string_to_wrap}\""


def convert_stls_to_objs(stl_files: list, stl_dir: str = "", save_dir: str = "") -> None:
    """Given a list of stl files, saves them as .objs with the same name

    Args:
        stl_files: the absolute paths to the stl files
        stl_dir: the directory where the stls are located
        save_dir: the directory we want to save the .obj files to
    """
    for stl in stl_files:
        stl_mesh = om.read_trimesh(os.path.join(stl_dir, stl))
        obj_filename = stl.split(".")[0]
        obj_path = os.path.join(save_dir, obj_filename + ".obj")
        om.write_mesh(obj_path, stl_mesh)


def log(msg, level=0):
    '''
    Logs a message to the console, with optional level paramater

    Args:
        - msg (str): message to send to console
        - level (int): log level; 0 for info, 1 for error (default = 0)
    '''

    red = '\033[91m'
    endc = '\033[0m'

    # configure the logging module
    cfg = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'stdout': {
                'format': '[%(levelname)s]: %(asctime)s - %(message)s',
                'datefmt': '%x %X'
            },
            'stderr': {
                'format': red + '[%(levelname)s]: %(asctime)s - %(message)s' + endc,
                'datefmt': '%x %X'
            }
        },
        'handlers': {
            'stdout': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'stdout'
            },
            'stderr': {
                'class': 'logging.StreamHandler',
                'level': 'ERROR',
                'formatter': 'stderr'
            }
        },
        'loggers': {
            'info': {
                'handlers': ['stdout'],
                'level': 'INFO',
                'propagate': True
            },
            'error': {
                'handlers': ['stderr'],
                'level': 'ERROR',
                'propagate': False
            }
        }
    }

    dictConfig(cfg)

    lg = 'info' if level == 0 else 'error'
    lvl = 20 if level == 0 else 40

    logger = logging.getLogger(lg)
    logger.log(lvl, msg)
