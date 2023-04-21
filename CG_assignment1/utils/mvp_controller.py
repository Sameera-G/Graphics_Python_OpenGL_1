import glm
import math


class MVPController:
    def __init__(self, callback_update, width: int, height: int):
        self.callback_update = callback_update
        self.width = width
        self.height = height
        self.position = glm.vec3(1, 1, -2)
        self.pitch = -0.5
        self.yaw = -0.5
        self.roll = 0.0
        self.speed = 0.4
        self.mouse_speed = 0.01
        self.fov = 90
        self.calc_view_projection()

    def calc_mvp(self, model_matrix=glm.mat4(1.0)):
        return self.projection_matrix * self.view_matrix * model_matrix

    def calc_view_projection(self):
        # 3. Implement the direction, right and up vectors here.
        # Currently none of them are correct
        # Calculate direction, right, and up vectors using Euler angles
        pch_sin = math.sin(self.pitch)
        pch_cos = math.cos(self.pitch)
        yaw_sin = math.sin(self.yaw)
        yaw_cos = math.cos(self.yaw)

        # direction
        self.direction = glm.vec3(
            pch_cos * yaw_sin,
            pch_sin,
            pch_cos * yaw_cos
        )
        self.right = glm.vec3(
            math.sin(self.yaw - math.pi / 2),
            0,
            math.cos(self.yaw - math.pi / 2)
        )
        self.up = glm.cross(self.right, self.direction)
        self.view_matrix = glm.lookAt(self.position,
                        self.position + self.direction,
                        self.up)
        self.projection_matrix = glm.perspective(glm.radians(self.fov), self.width / self.height, 0.1, 1000)

    def on_keyboard(self, key: bytes, x: int, y: int):
        # 4. Set the corresponding actions based on the key here
        #forward
        if key == b'w':
            self.position += self.direction * self.speed
        #backwards
        elif key == b's':
            self.position -= self.direction * self.speed
        #left side
        elif key == b'a':
            self.position += self.right * self.speed
        #right side
        elif key == b'd':
            self.position -= self.right * self.speed
        #up
        elif key == b'e':
            self.position -= self.up * self.speed
        #down
        elif key == b'r':
            self.position += self.up * self.speed
        self.calc_view_projection()
        self.callback_update()

        self.calc_view_projection()
        self.callback_update()

    def on_mouse(self, key: int, up: int, x: int, y: int):
        if key == 0 and up == 0:
            self.last_x = x
            self.last_y = y

    def on_mousemove(self, x: int, y: int):
        x_diff = self.last_x - x
        y_diff = self.last_y - y
        self.last_x = x
        self.last_y = y
        self.yaw -= x_diff * self.mouse_speed
        self.pitch -= y_diff * self.mouse_speed
        self.calc_view_projection()
        self.callback_update()

    def on_special_key(self, *args):
        pass

