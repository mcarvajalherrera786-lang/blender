import bpy, math
from mathutils import Vector

s = bpy.context.scene

def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

# Camara trasera (casa del arbol)
cam = bpy.data.objects.get("Cam_Back")
if not cam:
    cd = bpy.data.cameras.new("Cam_Back")
    cam = bpy.data.objects.new("Cam_Back", cd)
    s.collection.objects.link(cam)
cam.location = (12.8, 16.5, 6.4)
cam.data.lens = 32
look_at(cam, (-4.4, 6.8, 2.7))

def render(camobj, path, freestyle=True):
    s.camera = camobj
    s.render.use_freestyle = freestyle
    s.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("RENDER", path)

render(bpy.data.objects["Cam"], r"D:\Users\Asus\Desktop\BLENDER\simpsons_house_exterior.png", True)
render(cam, r"D:\Users\Asus\Desktop\BLENDER\simpsons_house_treehouse.png", True)
render(bpy.data.objects["Cam_Salon"], r"D:\Users\Asus\Desktop\BLENDER\simpsons_house_salon.png", False)

bpy.ops.wm.save_as_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")
print("SAVED", len(bpy.data.objects))
