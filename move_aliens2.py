import bpy
def move(prefix, x, y, z):
    for n in (prefix+"_Cuerpo", prefix+"_Cabeza", prefix+"_Ojo", prefix+"_Antena", prefix+"_AntenaN"):
        o = bpy.data.objects.get(n)
        if o: o.location = (x, y, z)
move("Kang", -2.5, -2.0, 8.0)
move("Kodos", 2.5, -5.0, 7.6)
print("MOVED2")
