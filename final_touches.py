import bpy, bmesh
from mathutils import Matrix

def delobj(pref):
    for o in list(bpy.data.objects):
        if o.name.startswith(pref):
            bpy.data.objects.remove(o, do_unlink=True)

def setcol(name, hexcol):
    m = bpy.data.materials.get(name)
    if not m or not m.use_nodes: return
    h = hexcol.lstrip('#')
    def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    rgb = tuple(lin(int(h[i:i+2],16)/255) for i in (0,2,4))
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs['Base Color'].default_value = (*rgb, 1)

def box(name,sx,sy,sz,x,y,z,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x,y,z), rotation=rot)
    o=bpy.context.active_object; o.name=name; o.scale=(sx,sy,sz)
    if m: o.data.materials.append(m)
    return o

def srgb(h):
    h=h.lstrip('#')
    def lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
    return tuple(lin(int(h[i:i+2],16)/255) for i in (0,2,4))

# ---- quitar arbol del frente derecho (solo queda el de la casa del arbol) ----
delobj('Arbol_')

# ---- marco de la puerta principal y del garaje (columnas fuera de la puerta) ----
box("PuertaMarco_PilarIzq",0.14,0.16,2.15,-0.53,-4.02,1.08, bpy.data.materials['Trim'])
box("PuertaMarco_PilarDer",0.14,0.16,2.15,0.53,-4.02,1.08, bpy.data.materials['Trim'])
box("PuertaMarco_Lintel",1.25,0.16,0.14,0,-4.02,2.12, bpy.data.materials['Trim'])
box("GarajeMarco_PilarIzq",0.16,0.16,2.2,5.62,-4.0,1.1, bpy.data.materials['Trim'])
box("GarajeMarco_PilarDer",0.16,0.16,2.2,8.88,-4.0,1.1, bpy.data.materials['Trim'])
box("GarajeMarco_Lintel",3.46,0.16,0.16,7.25,-4.0,2.22, bpy.data.materials['Trim'])
box("GarajeMarco_Panel",3.3,2.3,0.12,7.25,-2.55,2.85, bpy.data.materials['GarajeRosa'])

# ---- colores exactos ----
setcol('Pared','FFCC99')
setcol('Tejado','885522'); setcol('Tejado2','885522'); setcol('Cumbrera','885522'); setcol('Techo_PA','CC9B6B')
setcol('Trim','F4E5CB'); setcol('Blanco','F6F2E8'); setcol('Crema','F2E8DA')
setcol('Puerta','8C3B22')
setcol('GarajeRosa','E8A9AC')
setcol('CocheRosa','F2649B'); setcol('CocheRosa2','D9487A'); setcol('CocheCristal','CBCCFE')
setcol('Cristal','CBCCFE'); setcol('Faro','E8E8E8'); setcol('Pantal','7A4A22')
setcol('Cesped','68AF6B')
setcol('SueloGaraje','B9B4AC')
setcol('Hoja1','3E9B4F'); setcol('Hoja2','55B463'); setcol('Tronco','8B5A2B')
setcol('Seto','2F7D3A')

print("TOQUES OK")
