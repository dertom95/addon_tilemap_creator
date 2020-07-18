import bpy

class TMC_DT_COLLECTION_WRAPPER(bpy.types.PropertyGroup):
    bl_idname = "TMC_DT_COLLECTION_WRAPPER"

    collection : bpy.props.PointerProperty(type=bpy.types.Collection)
class TMC_DT_TILEMAP(bpy.types.PropertyGroup):
    name                : bpy.props.StringProperty()
    parent_collections  : bpy.props.CollectionProperty(type=TMC_DT_COLLECTION_WRAPPER)
    render_size         : bpy.props.IntVectorProperty(size=2,default=(128,128))
    delta_size          : bpy.props.FloatProperty(min=-10,max=10)
    output_path         : bpy.props.StringProperty(subtype="DIR_PATH")

class TMC_DT_SCENE_Settings(bpy.types.PropertyGroup):
    tilemaps    : bpy.props.CollectionProperty(type=TMC_DT_TILEMAP)

    
