import bpy, os, time
START, END = 97, 192

s = bpy.context.scene
outdir = r"D:\Users\Asus\Desktop\BLENDER\anim"
os.makedirs(outdir, exist_ok=True)

s.camera = bpy.data.objects["Cam_Garage"]
s.render.resolution_x = 1280
s.render.resolution_y = 720
s.render.resolution_percentage = 100
s.render.image_settings.file_format = 'PNG'
s.render.image_settings.color_mode = 'RGB'
s.render.use_freestyle = True
s.render.filepath = os.path.join(outdir, "f_")
s.frame_start = START
s.frame_end = END
s.render.use_overwrite = True
s.render.use_placeholder = False

bpy.ops.wm.save_as_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")

t = time.time()
for f in range(START, END + 1):
    s.frame_set(f)
    s.render.filepath = os.path.join(outdir, "f_%04d.png" % f)
    bpy.ops.render.render(write_still=True)
    print("frame", f, "%.1fs" % (time.time() - t), flush=True)
print("DONE", START, END, "%.1fs" % (time.time() - t))
