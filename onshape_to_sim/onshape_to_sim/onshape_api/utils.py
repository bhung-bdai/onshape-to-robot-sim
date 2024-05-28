'''
utils
=====

Handy functions for API key sample app
'''
from typing import Optional
from dataclasses import dataclass, asdict
import logging
from logging.config import dictConfig
import os
import subprocess

import openmesh as om

__all__ = [
    'log'
]


@dataclass
class API:
    accept: str = "accept"
    active: str = "ACTIVE"
    assemblies: str = "assemblies"
    assembly_computed_properties: str = "includeComputedAssemblyProperties"
    coarse: str = "coarse"
    computed_properties: str = "includeComputedProperties"
    config: str = "configuration"
    default: str = "default"
    documents: str = "documents"
    done: str = "DONE"
    elements: str = "elements"
    exclude_suppressed: str = "excludeSuppressed"
    external_data: str = "externaldata"
    external_data_ids: str = "resultExternalDataIds"
    fine: str = "fine"
    gltf: str = "gltf"
    mass_properties: str = "massproperties"
    mass_override: str = "useMassPropertyOverrides"
    mate_connectors: str = "includeMateConnectors"
    mate_features: str = "includeMateFeatures"
    medium: str = "med"
    metadata: str = "metadata"
    metadata_part: str = "p"
    microversion: str = "m"
    non_solids: str = "includeNonSolids"
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
    properties: str = "properties"
    root: str = "root"
    transform: str = "transform"
    value: str = "value"
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


def get_relevant_metadata(metadata_list: list, relevant_metadata: set) -> dict:
    """Returns each entry in the relevant metadata set mapped to its value."""
    metadata_value_map = {}
    for metadata in metadata_list:
        if (name := metadata[CommonAttributes.name]) in relevant_metadata:
            metadata_value_map[name] = metadata[CommonAttributes.value]
    return metadata_value_map


def check_and_append_extension(filename: str, extension: str) -> str:
    """Checks if the file ends with an extension. If not,it appends the given"""
    if len(filename.split(".")) > 1:
        return filename
    return f"{filename}.{extension}"


def convert_stls_to_objs(
    stl_files: list,
    stl_dir: Optional[str] = None,
    save_dir: Optional[str] = None,
    path_to_onshape_api: Optional[str] = None,
    ) -> None:
    """Given a list of stl files, saves them as .objs with the same name

    Args:
        stl_files: the absolute paths to the stl files
        stl_dir: the directory where the stls are located
        save_dir: the directory we want to save the .obj files to
    """
    # TODO: Figure out how to fix this later with an absolute path
    stl_to_obj = "./stl2obj"
    if path_to_onshape_api is not None:
        stl_to_obj = os.path.join(path_to_onshape_api, stl_to_obj)
    # Create the stl save directory if it doesn't exist
    if stl_dir is not None and not os.path.isdir(stl_dir):
        os.mkdir(stl_dir)
    elif stl_dir is None:
        stl_dir = ""
    # Create the obj save directory if it doesn't exist
    if save_dir is not None and not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    elif save_dir is None:
        save_dir = ""
    
    for stl in stl_files:
        obj_filename = "".join(stl.split(".")[:-1])
        obj_path = os.path.join(save_dir, check_and_append_extension(obj_filename, API.obj))
        stl_path = os.path.join(stl_dir, check_and_append_extension(stl, API.stl))
        # subprocess.call(["ls"])
        print(obj_path)
        print(stl_path)
        subprocess.call([stl_to_obj, "--input", str(stl_path), "--output", str(obj_path)])


def join_api_url(*args: str) -> str:
    """Joins all of the strings provided in the arguments with (/) slashes"""
    api_url = args[0]
    for i, arg in enumerate(args):
        if i == 0:
            continue
        api_url = api_url + "/" + arg
    return api_url


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
