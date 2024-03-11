'''
utils
=====

Handy functions for API key sample app
'''

from dataclasses import dataclass, asdict
import logging
from logging.config import dictConfig

__all__ = [
    'log'
]


@dataclass
class ElementAttributes:
    part: str = "Part"
    assembly: str = "Assembly"


@dataclass
class API:
    assemblies: str = "assemblies"
    computed_properties: str = "includeComputedProperties"
    config: str = "configuration"
    default: str = "default"
    documents: str = "documents"
    elements: str = "elements"
    mass_properties: str = "massproperties"
    mate_connectors: str = "includeMateConnectors"
    mate_features: str = "includeMateFeatures"
    metadata: str = "metadata"
    microversion: str = "m"
    part_id: str = "partid"
    parts: str = "parts"
    mass_override: str = "useMassPropertyOverrides"
    metadata_part: str = "p"
    version: str = "v"
    workspace: str = "w"
    get_request: str = "get"


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
