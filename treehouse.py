import bpy, math

def box(name,sx,sy,sz,x,y,z,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x,y,z), rotation=rot)
    o=bpy.context.active_object; o.name=name; o.scale=(sx,sy,sz)
    if m: o.data.materials.append(m)
    return o
def cyl(name,r,h,x,y,z,m,rot=(0,0,0),verts=16):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=(x,y,z), rotation=rot, vertices=verts)
    o=bpy.context.active_object; o.name=name
    if m: o.data.materials.append(m)
    return o
def ico(name,rx,ry,rz,x,y,z,m):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(x,y,z))
    o=bpy.context.active_object; o.name=name; o.scale=(rx,ry,rz)
    if m: o.data.materials.append(m)
    return o
def delobj(pref):
    for o in list(bpy.data.objects):
        if o.name.startswith(pref): bpy.data.objects.remove(o, do_unlink=True)
M=bpy.data.materials.get
def newmat(name,hexcol,rough=0.8,metal=0.0):
    m=bpy.data.materials.get(name)
    if m: return m
    m=bpy.data.materials.new(name); m.use_nodes=True
    def lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
    h=hexcol.lstrip('#')
    r,g,bl=(lin(int(h[i:i+2],16)/255) for i in (0,2,4))
    b=m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value=(r,g,bl,1)
    b.inputs["Roughness"].default_value=rough; b.inputs["Metallic"].default_value=metal
    return m

for p in ("BBQ_","Columpio_","TH_","TextoNoGirls","Luz_CasaArbol","Luz_Patio"):
    delobj(p)

METAL=M("Metal"); WOOD=M("Madera"); WOOD2=M("Madera2"); ROOF2=M("Tejado2")
ROOF=M("Tejado"); RED=M("Rojo"); LEAF1=M("Hoja1"); LEAF2=M("Hoja2")
BBQ=newmat("Parrilla","#2b2b2b",0.6,0.6)
SIGNM=newmat("Cartel","#d9c9a3",0.85)

# ---------- patio + parrilla ----------
box("Patio_Trasero",4.6,2.5,0.10, 0.4,5.4,0.05, M("Patio"))
box("Patio_Escalon",1.6,0.5,0.12, -1.45,4.35,0.06, M("Patio"))
box("BBQ_Cuerpo",0.64,0.64,0.30, 2.3,5.6,0.92, BBQ)
ico("BBQ_Tapa",0.32,0.32,0.20, 2.3,5.6,1.12, BBQ)
box("BBQ_Asa",0.30,0.06,0.05, 2.3,5.25,1.18, METAL)
for i,(dx,dy) in enumerate([(-0.2,-0.2),(0.2,-0.2),(0.0,0.22)]):
    cyl("BBQ_Pata%d"%i,0.03,0.85, 2.3+dx,5.6+dy,0.45, METAL, verts=10)

# ---------- columpio ----------
for i,(dx,dy) in enumerate([(-0.9,-0.5),(-0.9,0.5),(0.9,-0.5),(0.9,0.5)]):
    box("Columpio_Poste%d"%i,0.10,0.10,2.55, 4.5+dx,9.6+dy,1.30, WOOD2)
box("Columpio_Barra",2.0,0.10,0.10, 4.5,9.1,2.55, WOOD2)
box("Columpio_Barra2",2.0,0.10,0.10, 4.5,10.1,2.55, WOOD2)
for s,(sx,sy) in enumerate([(4.2,9.6),(4.8,9.6)]):
    for c in (-1,1):
        cyl("Columpio_Cadena%d_%d"%(s,c),0.012,1.85, sx+c*0.18,sy,1.60, METAL, verts=8)
    box("Columpio_Asiento%d"%s,0.42,0.22,0.05, sx,sy,0.66, RED)

# ---------- CASA DEL ARBOL ----------
TX,TY=-6.6,7.4
cyl("TH_Tronco",0.52,6.4, TX,TY,3.2, WOOD2, verts=16)
for i,(dx,dy,rx,ry) in enumerate([(0.5,0.2,0.5,0.3),(-0.5,0.3,-0.5,0.3),(0.1,-0.5,0.3,-0.6)]):
    cyl("TH_Raiz%d"%i,0.15,1.4, TX+dx,TY+dy,0.45, WOOD2, rot=(ry,rx,0), verts=8)
