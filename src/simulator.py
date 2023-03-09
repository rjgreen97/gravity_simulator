import tkinter as tk
import math
import random

from src.body import Body
from src.vector import Vector


class Simulator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gravity Simulator")
        self.window.configure(bg="black")
        self.sleep_duration = int(1000 / 60)
        self.create_canvas()
        self.create_bodies()
        self.register_bindings()

    def reset(self):
        for body in self.bodies:
            body.erase()
        self.bodies = []
        self.create_bodies()

    def create_canvas(self):
        self.canvas = tk.Canvas(
            self.window,
            width=self.window.winfo_screenwidth(),
            height=self.window.winfo_screenheight(),
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.update()

    def create_bodies(self):
        self.bodies = []
        for _ in range(2):
            body = Body.random_body(self.window, self.canvas)
            self.bodies.append(body)

    def register_bindings(self):
        self.canvas.bind("<Button-1>", self.mouse_pressed)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_released)
        self.canvas.bind("<B1-Motion>", self.mouse_dragged)
        self.window.bind("<Key>", self.key_pressed)

    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (screen_width / 2))
        y = int((screen_height / 2) - (screen_height / 2))
        self.window.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

    def mouse_pressed(self, event):
        self.mouse_x1 = event.x
        self.mouse_y1 = event.y
        self.create_indicator()

    def mouse_dragged(self, event):
        self.mouse_x2 = event.x
        self.mouse_y2 = event.y
        self.draw_line()

    def mouse_released(self, event):
        self.erase_indicator()
        position = Vector(self.mouse_x1, self.mouse_y1)
        velocity = Vector(event.x - self.mouse_x1, event.y - self.mouse_y1)
        self.add_body(position, velocity)

    def key_pressed(self, event):
        if event.char == "r":
            self.reset()

    def draw_line(self):
        self.canvas.coords(
            self.line, self.mouse_x1, self.mouse_y1, self.mouse_x2, self.mouse_y2
        )

    def create_indicator(self):
        self.line = self.canvas.create_line(0, 0, 0, 0, width=1, fill="grey")
        self.circle = self.canvas.create_oval(
            self.mouse_x1 - 5,
            self.mouse_y1 - 5,
            self.mouse_x1 + 5,
            self.mouse_y1 + 5,
            outline="grey",
        )

    def erase_indicator(self):
        self.canvas.delete(self.line)
        self.canvas.delete(self.circle)

    def add_body(self, position, velocity):
        body = Body(self.canvas, 5000, position, velocity)
        self.bodies.append(body)

    def run(self):
        self.center_window()
        self.update()
        self.window.mainloop()

    def update(self):
        for body in self.bodies:
            body.reset_acceleration()

        for i, body1 in enumerate(self.bodies):
            for j, body2 in enumerate(self.bodies):
                if i != j:
                    self.apply_gravity(body1, body2)

        for body in self.bodies:
            body.velocity += body.acceleration
            body.position += body.velocity
            self.clip_velocities()
            self.detect_wall_collision(body)
            # self.detect_wall_transition(body)
            body.draw()

        self.window.after(self.sleep_duration, self.update)

    def apply_gravity(self, body1, body2):
        G = 1
        distance = body2.position - body1.position
        force_magnitude = (G * body1.mass * body2.mass) / (distance.length() ** 2)
        force_direction = distance.normalized()
        force = force_direction * force_magnitude
        body1.apply_force(force * (1 / body1.mass))
        body2.apply_force(force * (1 / body2.mass) * -1)

    def clip_velocities(self, max_velocity=50):
        for body in self.bodies:
            body.velocity.x = max(min(body.velocity.x, max_velocity), -max_velocity)
            body.velocity.y = max(min(body.velocity.y, max_velocity), -max_velocity)

    def detect_wall_collision(self, body):
        elasticity_cooeficient = 0.75

        if body.position.x + body.radius > self.window.winfo_width():
            body.velocity.x *= -1 * elasticity_cooeficient
            body.position.x = self.window.winfo_width() - body.radius

        if body.position.x - body.radius < 0:
            body.velocity.x *= -1 * elasticity_cooeficient
            body.position.x = body.radius

        if body.position.y + body.radius > self.window.winfo_height():
            body.velocity.y *= -1 * elasticity_cooeficient
            body.position.y = self.window.winfo_height() - body.radius

        if body.position.y - body.radius < 0:
            body.velocity.y *= -1 * elasticity_cooeficient
            body.position.y = body.radius

    def detect_wall_transition(self, body):
        if body.position.x > self.window.winfo_width():
            body.position.x = body.position.x - self.window.winfo_width()

        if body.position.x < 0:
            body.position.x = self.window.winfo_width() + body.position.x

        if body.position.y > self.window.winfo_height():
            body.position.y = body.position.y - self.window.winfo_height()

        if body.position.y < 0:
            body.position.y = self.window.winfo_height() + body.position.y


if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()
