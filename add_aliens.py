import bpy, math
def mat(name, hexcol):
    m = bpy.data.materials.get(name)
    if not m:
        m = bpy.data.materials.new(name); m.use_nodes = True
    def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    h = hexcol.lstrip('#')
    rgb = tuple(lin(int(h[i:i+2],16)/255) for i in (0,2,4))
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value = (*rgb, 1)
    return m
def ico(name, r, x, y, z, m):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=r, location=(x,y,z))
    o = bpy.context.active_object; o.name = name; o.data.materials.append(m); return o
def alien(prefix, x, y, z, body_r, skin):
    c = ico(prefix+"_Cuerpo", body_r, x, y, z-body_r*0.6, skin)
    c.scale = (1,1,1.5)
    h = ico(prefix+"_Cabeza", body_r*0.85, x, y, z+body_r*0.55, skin)
    for dx in (-0.16, 0.16):
        ico(prefix+"_Ojo", body_r*0.22, x+dx, y, z+body_r*0.6, mat("AlienOjo","#111111"))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.35, location=(x, y, z+body_r*1.75), rotation=(math.pi/2,0,0))
    a = bpy.context.active_object; a.name = prefix+"_Antena"; a.data.materials.append(mat("Metal","#777777"))
    ico(prefix+"_AntenaN", 0.05, x, y, z+body_r*2.0, mat("Metal","#777777"))
KA = mat("AlienKang", "#5C9E3F"); KO = mat("AlienKodos", "#8FBF8F")
alien("Kang", -2.5, -2.0, 11.5, 0.38, KA)
alien("Kodos", 2.5, -5.0, 10.5, 0.38, KO)
print("ALIENOS_OK")
