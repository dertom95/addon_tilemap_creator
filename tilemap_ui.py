import bpy
from . tilemap_operators import TMC_Operations
from . tilemap_data import TMC_DT_SCENE_Settings

class TMC_PT_main(bpy.types.Panel):
    bl_idname = "TMC_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tilemap Creator"
    bl_label ="Tilemap Creator"
    

    #bl_options = {'DEFAULT_CLOSED'}
    
    # @classmethod
    # def poll(cls, context):
    #     return bpy.context.scene.render.engine=="CYCLES"   
    # 

    @classmethod
    def poll(cls, context):
        return True


    def draw(self, context):
        settings = bpy.context.scene.tmcSettings

        layout = self.layout

        row = layout.row()
        row.label(text="manage tilemap")
        
        row = layout.row()
        row.prop(settings,"select_collection")
        
        row = layout.row()
        op = row.operator("tmc.manage_tilemap")
        if settings.select_collection:
            op.operation = TMC_Operations.TMC_OP_CREATE_TILE
            op.col_name = settings.select_collection.name
        else:
            row.enabled = False

