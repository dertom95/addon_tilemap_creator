import bpy

class TMC_DT_SCENE_Settings(bpy.types.PropertyGroup):
    select_collection : bpy.props.PointerProperty(type=bpy.types.Collection)

class TMC_DT_COLLECTION_WRAPPER(bpy.types.PropertyGroup):
    collection : bpy.props.PointerProperty(type=bpy.types.Collection)