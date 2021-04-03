from glumpy import app, gloo, gl, glm
import numpy as np
from src import shader
from src import circle

# window settings
WIDTH = 1024
HEIGHT = 1024
# shader properties
u_color = 'u_color'
u_view = 'u_view'
u_proj = 'u_projection'
a_pos = 'a_position'
# color data
opacity = 0.2
color = [1, 1, 0, opacity]
outline_color = [1, 0, 0, 1]
# tranformation matrices
projection = np.eye(4,dtype=np.float32)
view = np.eye(4,dtype=np.float32)
glm.translate(view, 0, 0, -20)
# animation settings
sectors = 100
sps = sectors / 4 # sectors per second
# sader sources
vertex = shader.source('./static/shaders/vshader.vs')
fragment = shader.source('./static/shaders/fshader.fs')

window = app.Window(width=WIDTH, height=HEIGHT)
program = gloo.Program(vertex, fragment)
vertices, indices, outline = circle.circle(sectors=sectors)
program.bind(vertices)
program[u_view] = view

@window.event
def on_resize(width, height):
    ratio = width / height
    program[u_proj] = projection = glm.perspective(45.0, ratio, 0.1, 100.0)

@window.event
def on_draw(dt):
    window.clear()

    gl.glEnable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)

    program[u_color] = color
    program.draw(gl.GL_TRIANGLE_FAN, indices)

    gl.glLineWidth(3)
    program[u_color] = outline_color
    program.draw(gl.GL_LINE_LOOP, outline)

app.run()