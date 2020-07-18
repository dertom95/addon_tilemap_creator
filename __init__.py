
import sys,math,traceback

bl_info = {
    "name": "dertom-gametools: Tilemap Creator",
    "description": "Tool to automatically create tiles and tilemaps",
    "author": "Thomas Trocha",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" 
}

if "bpy" in locals():
    import importlib
    if "tilemap_data" in locals():
        importlib.reload(tilemap_data)
    if "tilemap_operators" in locals():
        importlib.reload(tilemap_operators)
    if "tilemap_ui" in locals():
        importlib.reload(tilemap_ui)        
    
import bpy
from . tilemap_data import TMC_DT_SCENE_Settings,TMC_DT_COLLECTION_WRAPPER,TMC_DT_TILEMAP
from . tilemap_operators import TMC_OT_CRUD_tilemaps,TMC_OT_Render_tiles
from . tilemap_ui import TMC_PT_main

# classes to be (un)registered. definied in its specific files
classes =  (
    # data
    TMC_DT_COLLECTION_WRAPPER,
    TMC_DT_TILEMAP,
    TMC_DT_SCENE_Settings,
    # operators
    TMC_OT_CRUD_tilemaps,TMC_OT_Render_tiles,
    # ui
    TMC_PT_main
)

defRegister, defUnregister = bpy.utils.register_classes_factory(classes)

def register():
    try:
        defRegister()
        bpy.types.Scene.tmcSettings = bpy.props.PointerProperty(type=TMC_DT_SCENE_Settings)
    except Exception:
        traceback.print_exc()

def unregister():
    try:
        defUnregister()
        del bpy.types.Scene.tmcSettings
    except Exception:
        traceback.print_exc()

