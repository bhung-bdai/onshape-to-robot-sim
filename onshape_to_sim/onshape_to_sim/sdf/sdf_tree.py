
import sdformat13 as sdf

from onshape_api.onshape_tree import OnshapeTreeNode

def onshape_tree_to_sdf(root: OnshapeTreeNode):
    # Depth first search
    # Each part should be a link in the system
    # Each link will be connected by parts through joints
