from typing import Any, Optional
import math
import os
import uuid

import numpy as np
import numpy.typing as npt

from xml.sax.saxutils import escape

from gz.math7 import (
    Color,
    Inertiald,
    MassMatrix3d,
    Pose3d,
    Vector3d,
)
from onshape_to_sim.onshape_api.client import (
    Client,
)
from onshape_to_sim.onshape_api.onshape_tree import (
    OnshapeTreeNode,
)
from onshape_to_sim.onshape_api.utils import (
    APIAttributes,
    CommonAttributes,
    ElementAttributes,
    FeatureAttributes,
    MassAttributes,
    OccurrenceAttributes,
    PartAttributes
)
from onshape_to_sim.sdf.element_data import (
    GeometryTypeMap,
    JointTypeMap,
    onshape_mate_to_gz_mate,
)
from sdformat13 import (
    Collision,
    Frame,
    Geometry,
    GeometryType,
    Joint,
    JointAxis,
    JointType,
    Link,
    Material,
    Mesh,
    Model,
    Root,
    Visual,
)


def xml_escape(unescaped: str) -> str:
    """Escapes XML characters in a string so that it can be safely added to an XML file
    """
    return escape(unescaped, entities={
        "'": "&apos;",
        "\"": "&quot;"
    })

def rotationMatrixToEulerAngles(R: npt.ArrayLike):
    """Converts a rotation matrix to its Euler angle parameterization.

    Args:
        R: an input rotation matrix
    
    Returns:
        The equivalent (x, y, z) Euler angles
    """
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


def make_color_gz(color_arr: npt.ArrayLike) -> Color:
    """Makes a Gazebo color object from an array"""
    return Color(color_arr[0], color_arr[1], color_arr[2], color_arr[3]) 


def make_inertia_gz(mass: float, inertia_matrix: np.ndarray) -> MassMatrix3d:
    """Creates a Gazebo inertial matrix based on its numpy equivalent.

    Args:
        inertial_matrix: (3, 3) inertial matrix 

    Returns:
        The Gazebo object representing the inertial matrix in world coordinates.
    """
    J = MassMatrix3d()
    J.set_mass(mass)
    J.set_ixx(inertia_matrix[0, 0])
    J.set_ixy(inertia_matrix[0, 1])
    J.set_ixz(inertia_matrix[0, 2])
    J.set_iyy(inertia_matrix[1, 1])
    J.set_iyz(inertia_matrix[1, 2])
    J.set_izz(inertia_matrix[2, 2])
    return J


def make_inertial_gz(mass: float, inertia_matrix: npt.ArrayLike, pose: npt.ArrayLike = np.zeros((6,))) -> Inertiald:
    """Creates an inertial object from the inertial values"""
    inertial = Inertiald()
    # Set the inertia
    inertia_object = make_inertia_gz(mass, inertia_matrix)
    inertial.set_mass_matrix(inertia_object)
    # Set the pose
    pose_object = make_pose_gz(pose[:3], pose[3:])
    inertial.set_pose(pose_object)
    return inertial


def make_pose_gz(xyz: npt.ArrayLike, rpy: npt.ArrayLike) -> Pose3d:
    """Creates a pose representing the center of mass frame with respect to the parent element's frame.
    
    Args:
        xyz: (x, y, z) point in world frame
        rpy: (roll, pitch, yaw) Euler angles with respect to world frame

    Returns:
        A Gazebo pose object representing the pose of the object.
    """
    return Pose3d(
        xyz[0],
        xyz[1],
        xyz[2],
        rpy[0],
        rpy[1],
        rpy[2]
    )


def make_collision_object(collision_name: str, mesh_uri: str, pose: npt.ArrayLike = np.zeros((6,))) -> Collision:
    """Creates a collision object from a mesh shape centered at a pose relative to the parent element."""
    collision = Collision()
    geometry = make_geometry_object(mesh_uri)
    collision.set_name(collision_name)
    collision.set_geometry(geometry)
    # print(collision.geometry().mesh_shape().uri())
    collision_pose = make_pose_gz(pose[:3], pose[3:])
    collision.set_raw_pose(collision_pose)
    return collision


