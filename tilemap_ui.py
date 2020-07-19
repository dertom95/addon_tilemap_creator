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
        row.label(text="manage tilemap 2")
        
        outer_box = layout.box()
        row = outer_box.row()

        for idx,tilemap in enumerate(settings.tilemaps):
            innerbox = outer_box.box()
            
            row = innerbox.row()
            row.prop(tilemap,"name")
            op = row.operator("tmc.manage_tilemaps",text="",icon="REMOVE")
            op.operation = TMC_Operations.TMC_OP_DELETE_TILEMAP
            op.idx = idx
            
            col_box = innerbox.box()
            for cidx,tcol in enumerate(tilemap.parent_collections):
                row = col_box.row()
                row.prop(tcol,"collection")
                # if tcol.collection:
                #     row.label(text="%s"%len(tcol.collection.children))
                op = row.operator("tmc.manage_tilemaps",text="",icon="REMOVE")
                op.operation = TMC_Operations.TMC_OP_REMOVE_ROOT_COLLECTION
                op.idx = idx
                op.cidx = cidx
            
            row = col_box.row()
            op = row.operator("tmc.manage_tilemaps",text="",icon="ADD")
            op.operation = TMC_Operations.TMC_OP_ADD_ROOT_COLLECTION
            op.idx = idx

            row = innerbox.row()
            row.prop(tilemap,"render_size")
            
            row = innerbox.row()
            row.prop(tilemap,"cam_delta_scale")

            row = innerbox.row()
            row.prop(tilemap,"output_path")

            row = innerbox.row()
            op = row.operator("tmc.manage_tilemaps",text="Render Single Tiles")
            op.operation = TMC_Operations.TMC_OP_REQUEST_RENDER
            op.idx = idx
            if not tilemap.output_path:
                row.enabled=False

            

        row = layout.row()
        op = row.operator("tmc.manage_tilemaps",text="create tilemap",icon="ADD")
        op.operation = TMC_Operations.TMC_OP_CREATE_TILEMAP


