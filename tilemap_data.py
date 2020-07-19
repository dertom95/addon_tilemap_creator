import bpy

class TMC_DT_COLLECTION_WRAPPER(bpy.types.PropertyGroup):
    bl_idname = "TMC_DT_COLLECTION_WRAPPER"

    collection : bpy.props.PointerProperty(type=bpy.types.Collection)

cam_preset_items = [
    ("cam_iso", "ISO", "Isometric(?) view", 1),
    ("cam_top_down", "Top Down", "Top Down View", 2),
    ("cam_frontal45", "Blue", "FrontalView with 45° Rotation", 3)
]    
class TMC_DT_TILEMAP(bpy.types.PropertyGroup):
    name                : bpy.props.StringProperty()
    parent_collections  : bpy.props.CollectionProperty(type=TMC_DT_COLLECTION_WRAPPER)
    render_size         : bpy.props.IntVectorProperty(size=2,default=(128,128))
    cam_ortho_scale     : bpy.props.FloatProperty(name="Cam Ortho Scale",min=0,max=20,default=4)
    output_path         : bpy.props.StringProperty(subtype="DIR_PATH")
    cam_preset          : bpy.props.EnumProperty(name="View", items=cam_preset_items)
    recursive           : bpy.props.BoolProperty(description="Process all collection recursively, otherwise only direct children are rendered")

class TMC_DT_SCENE_Settings(bpy.types.PropertyGroup):
    tilemaps    : bpy.props.CollectionProperty(type=TMC_DT_TILEMAP)

    
