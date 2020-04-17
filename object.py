"""The classes to hold information about items in space and space itself."""
TIMESTEP = 0.01


class Vector:
    """A 3-dimensional vector."""

    def __init__(self, x, y, z):
        """Create the vector with x, y and z."""
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """Return the vector in a neat form for outputting."""
        return f'Vector({self.x}, {self.y}, {self.z})'

    def __add__(self, other):
        """Add two vectors together."""
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __mul__(self, other):
        """Multiply a vector by a number."""
        if isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise TypeError('Can only multiply a vector by a number')


class Point:
    """A point in space with mass."""

    def __init__(self, mass, pos, vel):
        """
        Create the point with its initial attributes.

            - mass: int
            - pos: Vector
            - vel: Vector
        """
        self.mass = mass
        self.pos = pos
        self.vel = vel

    def __repr__(self):
        """Return information about the point."""
        return f'Point(mass={self.mass}, pos={self.pos}, vel={self.vel})'

    def step_pos(self, timestep=TIMESTEP):
        """Step the position forward according to the points velocity."""
        self.pos = self.pos + self.vel*TIMESTEP

    def step(self, timestep=TIMESTEP):
        """Step the point forward one timestep."""
        self.step_pos(timestep=timestep)
