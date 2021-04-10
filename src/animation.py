from glumpy import app, gloo, gl, glm, collections
from src import shader, circle, harmonic
import numpy as np
import math

class FourierSeriesCirclesAnimation :
    u_color = 'u_color'
    u_model = 'u_model'
    u_view = 'u_view'
    u_proj = 'u_projection'
    a_pos = 'a_position'

    def __init__(self, harmonics, view, projection, sectors=100) :
        self.__time = 0
        self.__sectors = sectors
        self.__sps = int(sectors / 4)
        self.__msps = int(1000 / self.__sps)
        self.__aps = 2 * math.pi / sectors
        self.__harmonics = harmonics
        self.__view = view
        self.__projection = projection

        vertices, indices, outline = circle.circle(sectors=sectors)
        self.__circle_v = vertices
        self.__circle_i = indices
        self.__ocircle_i = outline
        self.__circle_color =  [1, 1, 0, 0.2]
        self.__ocircle_color = [0.5, 1, 0, 1]

        unformatted_vertex = shader.source('./static/shaders/vshader.vs')
        path_vertex = unformatted_vertex.format('', 'position')
        simple_vertex = unformatted_vertex.format('attribute vec3 a_position;', 'a_position')
        fragment = shader.source('./static/shaders/fshader.fs')

        self.__circles_program = gloo.Program(simple_vertex, fragment)
        self.__circles_program.bind(vertices)
        self.__circles_program[self.u_view] = view
        self.__circles_program[self.u_proj] = projection

        model = np.eye(4, dtype=np.float32)  
        glm.scale(model, 0.5, 0.5, 1)
        self.__radiuses_program = gloo.Program(simple_vertex, fragment, count=len(harmonics)+1)
        self.__radiuses_program[self.u_model] = model
        self.__radiuses_program[self.u_view] = view
        self.__radiuses_program[self.u_proj] = projection
        self.__radiuses_program[self.u_color] = 1, 0, 1, 1

        self.__path_program = collections.RawPathCollection(color="shared", vertex=path_vertex, fragment=fragment)
        self.__path_program[self.u_model] = model
        self.__path_program[self.u_view] = view
        self.__path_program[self.u_proj] = projection
        self.__path_program[self.u_color] = 0, 1, 1, 1
    
    def draw(self, dt) :
        draw_path = self._update(dt)
        radiuses_path = self._get_radiuses()

        if draw_path :
            self._add_draw_path(draw_path)

        self._draw_circles(radiuses_path[:-1])
        self._draw_radiuses(radiuses_path)
        self._draw_path()
    
    def _draw_circles(self, centers) :
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glLineWidth(3)

        for i in range(len(centers)) :
            center = centers[i]
            radius = self.__harmonics[i].radius
            model = np.eye(4, dtype=np.float32)
            glm.scale(model, radius / 2, radius / 2, 1)
            glm.translate(model, center[0]/2, center[1]/2, 0)

            self.__circles_program[self.u_model] = model
            self.__circles_program[self.u_color] = self.__circle_color
            self.__circles_program.draw(gl.GL_TRIANGLE_FAN, self.__circle_i)

            self.__circles_program[self.u_color] = self.__ocircle_color
            self.__circles_program.draw(gl.GL_LINE_LOOP, self.__ocircle_i)

    def _draw_path(self) :
        self.__path_program.draw(gl.GL_LINE_STRIP)

    def _draw_radiuses(self, radiuses) :
        gl.glLineWidth(3)
        self.__radiuses_program[self.a_pos] = radiuses
        self.__radiuses_program.draw(gl.GL_LINE_STRIP)

    def _update(self, dt) :
        self.__time += dt

        draw_path = []
        if self.__time >= self.__msps :
            sectors_number = int(self.__time / self.__msps)
            self.__time -= self.__msps * sectors_number
            
            for i in range(sectors_number) :
                x = 0
                y = 0
                for harmonic in self.__harmonics :
                    radius = harmonic.radius
                    period = harmonic.period
                    phi = harmonic.phi + self.__aps * period
                    x += math.cos(phi) * radius
                    y += math.sin(phi) * radius
                    harmonic.phi = phi
                draw_path.append((x, y, 0))
        
        return draw_path

    def _get_radiuses(self) :
        radiuses = []
        x = 0
        y = 0
        radiuses.append((x, y, 0))
        for harmonic in self.__harmonics :
            phi = harmonic.phi
            radius = harmonic.radius
            x += math.cos(phi) * radius
            y += math.sin(phi) * radius
            radiuses.append((x, y, 0))
        return radiuses

    def _add_draw_path(self, path) :
        self.__path_program.append(np.array(path))
    
