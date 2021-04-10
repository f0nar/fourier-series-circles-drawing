from glumpy import app, glm
import numpy as np
from src.harmonic import CircleHarmonic
from src.animation import FourierSeriesCirclesAnimation

WIDTH = 1024
HEIGHT = 1024
window = app.Window(width=WIDTH, height=HEIGHT)

projection = glm.perspective(45.0, WIDTH / HEIGHT, 0.1, 100.0)
view = np.eye(4,dtype=np.float32)
glm.translate(view, 0, 0, -90)

harmonics = [CircleHarmonic(20), CircleHarmonic(20, -1)]
animation = FourierSeriesCirclesAnimation(harmonics, view, projection)

@window.event
def on_draw(dt):
    window.clear()
    animation.draw(dt*1000)

app.run()