import bpy
def move(prefix, x, y, z):
    for n in (prefix+"_Cuerpo", prefix+"_Cabeza", prefix+"_Ojo", prefix+"_Antena", prefix+"_AntenaN"):
        o = bpy.data.objects.get(n)
        if o: o.location = (x, y, z)
move("Kang", -2.5, -2.0, 6.6)
move("Kodos", 2.5, -5.0, 6.2)
print("MOVED")
