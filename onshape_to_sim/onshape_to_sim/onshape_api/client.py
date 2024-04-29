"""
client
======

Convenience functions for working with the Onshape API
"""

import json
import os
import random
import requests
import string
import time
from pathlib import Path

from onshape_to_sim.onshape_api.onshape import Onshape
from onshape_to_sim.onshape_api.utils import (
    API,
    CommonAttributes,
    add_d_wvm_ids,
    add_d_wvm_e_ids,
    check_and_append_extension,
    join_api_url,
)

# TODO: remove dead code
def _create_obj_export_assem_body(
    obj_name: str,
    resolution: str,
    ang_tol: float = 0.1,
    dist_tol: float = 0.0001
    ) -> dict:
    """Creates the body for an assembly obj export request. 
    
    Args:
        assembly_name: name of the file to store the zipped files as
        resolution: the resolution of the resulting mesh
        ang_tol: maximum tolerance allowed in angular distance calculations (in degrees)
        dist_tol: maximum tolerance allowed in linear distance calculations (in meters)

    Returns:
        The body of the JSON request to grab the full OBJ assembly from Onshape
    """
    return {
        "resolution" : f"{resolution}",
        "storeInDocument" : "false", 
        "notifyUser" : "false", 
        "destinationName" : f"{obj_name}", 
        "includeExportIds" : "false", 
        "flattenAssemblies" : "false", 
        "ignoreExportRulesForContents" : "true", 
        "formatName" : "OBJ", 
        "grouping" : "true",
        "maximumChordLength": 10, # I have no idea what this actually does
        "angularTolerance": ang_tol,
        "distanceTolerance": dist_tol,
        "onePartPerDoc": "true",
        "joinAdjacentSurfaces": "false",
        "splitAssembliesIntoMultipleDocuments": "true",
    }


# TODO: remove dead code
def _create_stl_export_assem_body(
    stl_name: str,
    resolution: str,
    ang_tol: float = 0.1,
    dist_tol: float = 0.0001
    ) -> dict:
    """Creates the body for an assembly obj export request. 
    
    Args:
        assembly_name: name of the file to store the zipped files as
        resolution: the resolution of the resulting mesh
        ang_tol: maximum tolerance allowed in angular distance calculations (in degrees)
        dist_tol: maximum tolerance allowed in linear distance calculations (in meters)

    Returns:
        The body of the JSON request to grab the full OBJ assembly from Onshape
    """
    return {
        "resolution" : f"{resolution}",
        "storeInDocument" : "false", 
        "notifyUser" : "false", 
        "destinationName" : f"{stl_name}", 
        "includeExportIds" : "false", 
        "flattenAssemblies" : "false", 
        "ignoreExportRulesForContents" : "true", 
        "formatName" : "STL", 
        "grouping" : "true",
        "maximumChordLength": 10, # I have no idea what this actually does
        "angularTolerance": ang_tol,
        "distanceTolerance": dist_tol,
        "onePartPerDoc": "true",
        "joinAdjacentSurfaces": "false",
        "unit": "meters",
        "splitAssembliesIntoMultipleDocuments": "true",
    }


