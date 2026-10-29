import bpy
s = bpy.context.scene
s.camera = bpy.data.objects["Cam_Garage"]
s.render.resolution_x = 1280
s.render.resolution_y = 720
s.render.resolution_percentage = 100
s.render.image_settings.file_format = 'FFMPEG'
s.render.ffmpeg.format = 'MPEG4'
s.render.ffmpeg.codec = 'H264'
s.render.ffmpeg.audio_codec = 'AAC'
s.render.ffmpeg.constant_rate_factor = 'HIGH'
s.render.filepath = r"D:\Users\Asus\Desktop\BLENDER\simpsons_garage_entry.mp4"
s.frame_start = 1
s.frame_end = 96
s.render.fps = 24
snd = bpy.data.sounds.load(r"D:\Users\Asus\Downloads\Los Simpsons (Intro) (Español Latino).mp3")
se = s.sequence_editor_create()
strip = se.strips.new_sound(name="Intro_Simpsons", sound=snd, channel=1, frame_start=1, frame_end=96)
s.render.use_overwrite = True
bpy.ops.render.render(animation=True)
print("AUDIO_RENDER_DONE")
