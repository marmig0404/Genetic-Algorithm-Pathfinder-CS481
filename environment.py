from vector import Vector


class Environment:
    def __init__(self, border, target, walls=[]):
        self.border = border
        self.target = target
        self.walls = walls

    def test_finish(self, other):
        return self.target.test_finish(other)

    def test_collision(self, other):
        wall_collisions = [wall.test_collision(other) for wall in self.walls]
        border_collision = self.border.test_collision(other)
        return any(wall_collisions) or border_collision


class Target:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

    def test_finish(self, other):
        return self.position.equals(other.position)


class Border:
    def __init__(self, top_left, bottom_right):
        self.top_wall = Wall(
            top_left,
            Vector([bottom_right.x() - top_left.x(), 0])
        )
        self.left_wall = Wall(
            top_left,
            Vector([0, bottom_right.y() - top_left.y()])
        )
        self.right_wall = Wall(
            bottom_right,
            Vector([0, top_left.y() - bottom_right.y()])
        )
        self.bottom_wall = Wall(
            bottom_right,
            Vector([top_left.x() - bottom_right.x(), 0])
        )
        self.walls = [self.top_wall, self.bottom_wall,
                      self.left_wall, self.right_wall]

    def test_collision(self, other):
        return any([wall.test_collision(other) for wall in self.walls])


class Wall:
    def __init__(self, position, vector):
        self.position = position
        self.vector = vector

    def test_collision(self, other):
        r = other.velocity
        s = self.vector
        q = self.position
        p = other.position
        u = (q - p).cross(r) / r.cross(s)
        t = (q - p).cross(s) / r.cross(s)
        return r.cross(s) != 0 and 0 <= t <= 1 and 0 <= u <= 1
