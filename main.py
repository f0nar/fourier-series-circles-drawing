from glumpy import app, gloo, gl
from src import shader
from src import circle

WIDTH = 1024
HEIGHT = 1024
u_color = 'color'
a_pos = 'position'
vertex = shader.source('./static/shaders/vshader.vs')
fragment = shader.source('./static/shaders/fshader.fs')
window = app.Window(width=WIDTH, height=HEIGHT)
program = gloo.Program(vertex, fragment)
vertices, indices = circle.circe()
program.bind(vertices)

@window.event
def on_draw(dt):
    window.clear()

    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)

    program[u_color] = [1, 1, 1, 1]
    
    program.draw(gl.GL_TRIANGLES, indices)

app.run()