def escape_url(s):
    return s.replace('/', '%2f').replace('+', '%2b')


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

    def ping_async_export_call(self, tid: str, configuration: str = API.default, time_delay: float = 30.0) -> dict:
        """Waits for the export call to complete and returns its translation ID.

        Args:
            api_url: The URL where the API is being called
            time_delay: The amount of time we spend waiting

        Returns:
            The translation ID which can be used to download the .OBJ files

        Raises:
            AttributeError if API is not actively being translated or not done 
        """
        status_response = self.translation_status_request(tid=tid, configuration=configuration)
        while (request_state := status_response[API.request_state]) != API.done:
            if request_state != API.active:
                raise AttributeError(f"Request state terminated with state {request_state}")
            time.sleep(time_delay)
            status_response = self.translation_status_request(tid=tid, configuration=configuration)
        return status_response
    
    def download_document_external_data(
        self,
        did: str,
        fid: str,
        filename: str,
        file_extension: str,
        configuration: str = API.default
        ) -> dict:
        """Downloads the external data associated with the document.

        Most commonly used to get .objs and .stls stored in the document

        Args:
            did: document id
            fid: file ids associated with the external object
            filename: name of the file we want to store this as
            configuration: the configuration of the thing
        """
        json_request = join_api_url(
            API.documents,
            "d",
            did,
            API.external_data,
            fid
        )
        response = self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration}
        )
        filename = check_and_append_extension(filename, file_extension)
        with open(filename, "wb") as fi:
            fi.write(response.content)
        return response

    def part_export_stl(
        self,
        did: str,
        wvmid: str,
        eid: str,
        part_id: str,
        wvm: str = API.workspace,
        configuration: str = API.default
        ) -> requests.Response:
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
            "Accept": "application/octet-stream"
        }
        query = {"mode": "binary", "units": "meter", "configuration": configuration, "angleTolerance": 0.1}
        return self._api.request(API.get_request, json_request, headers=req_headers, query=query)

    def part_stl_pipeline(
        self,
        did: str,
        wvmid: str,
        eid: str,
        part_id: str,
        filename: str,
        file_extension: str = API.stl,
        wvm: str = API.workspace,
        resolution: str = API.coarse,
        configuration: str = API.default,
        ) -> None:
        resp = self.part_export_stl(
            did = did,
            wvm = wvm,
            wvmid = wvmid,
            eid = eid,
            part_id = part_id
        )
        filename = check_and_append_extension(filename, file_extension)
        with open(filename, "wb") as fi:
            fi.write(resp.content)

    def assembly_export_obj(
        self,
        did: str,
        wvmid: str,
        eid: str,
        filename: str,
        wvm: str = API.workspace,
        resolution: str = API.coarse,
        configuration: str = API.default,
        ) -> dict:
        """Exports an entire assembly into a concatenated OBJ file.

        TODO (@bhung): figure out a smarter way to only grab the parts and not the assemblies, then split them up

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
            filename: name of the file you want to save to .obj as
            resolution: resolution level of the mesh. Choose from API.coarse, API.medium, API.fine

        Returns:
            The Onshape response data with the translation ID, which is queried for the download link / status
        """
        json_request = join_api_url(
            add_d_wvm_e_ids(API.assemblies, did=did, wvm=wvm, wvmid=wvmid, eid=eid),
            API.translations
        )
        export_body = _create_obj_export_assem_body(
            obj_name=filename, resolution=resolution, 
        )
        return self._api.request(
            API.post_request,
            json_request,
            query={API.config: configuration},
            body=export_body
        ).json()

    def assembly_export_stl(
        self,
        did: str,
        wvmid: str,
        eid: str,
        filename: str,
        wvm: str = API.workspace,
        resolution: str = API.coarse,
        configuration: str = API.default,
        ) -> dict:
        """Exports an entire assembly into a concatenated OBJ file.

        TODO (@bhung): figure out a smarter way to only grab the parts and not the assemblies, then split them up

        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
            filename: name of the file you want to save to .obj as
            resolution: resolution level of the mesh. Choose from API.coarse, API.medium, API.fine

        Returns:
            The Onshape response data with the translation ID, which is queried for the download link / status
        """
        json_request = join_api_url(
            add_d_wvm_e_ids(API.assemblies, did=did, wvm=wvm, wvmid=wvmid, eid=eid),
            API.translations
        )
        export_body = _create_stl_export_assem_body(
            stl_name=filename, resolution=resolution, 
        )
        return self._api.request(
            API.post_request,
            json_request,
            query={API.config: configuration},
            body=export_body
        ).json()

    def assembly_stl_pipeline(
        self,
        did: str,
        wvmid: str,
        eid: str,
        meshname: str,
        filename: str,
        wvm: str = API.workspace,
        resolution: str = API.coarse,
        configuration: str = API.default,
        ) -> None:
        resp = self.assembly_export_stl(
            did = did,
            wvm = wvm,
            wvmid = wvmid,
            eid = eid,
            filename = meshname,
        )
        try:
            url = resp[API.translation_id]
            time.sleep(1.0)
            download_resp = self.ping_async_export_call(url)
            fid = download_resp[API.external_data_ids][0]
            resp = self.download_document_external_data(
                did = did,
                fid = fid,
                filename = filename,
                file_extension = API.stl,
            )
        except KeyError:
            print(f"API call failed; return response {url}")

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

    def element_metadata(
        self,
        did: str,
        wvmid: str,
        eid: str,
        configuration: str = API.default,
        wvm: str = API.microversion,
        ) -> dict:
        """Retrieves the metadata for a specific part in a document
                
        Args:
            did: document id 
            wvm: the type of document we want to draw from (workspace, version, or microversion)
            wvmid: workspace/version/microversion id
            eid: element id
        """
        json_request = add_d_wvm_e_ids(API.metadata, did=did, wvm=wvm, wvmid=wvmid, eid=eid)
        response = self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration, API.computed_properties: True, API.assembly_computed_properties: True}
            ).json()
        return response[CommonAttributes.properties]

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
        response = self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration, API.computed_properties: True}
            ).json()
        return response[CommonAttributes.properties]

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
        query = {
            API.config: configuration,
            API.mate_connectors: False,
            API.mate_features: True,
            API.exclude_suppressed: True,
            API.non_solids: True,
        }
        return self._api.request(
            API.get_request,
            json_request,
            query=query
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

    def translation_status_request(
        self,
        tid: str,
        configuration: str = API.default,
        ) -> dict:
        """Checks the status of a translation request
        
        Args:
            tid: translation id of the item being translated
        """
        json_request = join_api_url(
            API.translations,
            tid
        )
        return self._api.request(
            API.get_request,
            json_request,
            query={API.config: configuration}
            ).json()
