import bpy
src = r"D:\Users\Asus\Desktop\BLENDER\src_model\source\casa nouuu.blend"
bpy.ops.wm.open_mainfile(filepath=src)
print("SRC MATS")
for m in sorted(bpy.data.materials, key=lambda m: m.name):
    if m.use_nodes:
        b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        col = tuple(round(v, 3) for v in b.inputs['Base Color'].default_value) if b else None
        rough = b.inputs['Roughness'].default_value if b else None
        print("MAT %s col %s rough %s" % (m.name, col, rough))
bpy.ops.wm.open_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")
print("BACK TO HOUSE")
