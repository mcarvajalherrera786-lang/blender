import bpy
for o in list(bpy.data.objects):
    if o.name.startswith("Porche_"):
        print("BORRANDO", o.name)
        bpy.data.objects.remove(o, do_unlink=True)
bpy.context.scene.frame_set(40)
bpy.ops.wm.save_as_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")
print("OK porch quitado")
