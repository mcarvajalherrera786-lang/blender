import bpy, math
from mathutils import Vector

s = bpy.context.scene
s.frame_start = 1
s.frame_end = 96
s.render.fps = 24

# centro del coche
xs=[]; ys=[]; zs=[]
car_objs=[o for o in bpy.data.objects if o.name.startswith("Coche_")]
for o in car_objs:
    for c in o.bound_box:
        p=o.matrix_world @ Vector(c); xs.append(p.x); ys.append(p.y); zs.append(p.z)
cx=(min(xs)+max(xs))/2; cy=(min(ys)+max(ys))/2; cz=(min(zs)+max(zs))/2

root = bpy.data.objects.get("Coche_Root")
if root:
    bpy.data.objects.remove(root, do_unlink=True)
root = bpy.data.objects.new("Coche_Root", None)
root.empty_display_type='ARROWS'
root.location=(cx, cy, 0.0)
s.collection.objects.link(root)

for o in car_objs:
    if o.parent: continue
    o.parent = root
    o.matrix_parent_inverse = root.matrix_world.inverted()

# coche mirando hacia el garaje (+Y)
root.rotation_euler = (0, 0, math.pi)

# recorrido: fuera -> dentro del garaje
START_Y = -8.0
END_Y   = -1.0
root.location.y = START_Y
root.keyframe_insert("location", index=1, frame=1)
root.keyframe_insert("location", index=1, frame=12)
root.location.y = END_Y
root.keyframe_insert("location", index=1, frame=72)
root.keyframe_insert("location", index=1, frame=96)

# giro de ruedas
for o in car_objs:
    if o.name.startswith("Coche_Rueda") or o.name.startswith("Coche_Llanta"):
        o.rotation_euler = (0,0,0)
        o.keyframe_insert("rotation_euler", index=0, frame=12)
        o.rotation_euler = (-(END_Y-START_Y)/0.36, 0, 0)
        o.keyframe_insert("rotation_euler", index=0, frame=72)
        if o.animation_data and o.animation_data.action:
            for fc in o.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'

# camara de la animacion
cam = bpy.data.objects.get("Cam_Garage")
if not cam:
    cd = bpy.data.cameras.new("Cam_Garage")
    cam = bpy.data.objects.new("Cam_Garage", cd)
    s.collection.objects.link(cam)
cam.location = (1.2, -15.2, 4.3)
cam.data.lens = 35
d = Vector((7.2, -4.2, 1.35)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
s.camera = cam

s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")
print("ANIM OK root", tuple(round(v,2) for v in root.location), "coche", len(car_objs))