def make_frame_object(frame_name: str) -> Frame:
    """Creates a frame object with a given name."""
    frame = Frame()
    frame.set_name(frame_name)
    return frame


# def make_joint_object(joint_name, parent: str, child: str, joint_type: int = JointType.revolute) -> Joint:
#     """Creates an SDF joint object based on the node data"""


def make_geometry_object(mesh_uri: str, geometry_type: int = GeometryTypeMap.mesh) -> Geometry:
    """Creates an SDF geometry object with a mesh"""
    geometry = Geometry()
    geometry.set_type(GeometryType(geometry_type))
    mesh = Mesh()
    mesh.set_uri(mesh_uri)
    geometry.set_mesh_shape(mesh)
    return geometry


def make_material_object(
    ambient: npt.ArrayLike = np.array([0.1, 0.1, 0.1, 1]),
    diffuse: npt.ArrayLike = np.array([0.1, 0.1, 0.1, 1]),
    specular: npt.ArrayLike = np.array([0.1, 0.1, 0.1, 1]),
    emissive: npt.ArrayLike = np.zeros((4,))
    ) -> Material:
    """Sets the materials required for each of these"""
    material = Material()
    material.set_ambient(make_color_gz(ambient))
    material.set_diffuse(make_color_gz(diffuse))
    material.set_specular(make_color_gz(specular))
    material.set_emissive(make_color_gz(emissive))
    return material


def make_visual_object(
    visual_name: str,
    mesh_uri: str,
    pose: npt.ArrayLike = np.zeros((6,)),
    ) -> Visual:
    """Creates a visual object from a mesh shape and a material ambience."""
    visual = Visual()
    geometry = make_geometry_object(mesh_uri)
    visual.set_name(visual_name)
    visual.set_geometry(geometry)
    visual_pose = make_pose_gz(pose[:3], pose[3:])
    visual.set_raw_pose(visual_pose)
    return visual


def mesh_filepath(robot_name: str, mesh_name: str, mesh_directory: str) -> str:
    return f"file://{mesh_directory}/{robot_name}/{mesh_name}.obj"


