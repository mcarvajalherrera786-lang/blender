import bpy, bmesh, math
from mathutils import Matrix, Vector

MIR = Matrix.Diagonal((-1, 1, 1, 1))

def srgb(h):
    h = h.lstrip('#')
    def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    return tuple(lin(int(h[i:i+2], 16)/255) for i in (0, 2, 4))

def setcol(name, hexcol):
    m = bpy.data.materials.get(name)
    if not m or not m.use_nodes: return
    rgb = srgb(hexcol)
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs['Base Color'].default_value = (*rgb, 1)

def delobj(pref):
    for o in list(bpy.data.objects):
        if o.name.startswith(pref):
            bpy.data.objects.remove(o, do_unlink=True)

# ---- camaras: guardar direccion antes de espejar ----
cams = {}
for o in bpy.data.objects:
    if o.type == 'CAMERA':
        fwd = (o.matrix_world.to_quaternion() @ Vector((0, 0, -1)))
        cams[o.name] = (o.location.copy(), fwd)

# ---- espejar mallas (con normales corregidas) ----
nmesh = 0
for o in list(bpy.data.objects):
    if o.type != 'MESH': continue
    me = o.data
    me.transform(MIR @ o.matrix_world)
    # origen en el centro de la geometria
    if len(me.vertices):
        c = sum((v.co for v in me.vertices), Vector()) / len(me.vertices)
        me.transform(Matrix.Translation(-c))
        o.matrix_world = Matrix.Translation(c)
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    me.update()
    nmesh += 1

# ---- luces ----
for o in bpy.data.objects:
    if o.type == 'LIGHT' and o.data.type != 'SUN':
        o.location.x *= -1

# ---- camaras: posicion y direccion espejadas ----
for name, (loc, fwd) in cams.items():
    o = bpy.data.objects[name]
    loc = Vector((-loc.x, loc.y, loc.z))
    fwd = Vector((-fwd.x, fwd.y, fwd.z))
    o.location = loc
    o.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler()

# ---- textos (no se espejan: se recolocan) ----
t = bpy.data.objects.get('TextoNoGirls')
if t: t.location.x *= -1

# ---- frente libre: fuera arbustos y seto ----
delobj('Arbusto_')
delobj('Seto_Frontal')

# ---- colores casa real ----
setcol('Pared',      '#E3B183')   # beige-melocoton
setcol('Tejado',     '#885522')   # marron del tejado
setcol('Tejado2',    '#7A4A1E')
setcol('Trim',       '#F4E5CB')
setcol('Blanco',     '#F6F2E8')
setcol('Puerta',     '#8C3B22')
setcol('CocheRosa',  '#F2649B')
setcol('CocheRosa2', '#D94B80')
setcol('Parrilla',   '#2B2B2B')

# puerta del garaje en rosa palido
for n in ('Garaje_Puerta_Abierta', 'Garaje_Panel0', 'Garaje_Panel1'):
    o = bpy.data.objects.get(n)
    if o:
        m = bpy.data.materials.get('GarajeRosa')
        if not m:
            m = bpy.data.materials.new('GarajeRosa'); m.use_nodes = True
            b = next(x for x in m.node_tree.nodes if x.type == 'BSDF_PRINCIPLED')
            b.inputs['Base Color'].default_value = (*srgb('#EFC0BA'), 1)
            b.inputs['Roughness'].default_value = 0.6
        o.data.materials.clear(); o.data.materials.append(m)

# ---- suelo del garaje mas claro ----
g = bpy.data.objects.get('Garaje_Suelo')
if g:
    m = bpy.data.materials.new('GarajeSuelo'); m.use_nodes = True
    b = next(x for x in m.node_tree.nodes if x.type == 'BSDF_PRINCIPLED')
    b.inputs['Base Color'].default_value = (*srgb('#B9B4AC'), 1)
    b.inputs['Roughness'].default_value = 0.85
    g.data.materials.clear(); g.data.materials.append(m)

print('MIRROR OK', nmesh, 'objects', len(bpy.data.objects))
