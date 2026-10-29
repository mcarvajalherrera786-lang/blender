import bpy, os
src = r"D:\Users\Asus\Desktop\BLENDER\src_model\source\casa nouuu.blend"
bpy.ops.wm.open_mainfile(filepath=src)
print("SRC OPENED", bpy.data.filepath)
print("OBJETOS", len(bpy.data.objects))
names = {}
for o in bpy.data.objects:
    key = o.name.split('_')[0].split('.')[0]
    names[key] = names.get(key, 0) + 1
print("GRUPOS", sorted(names.items(), key=lambda x: -x[1]))
for o in list(bpy.data.objects)[:60]:
    print("OBJ", o.name, o.type, tuple(round(v, 2) for v in o.location), tuple(round(v, 2) for v in o.dimensions))
print("MATERIAS", sorted({m.name for m in bpy.data.materials if m}))
print("CAMS", [o.name for o in bpy.data.objects if o.type == 'CAMERA'])
print("LIGHTS", [(o.name, o.data.type) for o in bpy.data.objects if o.type == 'LIGHT'])
print("SCENE", bpy.context.scene.render.engine, bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y)
bpy.ops.wm.open_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")
print("BACK TO HOUSE", len(bpy.data.objects))
