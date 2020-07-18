import bpy
import traceback,sys
from . tilemap_data import TMC_DT_COLLECTION_WRAPPER


class TMC_Operations:
    TMC_OP_CREATE_TILE = "create_tile"

    TMC_CAM_PRESET_TOPDOWN = "cam_top_down"    # top down
    TMC_CAM_PRESET_FRONTAL45 = "cam_frontal45" # looking diagonal frontal on tile
    TMC_CAM_PRESET_ISO = "cam_iso"             # iso. (is this iso?)

class TMC_OT_Manage_tilemaps(bpy.types.Operator):
    """"""

    bl_idname = "tmc.manage_tilemap"
    bl_label = "Tilemap Operation"

    operation       : bpy.props.StringProperty()
    scene_name      : bpy.props.StringProperty()
    col_name        : bpy.props.StringProperty()
    render_width    : bpy.props.IntProperty(default=512)
    render_height   : bpy.props.IntProperty(default=512)
    output_folder   : bpy.props.StringProperty()
    cam_preset      : bpy.props.StringProperty(default=TMC_Operations.TMC_CAM_PRESET_ISO)
    remove_scene    : bpy.props.BoolProperty(default=False)

    def set_camera_preset(self,cam,preset):
        if preset == TMC_Operations.TMC_CAM_PRESET_FRONTAL45:
            cam.location = (0.0, -20.0, 20.0)
            cam.rotation_euler = (0.7853981852531433, -0.0, 0.0)
        #TopDown
        elif preset == TMC_Operations.TMC_CAM_PRESET_TOPDOWN:
            cam.location = (0.0, -20.0, 28.18587303161621)
            cam.rotation_euler = (0,0,0)
        #iso?
        elif preset == TMC_Operations.TMC_CAM_PRESET_ISO:
            cam.location = (-20.0, -20.0, 28.18587303161621)
            cam.rotation_euler = (0.7853981852531433, -0.0, -0.7853981852531433)
        else:
            print("ERROR: Tilemap Operation: Unknown camera-presetion %s! Using iso-preset!" % self.cam_preset)       
            set_camera_preset(TMC_Operations.TMC_CAM_PRESET_ISO)


    def setup_scene(self, context):
        sname = "__tilemap_scene" if not self.scene_name else self.scene_name
        tilemap_scene = bpy.data.scenes.new(sname)
        bpy.context.window.scene = tilemap_scene
        
        # create camera
        cam = bpy.data.cameras.new("__tilemap_cam")
        cam.type="ORTHO"
        camnode = bpy.data.objects.new("__timemap_camnode",cam)
        self.set_camera_preset(camnode,self.cam_preset)

        tilemap_scene.camera = camnode

        tilemap_scene.collection.objects.link(camnode)
        # create light
        light = bpy.data.lights.new("__tilemap_light","SUN")
        lightnode = bpy.data.objects.new("__tilemape_lightnode",light)
        tilemap_scene.collection.objects.link(lightnode)   
        return tilemap_scene     

    def execute(self, context):
        #settings = bpy.context.scene.tmcSettings

        if self.operation == TMC_Operations.TMC_OP_CREATE_TILE:
            before_scene = bpy.context.scene
            
            try:
                scene = None
                if self.scene_name and self.scene_name in bpy.data.scenes:
                    scene = bpy.data.scenes[self.scene_name]
                    bpy.context.window.scene = scene
                    if "tile" in bpy.data.objects:
                        bpy.data.objects.remove(bpy.data.objects["tile"]) # remove old tile
                else:                    
                    scene = self.setup_scene(context)

                bpy.context.scene.render.resolution_x = self.render_width
                bpy.context.scene.render.resolution_y = self.render_height

                bpy.ops.object.collection_instance_add(collection=self.col_name, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                bpy.context.active_object.name = "tile"

                bpy.ops.render.render()
                render_image = bpy.data.images["Render Result"]
                filepath = "%s/%s_%s/%s.png" % (self.output_folder,self.render_width,self.render_height,self.col_name)
                render_image.save_render(filepath)
                if self.remove_scene:
                    bpy.data.scenes.remove(scene)

            except Exception:
                print("ERROR: Tilemap Operation [%s]: scene_name:%s col_name:%s width:%s height:%s" % ( TMC_Operations.TMC_OP_CREATE_TILE,self.scene_name,self.col_name,self.render_width,self.render_height ))
                traceback.print_exc()

            # finally:
            #     bpy.context.window.scene = before_scene
                
        else:
            print("ERROR: Tilemap Operation: Unknown operation %s" % self.operation)                        


        return{'FINISHED'}

