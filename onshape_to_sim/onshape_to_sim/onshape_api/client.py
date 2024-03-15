"""
client
======

Convenience functions for working with the Onshape API
"""

import mimetypes
import random
import requests
import string
import os
import json
import hashlib
from pathlib import Path

from onshape_to_sim.onshape_api.onshape import Onshape
from onshape_to_sim.onshape_api.utils import (
    API,
    add_d_wvm_ids,
    add_d_wvm_e_ids,
)


def escape_url(s):
    return s.replace('/', '%2f').replace('+', '%2b')


def join_api_url(*args: str) -> str:
    """Joins all of the strings provided in the arguments with (/) slashes"""
    api_url = args[0]
    for i, arg in enumerate(args):
        if i == 0:
            continue
        api_url = api_url + "/" + arg
    return api_url


class Client():
    """
    Defines methods for testing the Onshape API. Comes with several methods:

    - Create a document
    - Delete a document
    - Get a list of documents

    Attributes:
        - stack (str, default='https://cad.onshape.com'): Base URL
        - logging (bool, default=True): Turn logging on or off
    """

    def __init__(self, stack='https://cad.onshape.com', logging=True, creds='./config.json'):
        """
        Instantiates a new Onshape client.

        Args:
            stack: Base URL used to access the API
            logging: Turn logging on or off
            creds: Location of the config.json file holding the credentials
        """
        self._stack = stack
        self._api = Onshape(stack=stack, logging=logging, creds=creds)
        self.useCollisionsConfigurations = True

    def rename_document(self, did, name):
        """
        Renames the specified document.

        Args:
            - did (str): Document ID
            - name (str): New document name

        Returns:
            - requests.Response: Onshape response data
        """

        payload = {
            'name': name
        }

        return self._api.request('post', 'documents/' + did, body=payload)

    def del_document(self, did):
        """
        Delete the specified document.

        Args:
            - did (str): Document ID

        Returns:
            - requests.Response: Onshape response data
        """

        return self._api.request('delete', 'documents/' + did)

    def get_document(self, did: str):
        """
        Get details for a specified document.

        Args:
            did: Document ID

        Returns:
            Document information retrieved by the document id
        """
        json_request = join_api_url(
            API.documents,
            did
        )
        return self._api.request(API.get_request, json_request).json()

    def list_documents(self):
        """
        Get list of documents for current user.

        Returns:
            - requests.Response: Onshape response data
        """
        json_request = API.documents
        return self._api.request(API.get_request, json_request).json()

    def part_export_stl(self, did: str, wvmid: str, eid: str, part_id: str, wvm: str = "w") -> requests.Response:
        """
        Exports STL export from a part studio

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
            part_id: the id of the part

        Returns:
            Onshape response data with the STL exported inside the request.content
        """
        json_request = join_api_url(
            add_d_wvm_e_ids(API.parts, did=did, wvm=wvm, wvmid=wvmid, eid=eid),
            API.part_id,
            part_id,
            API.stl
        )
        req_headers = {
            "Accept": "*/*"
        }
        return self._api.request(API.get_request, json_request, headers=req_headers)

    def all_elements_in_document(
        self,
        did: str,
        wvmid: str,
        wvm: str = API.workspace
        ) -> dict:
        """Get the list of elements in a given document.
        
        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
        """
        json_request = add_d_wvm_ids(API.documents, did=did, wvm=wvm, wvmid=wvmid)
        return self._api.request(
            API.get_request,
            json_request,
            ).json()

    def all_parts_in_document(
        self,
        did: str,
        wvmid: str,
        configuration: str = API.default,
        wvm: str = API.microversion,
        ) -> dict:
        """Returns all parts inside a document.

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
        """
        json_request = add_d_wvm_ids(API.parts, did=did, wvm=wvm, wvmid=wvmid)
        return self._api.request(
            API.get_request,
            json_request,
            query={API.get_request: configuration}
            ).json()

    def all_parts_in_element(
        self,
        did: str,
        wvmid: str,
        eid: str,
        configuration: str = API.default,
        wvm: str = API.microversion,
        ) -> dict:
        """Retrieves all parts in the document.

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
        """
        json_request = add_d_wvm_e_ids(API.parts, did=did, wvm=wvm, wvmid=wvmid, eid=eid)
        return self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration}
            ).json()

    def all_part_metadata(
        self,
        did: str,
        wvmid: str,
        eid: str,
        configuration: str = API.default,
        wvm: str = API.microversion,
        ) -> dict:
        """Retrieves the metadata for all parts in the document.

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
        """
        json_request = join_api_url(
            add_d_wvm_e_ids(API.metadata, did=did, wvm=wvm, wvmid=wvmid, eid=eid),
            API.metadata_part
        )
        return self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration, API.computed_properties: True}
            ).json()

    def part_metadata(
        self,
        did: str,
        wvmid: str,
        eid: str, 
        partid: str, 
        configuration: str = API.default,
        wvm: str = API.microversion,
        ) -> dict:
        """Retrieves the metadata for a specific part in a document
                
        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
            partid: the id of the part
        """
        json_request = join_api_url(
            add_d_wvm_e_ids(API.metadata, did=did, wvm=wvm, wvmid=wvmid, eid=eid),
            API.metadata_part,
            escape_url(partid)
        )
        return self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration, API.computed_properties: True}
            ).json()

    def part_mass_properties(
        self, 
        did: str, 
        wvmid: str,
        eid: str, 
        partid: str,
        configuration: str = API.default,
        wvm: str = API.microversion,
        ) -> dict:
        """Retrieves the mass properties of a part.

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
            partid: the id of the part
        """
        json_request = join_api_url(
            add_d_wvm_e_ids(API.parts, did=did, wvm=wvm, wvmid=wvmid, eid=eid),
            API.part_id,
            escape_url(partid),
            API.mass_properties
        )
        return self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration, API.mass_override: True}
            ).json()

    def assembly_definition(
        self,
        did: str,
        wvmid: str,
        eid: str,
        configuration: str = API.default,
        wvm: str = API.workspace,
        ) -> dict:
        """Retrieves the definition of an assembly.

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
            """
        json_request = add_d_wvm_e_ids(API.assemblies, did=did, wvm=wvm, wvmid=wvmid, eid=eid)
        return self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration, API.mate_connectors: True, API.mate_features: True}
            ).json()

    def assembly_mass_properties(
        self,
        did: str,
        wvmid: str,
        eid: str,
        configuration: str = API.default,
        wvm: str = API.microversion,
        ) -> dict:
        """Retrieves the mass properties of an assembly.

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
        """
        json_request = join_api_url(
            add_d_wvm_e_ids(API.assemblies, did=did, wvm=wvm, wvmid=wvmid, eid=eid),
            API.mass_properties
        )
        return self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration}
            ).json()
