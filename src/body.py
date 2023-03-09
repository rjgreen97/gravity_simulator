import random

from src.vector import Vector


class Body:
    MIN_MASS = 5000

    def __init__(self, canvas, mass, position, velocity):
        self.canvas = canvas
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector(0, 0)
        self.radius = mass / 1000
        self.color = self.random_color()
        self.circle = self.canvas.create_oval(
            self.bbox(), outline=self.color, fill=self.color
        )

    def reset_acceleration(self):
        self.acceleration.x = 0
        self.acceleration.y = 0

    def apply_force(self, force):
        self.acceleration += force

    def draw(self):
        self.canvas.coords(self.circle, self.bbox())

    def erase(self):
        self.canvas.delete(self.circle)

    def bbox(self):
        return [
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.position.x + self.radius,
            self.position.y + self.radius,
        ]

    def __str__(self):
        return f"Body(mass={self.mass}, position={self.position}, velocity={self.velocity}, acceleration={self.acceleration})"

    @classmethod
    def random_body(cls, window, canvas):
        position = cls.random_position(window)
        velocity = cls.random_velocity()
        return cls(canvas, 5 * Body.MIN_MASS, position, velocity)

    @classmethod
    def random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    @classmethod
    def random_position(cls, window):
        x = random.randint(0, window.winfo_width())
        y = random.randint(0, window.winfo_height())
        return Vector(x, y)

    @classmethod
    def random_velocity(cls):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        return Vector(x, y)