for i,(dx,dy,dz,r) in enumerate([(0,0,7.7,2.7),(1.9,0.5,7.3,1.7),(-1.9,0.2,7.4,1.6),(0.3,1.7,8.0,1.5),(0.2,-1.6,7.3,1.5),(0,0,8.8,1.3)]):
    ico("TH_Copa%d"%i, r,r*0.8,r*0.75, TX+dx,TY+dy,dz, LEAF1 if i%2==0 else LEAF2)
for i in range(7):
    box("TH_Tabla%d"%i, 0.46,3.40,0.14, TX-1.44+i*0.48,TY,3.10, WOOD)
for i,(dx,dy) in enumerate([(-1.5,-1.5),(1.5,-1.5),(-1.5,1.5),(1.5,1.5)]):
    box("TH_Poste%d"%i,0.15,0.15,3.10, TX+dx,TY+dy,1.55, WOOD2)
for i in range(8):
    xx=TX-1.54+i*0.44
    box("TH_BarandaF%d"%i,0.07,0.07,1.05, xx,TY-1.55,3.62, WOOD2)
for i in range(8):
    yy=TY-1.54+i*0.44
    box("TH_BarandaL%d"%i,0.07,0.07,1.05, TX-1.55,yy,3.62, WOOD2)
    box("TH_BarandaR%d"%i,0.07,0.07,1.05, TX+1.55,yy,3.62, WOOD2)
box("TH_PasamanosF",3.20,0.08,0.09, TX,TY-1.55,4.15, WOOD)
box("TH_PasamanosL",0.08,3.20,0.09, TX-1.55,TY,4.15, WOOD)
box("TH_PasamanosR",0.08,3.20,0.09, TX+1.55,TY,4.15, WOOD)
for i,(dx,dy) in enumerate([(-1.4,0.4),(1.4,0.4),(-1.4,1.5),(1.4,1.5)]):
    box("TH_Pilar%d"%i,0.12,0.12,2.10, TX+dx,TY+dy,4.25, WOOD2)
for i in range(6):
    box("TH_ParedFondo%d"%i, 2.8,0.05,0.30, TX,TY+1.50,3.45+i*0.33, WOOD)
for i in range(6):
    box("TH_ParedIzq%d"%i, 0.05,1.1,0.30, TX-1.40,TY+0.95,3.45+i*0.33, WOOD)
box("TH_Tejado",3.30,1.60,0.12, TX,TY+0.95,5.30, ROOF2, rot=(math.radians(12),0,0))
box("TH_Cumbrera",3.32,0.10,0.10, TX,TY+0.95,5.40, ROOF)
for s in (-1,1):
    box("TH_EscaleraRail%d"%((s+1)//2), 0.08,0.08,3.55, TX+s*0.42,TY-1.72,1.72, WOOD2, rot=(0.11,0,0))
for i in range(9):
    zz=0.32+i*0.36
    box("TH_Peldano%d"%i,0.80,0.07,0.06, TX,TY-1.55-0.03*i,zz, WOOD)
box("TH_Cartel",2.55,0.06,0.42, TX,TY+0.36,5.00, SIGNM)
cu=bpy.data.curves.new("TextoNoGirls","FONT"); cu.body="NO GIRLS"; cu.size=0.16
cu.align_x='CENTER'; cu.align_y='CENTER'; cu.extrude=0.006
ob=bpy.data.objects.new("TextoNoGirls",cu); bpy.context.scene.collection.objects.link(ob)
ob.location=(TX,TY+0.32,5.00); ob.rotation_euler=(math.radians(90),0,0)
ob.data.materials.append(ROOF2)
cyl("TH_Asta",0.02,1.2, TX+0.9,TY+0.6,6.0, METAL, verts=8)
box("TH_Bandera",0.02,0.5,0.3, TX+0.9,TY+0.85,6.45, RED)

bpy.ops.object.light_add(type='POINT', location=(TX,TY-1.0,4.6))
L=bpy.context.active_object; L.name="Luz_CasaArbol"; L.data.energy=90; L.data.color=(1.0,0.85,0.65)
bpy.ops.object.light_add(type='POINT', location=(0.4,5.4,2.4))
L=bpy.context.active_object; L.name="Luz_Patio"; L.data.energy=120; L.data.color=(1.0,0.8,0.6)
print("objetos:", len(bpy.data.objects))