class RobotSDF():

    world_frame: str = "world_frame"

    def __init__(self, onshape_root: OnshapeTreeNode, mesh_directory: str):
        self.robot_name = onshape_root.name
        self.sdf_root = Root()
        self.mesh_directory = mesh_directory
        model = Model()
        model.set_name(self.robot_name)
        model.add_frame(make_frame_object(self.world_frame))
        self.sdf_root.set_model(model)
        self._build_sdf(onshape_root)

    def add_joints(self, joint_info: list, occurrence_id_to_node: dict, parent_link: str) -> None:
        """Takes in a node which has a joint with children.""" 
        # TODO: figure out how to set the name of the joints
        # Loops through all the joints in the parent and creates a joint
        for joint in joint_info:
            for child in joint[FeatureAttributes.children]:
                joint_sdf = Joint()
                child_node = occurrence_id_to_node[child]
                gz_mate_type = onshape_mate_to_gz_mate(joint[FeatureAttributes.mateType])
                joint_sdf.set_type(JointType(gz_mate_type))
                # Set the joint to be linked to the parent and the child links
                joint_sdf.set_parent_name(parent_link)
                joint_sdf.set_child_name(child_node.simplified_name)
                # Add the pose of the joint
                # The transform is given wrt to the world (I think) so we extract/set pose
                joint_transform = joint[FeatureAttributes.transform]
                joint_pose_gz = make_pose_gz(
                    joint_transform[:3, 3],
                    rotationMatrixToEulerAngles(joint_transform[:3, :3])
                )
                joint_sdf.set_raw_pose(joint_pose_gz)
                joint_sdf.set_name(joint[CommonAttributes.name])
                # TODO implement the rest of the joints types later
                match gz_mate_type:
                    case JointTypeMap.revolute | JointTypeMap.prismatic:
                        # Revolute joints currently only support turning about the Z-axis: see 
                        # https://cad.onshape.com/help/Content/mate-revolute.htm?cshid=mate_revolute
                        # https://cad.onshape.com/help/Content/mate-slider.htm?Highlight=slider%20mate
                        joint_axis = JointAxis()
                        # print(gz_mate_type)
                        joint_axis.set_xyz(Vector3d(0, 0, 1))
                        joint_sdf.set_axis(0, joint_axis)
                        # TODO: include stiffness, damping, dynamics, etc
                        # TODO: include gearing and gearbox ratios
                        # TODO: include the position velocity and effort limits
                        # Both of the above need to be added in metadata I think. 
                        pass
                    case JointTypeMap.fixed:
                        pass
                self.sdf_root.model().add_joint(joint_sdf)

    def add_link(self, node: OnshapeTreeNode) -> None:
        """Adds a link if a node specifies that it should be a link."""
        link_sdf = Link()
        # A node name is not guaranteed to be unique, so we need to keep tally
        link_sdf.set_name(node.simplified_name)
        # Create the pose wrt the world frame and set it to the link
        world_r_link = node.world_tform_element[:3, :3]
        rpy = rotationMatrixToEulerAngles(world_r_link)
        com_in_world_gz = make_pose_gz(node.com_wrt_world, rpy)

        # This is going to be 0 with respect to the world frame. You kind of have 2 options:
        # You can either set the pose wrt the center of mass. This requires a reorienting everything properly
        # Or you can set it wrt to the world, which is what Onshape gives. This means your frames are kind of all over,
        # but it's a bit easier to deal with

        # Create the inertial element
        inertia_in_world_gz = make_inertial_gz(node.mass, node.inertia_wrt_world, np.hstack((node.com_wrt_world, rpy)))
        link_sdf.set_inertial(inertia_in_world_gz)
        mesh_uri = mesh_filepath(self.robot_name, node.mesh_name, self.mesh_directory)
        # TODO: Drake appears to fail with the collision object for some reason?
        # collision_sdf = make_collision_object(
        #     node.simplified_name + "_collision",
        #     mesh_uri
        # )
        # collision_sdf.set_raw_pose(com_in_world_gz)
        # link_sdf.add_collision(collision_sdf)
        # TODO: get all of the colors and make the visuals
        material_sdf = self.get_material(node)
        visual_sdf = make_visual_object(
            node.simplified_name + "_visual",
            mesh_uri,
        )
        # TODO figure out why the visual is not correctly set
        visual_pose_in_world_gz = make_pose_gz(
            node.world_tform_element[:3, 3],
            rotationMatrixToEulerAngles(node.world_tform_element[:3, :3])
        )
        visual_sdf.set_raw_pose(visual_pose_in_world_gz)
        # visual_sdf.set_raw_pose(com_in_world_gz)
        # TODO!!! The pose isn't being calculated properly. 
        visual_sdf.set_material(material_sdf)
        link_sdf.add_visual(visual_sdf)

        # TODO!!! Open3d stl not working, need to get .objs
        
        # Add the link to the the model
        self.sdf_root.model().add_link(link_sdf)
        # Add a frame associated with the link
        frame_sdf = Frame()
        frame_sdf.set_name(node.simplified_name + "_frame")
        frame_sdf.set_attached_to(link_sdf.name())
        frame_sdf.set_raw_pose(com_in_world_gz)
        self.sdf_root.model().add_frame(frame_sdf)

    def get_material(self, node: OnshapeTreeNode) -> Material:
        """TODO: Get the actual material properties based on the colors and shit"""
        return make_material_object()

    def _build_sdf(self, onshape_root: OnshapeTreeNode) -> None:
        # TODO: substitute it with the links instead of the parts.
        for part in onshape_root.parts:
            self.add_link(part)
        for joint_parent, joint_info in onshape_root.parent_nodes.items():
            self.add_joints(joint_info, onshape_root.occurrence_id_to_node, joint_parent)
        
    def write_sdf(self, sdf_filepath: Optional[str] = None):
        """Writes the sdf as a string"""
        if sdf_filepath is None:
            sdf_filepath = self.robot_name
        if not sdf_filepath.endswith(".sdf"):
            sdf_filepath += ".sdf"
        with open(sdf_filepath, "w") as fi:
            fi.write(self.sdf_root.to_string())

    # def addFixedJoint(self, parent, child, matrix, name=None):
    #     if name is None:
    #         name = parent + '_' + child + '_fixing'

    #     self.append('<joint name="' + name + '" type="fixed">')
    #     self.append(pose(matrix))
    #     self.append('<parent>'+parent+'</parent>')
    #     self.append('<child>'+child+'</child>')
    #     self.append('</joint>')
    #     self.append('')

    # def addDummyLink(self, name, visualMatrix=None, visualSTL=None, visualColor=None):
    #     self.append('<link name="'+name+'">')
    #     self.append('<pose>0 0 0 0 0 0</pose>')
    #     self.append('<inertial>')
    #     self.append('<pose>0 0 0 0 0 0</pose>')
    #     self.append('<mass>1e-9</mass>')
    #     self.append('<inertia>')
    #     self.append(
    #         '<ixx>0</ixx><ixy>0</ixy><ixz>0</ixz><iyy>0</iyy><iyz>0</iyz><izz>0</izz>')
    #     self.append('</inertia>')
    #     self.append('</inertial>')
    #     if visualSTL is not None:
    #         self.addSTL(visualMatrix, visualSTL, visualColor,
    #                     name+"_visual", "visual")
    #     self.append('</link>')

    # def endLink(self):
    #     mass, com, inertia = self.linkDynamics()

    #     for node in ['visual', 'collision']:
    #         if self._mesh[node] is not None:
    #             color = self._color / self._color_mass
    #             filename = self._link_name+'_'+node+'.stl'
    #             stl_combine.save_mesh(
    #                 self._mesh[node], self.meshDir+'/'+filename)
    #             if self.shouldSimplifySTLs(node):
    #                 stl_combine.simplify_stl(
    #                     self.meshDir+'/'+filename, self.maxSTLSize)
    #             self.addSTL(np.identity(4), filename, color, self._link_name, 'visual')

    #     self.append('<inertial>')
    #     self.append('<pose frame="'+self._link_name +
    #                 '_frame">%.20g %.20g %.20g 0 0 0</pose>' % (com[0], com[1], com[2]))
    #     self.append('<mass>%.20g</mass>' % mass)
    #     self.append('<inertia><ixx>%.20g</ixx><ixy>%.20g</ixy><ixz>%.20g</ixz><iyy>%.20g</iyy><iyz>%.20g</iyz><izz>%.20g</izz></inertia>' %
    #                 (inertia[0, 0], inertia[0, 1], inertiabecause you're rightthat we [0, 2], inertia[1, 1], inertia[1, 2], inertia[2, 2]))
    #     self.append('</inertial>')

    #     if self.useFixedLinks:
    #         self.append(
    #             '<visual><geometry><box><size>0 0 0</size></box></geometry></visual>')

    #     self.append('</link>')
    #     self.append('')

    #     if self.useFixedLinks:
    #         n = 0
    #         for visual in self._visuals:
    #             n += 1
    #             visual_name = '%s_%d' % (self._link_name, n)
    #             self.addDummyLink(visual_name, visual[0], visual[1], visual[2])
    #             self.addJoint('fixed', self._link_name, visual_name,
    #                           np.eye(4), visual_name+'_fixing', None)

    # def addFrame(self, name, matrix):
    #     # Adding a dummy link
    #     self.addDummyLink(name)

    #     # Linking it with last link with a fixed link
    #     self.addFixedJoint(self._link_name, name, matrix, name+'_frame')

    # def addMaterial(
    #     self,
    #     color: npt.ArrayLike
    #     ) -> Element:
    #     rgba_color = np.array([color[0], color[1], color[2], 1])
    #     specular_color = np.array([0.1, 0.1, 0.1, 1])
    #     return material(
    #         rgba_color,
    #         rgba_color,
    #         specular_color,
    #         np.zeros(4,)
    #     )

    # def addSTL(self, matrix, stl, color, name, node='visual'):
    #     self.append('<'+node+' name="'+name+'_visual">')
    #     self.append(pose(matrix))
    #     self.append('<geometry>')
    #     self.append('<mesh><uri>file://'+stl+'</uri></mesh>')
    #     self.append('</geometry>')
    #     if node == 'visual':
    #         self.append(self.material(color))
    #     self.append('</'+node+'>')

    # def addPart(self, matrix, stl, mass, com, inertia, color, shapes=None, name=''):
    #     name = self._link_name+'_'+str(self._link_childs)+'_'+name
    #     self._link_childs += 1

    #     # self.append('<link name="'+name+'">')
    #     # self.append(pose(matrix))

    #     if stl is not None:
    #         if not self.drawCollisions:
    #             if self.useFixedLinks:
    #                 self._visuals.append(
    #                     [matrix, self.packageName + os.path.basename(stl), color])
    #             elif self.shouldMergeSTLs('visual'):
    #                 self.mergeSTL(stl, matrix, color, mass)
    #             else:
    #                 self.addSTL(matrix, os.path.basename(
    #                     stl), color, name, 'visual')

    #         entries = ['collision']
    #         if self.drawCollisions:
    #             entries.append('visual')
    #         for entry in entries:
    #             if shapes is None:
    #                 # We don't have pure shape, we use the mesh
    #                 if self.shouldMergeSTLs(entry):
    #                     self.mergeSTL(stl, matrix, color, mass, entry)
    #                 else:
    #                     self.addSTL(matrix, stl, color, name, entry)
    #             else:
    #                 # Inserting pure shapes in the URDF model
    #                 k = 0
    #                 self.append('<!-- Shapes for '+name+' -->')
    #                 for shape in shapes:
    #                     k += 1
    #                     self.append('<'+entry+' name="'+name +
    #                                 '_'+entry+'_'+str(k)+'">')
    #                     self.append(pose(matrix*shape['transform']))
    #                     self.append('<geometry>')
    #                     if shape['type'] == 'cube':
    #                         self.append('<box><size>%.20g %.20g %.20g</size></box>' %
    #                                     tuple(shape['parameters']))
    #                     if shape['type'] == 'cylinder':
    #                         self.append(
    #                             '<cylinder><length>%.20g</length><radius>%.20g</radius></cylinder>' % tuple(shape['parameters']))
    #                     if shape['type'] == 'sphere':
    #                         self.append(
    #                             '<sphere><radius>%.20g</radius></sphere>' % shape['parameters'])
    #                     self.append('</geometry>')

    #                     if entry == 'visual':
    #                         self.append(self.material(color))
    #                     self.append('</'+entry+'>')

    #     self.addLinkDynamics(matrix, mass, com, inertia)

    # def addJoint(self, jointType, linkFrom, linkTo, transform, name, jointLimits, zAxis=[0, 0, 1]):
    #     self.append('<joint name="'+name+'" type="'+jointType+'">')
    #     self.append(pose(transform))
    #     self.append('<parent>'+linkFrom+'</parent>')
    #     self.append('<child>'+linkTo+'</child>')
    #     self.append('<axis>')
    #     self.append('<xyz>%.20g %.20g %.20g</xyz>' % tuple(zAxis))
    #     lowerUpperLimits = ''
    #     if jointLimits is not None:
    #         lowerUpperLimits = '<lower>%.20g</lower><upper>%.20g</upper>' % jointLimits
    #     self.append('<limit><effort>%.20g</effort><velocity>%.20g</velocity>%s</limit>' %
    #                 (self.jointMaxEffortFor(name), self.jointMaxVelocityFor(name), lowerUpperLimits))
    #     self.append('</axis>')
    #     self.append('</joint>')
    #     self.append('')

    @property
    def model(self):
        return self.root.model()