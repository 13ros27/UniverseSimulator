"""The classes to hold information about items in space and space itself."""
import math
from copy import deepcopy

# Constants
TIMESTEP = 0.0001
G = 0.00000000006743
c = 299792458


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
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        """Subtract a vector from this."""
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)

    def __mul__(self, other):
        """Multiply a vector by a number."""
        if isinstance(other, (int, float)):
            return Vector(self.x*other, self.y*other, self.z*other)
        else:
            raise TypeError('Can only multiply a vector by a number')

    def __truediv__(self, other):
        """Divide a vector by a number."""
        if isinstance(other, (int, float)):
            return Vector(self.x/other, self.y/other, self.z/other)
        else:
            raise TypeError('Can only multiply a vector by a number')

    def __pow__(self, other):
        """Raise each element of this vector to a power."""
        if isinstance(other, (int, float)):
            return Vector(self.x**other, self.y**other, self.z**other)
        else:
            raise TypeError('Can only multiply a vector by a number')

    @property
    def sum(self):
        """Get the sum of the vector parts."""
        return self.x + self.y + self.z

    def dist(self, other):
        """Distance between this vector and another."""
        return math.sqrt(((self-other)**2).sum)


class UnitVector(Vector):
    """A 3-dimensional vector with a length of one."""

    def __init__(self, x, y, z):
        """Create the vector with x, y and z."""
        length = math.sqrt(x*x + y*y + z*z)
        self.x = x/length
        self.y = y/length
        self.z = z/length

    def __repr__(self):
        """Return the vector in a neat form for outputting."""
        return f'UnitVector({self.x}, {self.y}, {self.z})'


class Space:
    """Space for any item to exist in."""

    def __init__(self):
        """Create a blank list of objects."""
        self.objs = []
        self.new_objects = []
        self.time = 0

    def add(self, obj):
        """Add an object to the space."""
        if self.new_objects != []:
            self.unlock()
        self.objs.append(obj)

    def objects(self, cur_obj=None):
        """Return the mass and position of all objects except the given one."""
        if cur_obj is None:
            return self.objs
        ret = []
        for obj in self.objs:
            if obj != cur_obj:
                ret.append(obj)
        return ret

    def unlock(self):
        """Unlocks all objects in this space."""
        for i in range(len(self.objs)):
            self.objs[i].mass = self.new_objects[i].mass
            self.objs[i].pos = self.new_objects[i].pos
            self.objs[i].vel = self.new_objects[i].vel

    def lock(self):
        """Lock all objects in this space."""
        self.new_objects = []
        for obj in self.objs:
            self.new_objects.append(deepcopy(obj))

    def step(self, timestep=TIMESTEP):
        """Step all objects in this space while locking their positions."""
        self.lock()
        for obj in self.new_objects:
            obj.step(timestep=timestep)
        self.unlock()
        self.time += timestep


class Point:
    """A point in space with mass."""

    def __init__(self, mass, pos, vel, space):
        """
        Create the point with its initial attributes.

            - mass:  int (kg)
            - pos:   Vector (m)
            - vel:   Vector (m)
            - space: Space
        """
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.space = space
        space.add(self)
        self.acc = Vector(0, 0, 0)

    def __repr__(self):
        """Return information about the point."""
        return f'Point(mass={self.mass}, pos={self.pos}, vel={self.vel})'

    def step_pos(self, timestep=TIMESTEP):
        """Step the position forward according to the points velocity."""
        self.pos += self.vel*timestep

    def step_vel(self, timestep=TIMESTEP):
        """Step the velocity forward according to the points acceleration."""
        self.vel += self.acc*timestep

    def update(self):
        """Update the acceleration according to the objects around it."""
        objects = self.space.objects(cur_obj=self)
        force = Vector(0, 0, 0)
        for obj in objects:
            dist = self.pos.dist(obj.pos)
            sc_force = G*(self.mass*obj.mass)/(dist**2)
            direction = (obj.pos-self.pos)/dist
            force += direction*sc_force
        self.acc = force / self.mass

    def step(self, timestep=TIMESTEP):
        """Step the point forward one timestep."""
        self.update()
        self.step_vel(timestep=timestep)
        self.step_pos(timestep=timestep)


class Photon(Point):
    """A point with 0 mass."""

    def __init__(self, pos, direction, space):
        """
        Create the point with its initial attributes.

            - mass:  int (kg)
            - pos:   Vector (m)
            - direction:   UnitVector
            - space: Space
        """
        self.mass = 0
        self.pos = pos
        self.direction = direction
        self.vel = self.direction*c
        self.space = space
        space.add(self)

    def __repr__(self):
        """Return information about the point."""
        return f'Photon(mass={self.mass}, pos={self.pos}, vel={self.vel})'

    def step(self, timestep=TIMESTEP):
        """Step the point forward one timestep."""
        self.step_pos(timestep=timestep)


s = Space()
bh = Point(float('Inf'), Vector(0, 0, 0), Vector(0, 0, 0), s)
photon = Photon(Vector(5000, 5000, 5000), UnitVector(1, 0, 0), s)
for i in range(1000):
    s.step()
print(bh)
print(photon)
