import bpy
src = r"D:\Users\Asus\Desktop\BLENDER\src_model\source\casa nouuu.blend"
bpy.ops.wm.open_mainfile(filepath=src)
print("SRC OPENED", len(bpy.data.objects))
for o in bpy.data.objects:
    mats = [m.name if m else None for m in o.data.materials] if o.type in ('MESH','CURVE') else []
    print("OBJ %s %s loc %s dims %s mats %s" % (o.name, o.type, tuple(round(v,2) for v in o.location), tuple(round(v,2) for v in o.dimensions), mats))
bpy.ops.wm.open_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")
print("BACK TO HOUSE")
