import bpy

SHELL_PREFIXES = ("Gable", "Gar_", "Tejado", "Cumbrera")
objs0 = list(bpy.data.objects)
shell = [o for o in objs0 if o.type == 'MESH' and not o.name.startswith("TH_")
         and any(o.name.startswith(p) for p in SHELL_PREFIXES)]
for o in shell:
    bpy.data.objects.remove(o, do_unlink=True)
print("ELIMINADOS_SHELL", len(shell), sorted(o.name for o in shell))

src = r"D:\Users\Asus\Desktop\BLENDER\src_model/source/casa nouuu.blend"
bpy.ops.wm.open_mainfile(filepath=src)
MAP = {
    "Material": "Pared", "Material.001": "Pared", "Material.002": "Tejado", "Material.003": "Pared",
    "Material.004": "Tejado", "Material.005": "Tejado", "Material.006": "GarajeRosa", "Material.007": "Tejado",
    "Material.008": "Cesped", "Material.009": "Valla", "Material.011": "NegroMate", "Material.012": "Cristal",
    "Material.013": "Verde", "Material.015": "Verde", "Material.016": "Blanco", "Material.018": "Pared",
    "Material.019": "Blanco", "Material.020": "Tejado", "Material.021": "NegroMate", "Material.022": "Cristal",
    "Material.023": "Trim", "Material.024": "Tejado", "Material.025": "Pared",
}
added = []
for o in [o for o in list(bpy.data.objects) if o.type == 'MESH']:
    no = o.copy(); no.data = o.data.copy()
    bpy.context.scene.collection.objects.link(no)
    no.matrix_world = o.matrix_world.copy()
    no.name = "SRC_" + o.name
    srcm = o.data.materials[0].name if o.data.materials else None
    no.data.materials.append(bpy.data.materials.get(MAP.get(srcm, "Pared")))
    added.append(no.name)
bpy.ops.wm.open_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")
print("AGREGADOS_SRC", len(added), sorted(added))

def srgb(h):
    h = h.lstrip('#')
    def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
    return tuple(lin(int(h[i:i+2],16)/255) for i in (0,2,4))

def setcol(name, hexcol):
    m = bpy.data.materials.get(name)
    if not m or not m.use_nodes: return
    rgb = srgb(hexcol)
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs['Base Color'].default_value = (*rgb, 1)

setcol('Pared', '#FFCC99'); setcol('Tejado', '#885522'); setcol('Tejado2', '#885522')
setcol('Techo_PA', '#CC9B6B'); setcol('GarajeRosa', '#E8A9AC'); setcol('Cesped', '#68AF6B')
setcol('Cristal', '#CBCCFE'); setcol('Trim', '#F4E5CB'); setcol('GarajeSuelo', '#B9B4AC')
setcol('SueloGaraje', '#B9B4AC'); setcol('CocheRosa', '#F2649B'); setcol('CocheRosa2', '#D9487A')
setcol('Hoja1', '#3E9B4F'); setcol('Hoja2', '#55B463'); setcol('Tronco', '#8B5A2B')
setcol('Verde', '#2F7D3A'); setcol('Valla', '#F2F1EA')

bpy.context.scene.frame_set(40)
bpy.ops.wm.save_as_mainfile(filepath=r"D:\Users\Asus\Desktop\BLENDER\simpsons_house.blend")
print("SWAP_OK")
