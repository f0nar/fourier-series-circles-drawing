import math
import numpy as np
from glumpy import gloo

def circle_path(center=[0,0], r=1, sectors=100):
    assert r > 0 and sectors >= 3 and len(center) >= 2

    path = [[center[0], center[1], 0]]
    step_angle = 2*math.pi/sectors

    for i in range(sectors+1) :
        angle = i*step_angle
        x = r*math.cos(angle) + center[0]
        y = r*math.sin(angle) + center[1]
        path.append([x, y, 0])
    
    return path

def circle_indices(sectors=100, triangle_fan=False):
    assert sectors >= 3

    indices = []

    if triangle_fan :
        indices.append(0)
        indices.extend(range(1, sectors+1))
        indices.append(1)
    else :
        for i in range(1, sectors+1) :
            indices.append(0)
            indices.append(i)
            indices.append(i+1)
            
    return indices

def circe(center=[0,0], r=1, sectors=100, triangle_fan=False):
    a_pos = 'position'
    v_type = [(a_pos, np.float32, 3)]

    path = np.array(circle_path(center, r, sectors), dtype=float)
    indices = np.array(circle_indices(sectors, triangle_fan), dtype=np.uint32)
    vertices = np.zeros(path.shape[0], v_type)
    vertices[a_pos] = path

    indices = indices.view(gloo.IndexBuffer)
    vertices = vertices.view(gloo.VertexBuffer)

    return vertices, indices

