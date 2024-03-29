import bpy,os
import traceback,sys


class TMC_Operations:
    TMC_OP_CREATE_TILEMAP = "create_tilemap"
    TMC_OP_DELETE_TILEMAP = "delete_tilemap"
    TMC_OP_ADD_ROOT_COLLECTION = "add_collection"
    TMC_OP_REMOVE_ROOT_COLLECTION = "remove_collection"
    TMC_OP_REQUEST_RENDER = "request_render"

    TMC_CAM_PRESET_TOPDOWN = "cam_top_down"    # top down
    TMC_CAM_PRESET_FRONTAL45 = "cam_frontal45" # looking diagonal frontal on tile
    TMC_CAM_PRESET_ISO = "cam_iso"             # iso. (is this iso?)

def parent_collection_to_csv_children(parent_collection,collection_names="",recursive=False):
    for child in parent_collection.children:
        if child:
            collection_names = child.name if collection_names=="" else "%s,%s"%(collection_names,child.name)
            if recursive and len(child.children)>0:
                collection_names = parent_collection_to_csv_children(child,collection_names,True)
    return collection_names


class TMC_OT_CRUD_tilemaps(bpy.types.Operator):
    """ CRUD Tilemap """

    bl_idname = "tmc.manage_tilemaps"
    bl_label = "Tilemap Operation"

    operation : bpy.props.StringProperty() 
    idx       : bpy.props.IntProperty()
    cidx      : bpy.props.IntProperty()

    def execute(self, context):
        settings = bpy.context.scene.tmcSettings

        if self.operation==TMC_Operations.TMC_OP_CREATE_TILEMAP:
            settings.tilemaps.add()

        elif self.operation==TMC_Operations.TMC_OP_DELETE_TILEMAP:
            settings.tilemaps.remove(self.idx) 

        elif self.operation==TMC_Operations.TMC_OP_ADD_ROOT_COLLECTION:
            tilemap = settings.tilemaps[self.idx]
            tilemap.parent_collections.add()

        elif self.operation==TMC_Operations.TMC_OP_REMOVE_ROOT_COLLECTION:
            tilemap = settings.tilemaps[self.idx]
            tilemap.parent_collections.remove(self.cidx)

        elif self.operation==TMC_Operations.TMC_OP_REQUEST_RENDER:
            tilemap = settings.tilemaps[self.idx]

            collection_names=""
            for parent_collection in tilemap.parent_collections:
                if parent_collection.collection:
                    collection_names = parent_collection_to_csv_children(parent_collection.collection,collection_names,tilemap.recursive)

            print("collection_name:%s" % collection_names)
            bpy.ops.tmc.render_tiles(scene_name="tilemap_scene"
                                        ,col_names=collection_names
                                        ,output_folder=tilemap.output_path
                                        ,render_width=tilemap.render_size[0]
                                        ,render_height=tilemap.render_size[1]
                                        ,cam_ortho_scale=tilemap.cam_ortho_scale
                                        ,remove_scene=True)

        return{'FINISHED'}      


