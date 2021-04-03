import math
import numpy as np
from glumpy import gloo

def circle_path(center=[0,0,0], r=1, sectors=100):
    assert r > 0 and sectors >= 3 and len(center) >= 3

    path = [[center[0], center[1], center[2]]]
    step_angle = 2*math.pi/sectors

    for i in range(sectors+1) :
        angle = i*step_angle
        x = r*math.cos(angle) + center[0]
        y = r*math.sin(angle) + center[1]
        path.append([x, y, center[2]])
    
    return path

def circle_indices(sectors=100, triangle_fan=True):
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

def circle_outline_indices(sectors=100, triangle_fan=True, line_loop=True):
    assert sectors >= 3

    indices = []

    if triangle_fan :
        indices.extend(range(1, sectors+1))
        if not line_loop :
            indices.append(1)
    else :
        for i in range(1, sectors) :
            indices.append(i * 3 + 1)
        if not line_loop :
            indices.append(1)
    
    return indices

def circle(center=[0,0,0], r=1, sectors=100, triangle_fan=True, line_loop=True):
    a_pos = 'a_position'
    v_type = [(a_pos, np.float32, 3)]

    outline =np.array(circle_outline_indices(sectors, triangle_fan, line_loop), dtype=np.uint32)
    indices = np.array(circle_indices(sectors, triangle_fan), dtype=np.uint32)
    path = np.array(circle_path(center, r, sectors), dtype=float)
    vertices = np.zeros(path.shape[0], v_type)
    vertices[a_pos] = path

    outline = outline.view(gloo.IndexBuffer)
    indices = indices.view(gloo.IndexBuffer)
    vertices = vertices.view(gloo.VertexBuffer)

    return vertices, indices, outline

