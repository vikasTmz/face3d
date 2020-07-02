import bpy
import os, sys
import subprocess
import numpy as np

print(sys.version_info)

import scipy.io as sio
#from skimage import io
from time import time
#import matplotlib.pyplot as plt

sys.path.append('..')
import face3d
from face3d import mesh
from face3d.morphable_model import MorphabelModel

# --------------------- Forward: parameters(shape, expression, pose) --> 3D obj  ---------------
# --- 1. load model
bfm = MorphabelModel('Data/BFM/Out/BFM.mat')
print('init bfm model success')


# --- 2. generate face mesh: vertices(represent shape) & colors(represent texture)
sp = bfm.get_shape_para('random')
ep = bfm.get_exp_para('random')
vertices = bfm.generate_vertices(sp, ep)

tp = bfm.get_tex_para('random')
colors = bfm.generate_colors(tp)
colors = np.minimum(np.maximum(colors, 0), 1)

# --- 3. create a mesh in blender and load 3dmm vertices and faces
mesh = bpy.data.meshes.new("3dmm_face")  # add the new mesh
obj = bpy.data.objects.new(mesh.name, mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

edges = []

verts = vertices.tolist()
faces = bfm.triangles.tolist()
mesh.from_pydata(verts, edges, faces)

bpy.ops.export_scene.obj(filepath='./3dmm_face.obj')