class TMC_OT_Render_tiles(bpy.types.Operator):
    """ Render Tilemap """

    bl_idname = "tmc.render_tiles"
    bl_label = "Tilemap Operation"

    scene_name      : bpy.props.StringProperty()
    col_names       : bpy.props.StringProperty()
    render_width    : bpy.props.IntProperty(default=512)
    render_height   : bpy.props.IntProperty(default=512)
    output_folder   : bpy.props.StringProperty()
    cam_preset      : bpy.props.StringProperty(default=TMC_Operations.TMC_CAM_PRESET_ISO)
    remove_scene    : bpy.props.BoolProperty(default=True)
    cam_ortho_scale : bpy.props.FloatProperty(default=5.0)
    rotation        : bpy.props.FloatVectorProperty(size=3)
    save_filenames  : bpy.props.StringProperty(default="output_files.txt")
    save_filename_postfix : bpy.props.StringProperty(default="")
    save_filenames_append : bpy.props.BoolProperty()

    def set_camera_preset(self,cam,preset):
        if preset == TMC_Operations.TMC_CAM_PRESET_FRONTAL45:
            cam.location = (0.0, -20.0, 20.0)
            cam.rotation_euler = (0.7853981852531433, -0.0, 0.0)
        #TopDown
        elif preset == TMC_Operations.TMC_CAM_PRESET_TOPDOWN:
            cam.location = (0.0, 0, 28.18587303161621)
            cam.rotation_euler = (0,0,0)
        #iso?
        elif preset == TMC_Operations.TMC_CAM_PRESET_ISO:
            cam.location = (-18.0, -18.0, 30)
            cam.rotation_euler = (0.7853981852531433, -0.0, -0.7853981852531433)
        else:
            print("ERROR: Tilemap Operation: Unknown camera-presetion %s! Using iso-preset!" % self.cam_preset)       
            self.set_camera_preset(TMC_Operations.TMC_CAM_PRESET_ISO)


    def setup_scene(self, context):
        sname = "__tilemap_scene" if not self.scene_name else self.scene_name
        tilemap_scene = bpy.data.scenes.new(sname)
        bpy.context.window.scene = tilemap_scene
        
        # create camera
        cam = bpy.data.cameras.new("__tilemap_cam")
        cam.type="ORTHO"
        cam.ortho_scale = self.cam_ortho_scale

        camnode = bpy.data.objects.new("__timemap_camnode",cam)
        self.set_camera_preset(camnode,self.cam_preset)

        tilemap_scene.camera = camnode

        tilemap_scene.collection.objects.link(camnode)
        # create light
        light = bpy.data.lights.new("__tilemap_light","SUN")
        light.energy=5
        light.specular_factor=0.01
        lightnode = bpy.data.objects.new("__tilemape_lightnode",light)
        #lightnode.rotation_euler=(0.6503279805183411, 0.055217113345861435, 1.8663908243179321)
        lightnode.rotation_euler=camnode.rotation_euler
        tilemap_scene.collection.objects.link(lightnode)   
        return tilemap_scene     

    def execute(self, context):
        self.new_file_data=""
        #settings = bpy.context.scene.tmcSettings

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
            bpy.context.scene.render.film_transparent = True

            print("COLNAMES INPUT:%s" %self.col_names)

            colnames = self.col_names.split(",")

            abs_path = bpy.path.abspath(self.output_folder)

            dir_name = os.path.dirname(abs_path)
            try:
                os.makedirs(dir_name)
            except:
                pass


            for col_name in colnames:
                print("Process:%s" % col_name)

                col_name = col_name.strip() 
                if col_name not in bpy.data.collections:
                    print("Unknown collection:%s" % col_name)
                    continue

                bpy.ops.object.collection_instance_add(collection=col_name, align='WORLD', location=(0, 0, 0), rotation=self.rotation, scale=(1, 1, 1))
                current_tile = bpy.context.active_object

                bpy.ops.render.render()
                render_image = bpy.data.images["Render Result"]
                
#                filepath = "%s/%s_%s_%s.png" % (abs_path,self.render_width,self.render_height,col_name)
                filepath = "%s/%s%s.png" % (abs_path,col_name,self.save_filename_postfix)
                render_image.save_render(filepath)
                print("Thumbnail wrote to :%s" %filepath)
                self.new_file_data+="%s\n" % filepath
                bpy.data.objects.remove(current_tile) # remove old tile

            if self.remove_scene:
                bpy.data.scenes.remove(scene)

            if self.save_filenames!="":
                if self.save_filenames_append:
                    text_file = open("%s/%s" % (abs_path,self.save_filenames) , "a")
                else:
                    text_file = open("%s/%s" % (abs_path,self.save_filenames) , "w")

                n = text_file.write(self.new_file_data)
                text_file.close()

        except Exception:
            print("ERROR: Tilemap Operation [%s]: scene_name:%s col_name:%s width:%s height:%s" % ( "Render Tilemap",self.scene_name,self.col_name,self.render_width,self.render_height ))
            traceback.print_exc()

        # finally:
        #     bpy.context.window.scene = before_scene
                


        return{'FINISHED'}



## TODO: Can we use this and create an operator out of it
def rearrange_objects(col_size=15,distance=2.0):
    current_x=0
    current_y=0
    for obj in bpy.data.objects:
        if obj.type!="MESH":
            continue
        
        obj.location = (current_x,current_y,0)
        for col in obj.users_collection:
            col.instance_offset = obj.location
        
        current_x += distance
        
        if current_x >= col_size * distance:
            current_x = 0
            current_y += distance

def rearrange_collections(col_size=15,distance=2.0):
    current_x=0
    current_y=0
    
    for col in bpy.data.collections:
        master_loc = col.instance_offset
        for obj in col.objects:
            if obj.type!="MESH":
                continue

            delta = master_loc - obj.location
            obj.location = (current_x-delta[0],current_y-delta[1],0)
                
        col.instance_offset=(current_x,current_y,0)
        
        current_x += distance
        if current_x >= col_size * distance:
            current_x = 0
            current_y += distance
    
    
#rearrange_collections()      
