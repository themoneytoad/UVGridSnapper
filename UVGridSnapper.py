import bpy
from mathutils import Vector
import bmesh
    
def MoveUVs(img, tile, row, column, rot):
    num_images = img/tile       # numbe of images in a column / row
    uv_unit = 1.0/num_images    # the UV grid based on tile image size
    padding = 0.0002

    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    uv_layer = bm.loops.layers.uv.verify()
    for face in bm.faces:
        #print(face)
        if face.select:
            order = [0,1,2,3]
            if rot == 90 or rot == -270:
                order = [1,2,3,0]
            elif rot == 180 or rot == -180:
                order = [2,3,0,1]
            elif rot == 270 or rot == -90:
                order = [3,0,1,2]
            face.loops[order[0]][uv_layer].uv = Vector(((column - 1)*uv_unit + padding, ((num_images-(row-1))-1)*uv_unit + padding))
            face.loops[order[1]][uv_layer].uv = Vector(((column)*uv_unit - padding, ((num_images-(row-1))-1)*uv_unit + padding))
            face.loops[order[2]][uv_layer].uv = Vector(((column)*uv_unit - padding, (num_images-(row-1))*uv_unit - padding))
            face.loops[order[3]][uv_layer].uv = Vector(((column - 1)*uv_unit + padding, (num_images-(row-1))*uv_unit - padding))
        bmesh.update_edit_mesh(bpy.context.active_object.data)
    
    
class UVGridSnappingUI(bpy.types.Panel):
    bl_label = "UVGrid Snapper"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "UVGrid Snapper"
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        col = layout.column()
        col.prop(obj, "iimg")
        col = layout.column()
        col.prop(obj, "ttile")
        col = layout.column()
        col.prop(obj, "rrows")
        col = layout.column()
        col.prop(obj, "ccols")
        col = layout.column()
        col.prop(obj, "rrots", expand=False)
        op = col.operator("uv.grid_snapper", text="Apply")
        op.img_in = obj.iimg
        op.tile_in = obj.ttile
        op.row_in = obj.rrows
        op.col_in = obj.ccols
        op.rot_in = obj.rrots
        
class UVGridSnapper(bpy.types.Operator):
    bl_idname = "uv.grid_snapper"
    bl_label = "UV Grid Snapper"
    bl_options = {'REGISTER', 'UNDO'}
    
    img_in = bpy.props.IntProperty(min=1, default=2048)
    tile_in = bpy.props.IntProperty(min=1, default=32)
    row_in = bpy.props.IntProperty(min=1, default=1)
    col_in = bpy.props.IntProperty(min=1, default=1)
    rot_in = bpy.props.EnumProperty(
        items=(
            ('0', "0", ""),
            ('90', "90", ""),
            ('180', "180", ""),
            ('270', "270", "")
        ),
        default='0'
    )
    
    def execute(self, context):
        print(self.rot_in)
        MoveUVs(self.img_in, self.tile_in, self.row_in, self.col_in, int(self.rot_in))
        return {"FINISHED"}
        

def find_cursor_location():
    # Look through area and find the first image editor
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            return area.spaces.active.cursor_location
    return None

#obj = bpy.context.object
#cursor = find_cursor_location()

#uv_unit = 0.015625 # 32 pixels in UV space
# 64 x 64 num images
# (64 - 1) * uv_unit => 
# xl = ( column - 1 ) * uv_unit, xr = (column) * uv_unit
# yt = (64 - (row - 1)) * uv_unit, yb = ((64 - (row - 1)) - 1) * uv_unit
# num (1) -> 64 - (num - 1) = 64
# num (3) -> 64 - (num - 1) = 62
#row = 1
#column = 2
#rot = 0

#if cursor:
#    
#    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
#    uv_layer = bm.loops.layers.uv.verify()
#    print('new')
#    for face in bm.faces:
#        #print(face)
#        if face.select:
#            order = [0,1,2,3]
#            if rot == 90 or rot == -270:
#                order = [1,2,3,0]
#            elif rot == 180 or rot == -180:
#                order = [2,3,0,1]
#            elif rot == 270 or rot == -90:
#                order = [3,0,1,2]
#            face.loops[order[0]][uv_layer].uv = Vector(((column - 1)*uv_unit, ((64-(row-1))-1)*uv_unit))
#            face.loops[order[1]][uv_layer].uv = Vector(((column)*uv_unit, ((64-(row-1))-1)*uv_unit))
#            face.loops[order[2]][uv_layer].uv = Vector(((column)*uv_unit, (64-(row-1))*uv_unit))
#            face.loops[order[3]][uv_layer].uv = Vector(((column - 1)*uv_unit, (64-(row-1))*uv_unit))
#        bmesh.update_edit_mesh(bpy.context.active_object.data)
#    
       
def register():
    bpy.utils.register_class(UVGridSnapper)
    bpy.utils.register_class(UVGridSnappingUI)
    bpy.types.Object.iimg = bpy.props.IntProperty(name="Image Size", default=2048, min=1)
    bpy.types.Object.ttile = bpy.props.IntProperty(name="Tile Size", default=32, min=1)
    bpy.types.Object.rrows = bpy.props.IntProperty(name="Row", default=1, min=1)
    bpy.types.Object.ccols = bpy.props.IntProperty(name="Column", default=1, min=1)
    bpy.types.Object.rrots = bpy.props.EnumProperty(name="Rotation",
        items=(
            ('0', "0", ""),
            ('90', "90", ""),
            ('180', "180", ""),
            ('270', "270", "")
        ),
        default='0'
    )

    
def unregister():
    bpy.utils.unregister_class(UVGridSnapper)
    bpy.utils.unregister_class(UVGridSnappingUI)
    del bpy.types.Object.iimg
    del bpy.types.Object.ttile
    del bpy.types.Object.rrows
    del bpy.types.Object.ccols
    del bpy.types.Object.rrots
    
if __name__ == "__main__":
    register()
