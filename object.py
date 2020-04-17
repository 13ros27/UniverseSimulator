"""The classes to hold information about items in space and space itself."""
import math

# Constants
TIMESTEP = 0.001
G = 0.00000000006743


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

    def __div__(self, other):
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
        return self.x + self.y + self.z

    def dist(self, other):
        """Distance between this vector and another."""
        return math.sqrt(((self-other)**2).sum)


class Space:
    """Space for any item to exist in."""

    def __init__(self):
        """Create a blank list of objects."""
        self.objs = []
        self.lock_objects = None

    def add(self, obj):
        """Add an object to the space."""
        self.objs.append(obj)
        self.lock_objects = None

    @staticmethod
    def _get_attrs(obj):
        return {'mass': obj.mass, 'pos': obj.pos}

    def _objects(self):
        objects = []
        for obj in self.objs:
            objects.append(self._get_attrs(obj))
        return objects

    def objects(self, cur_obj=None):
        """Return the mass and position of all objects except the given one."""
        if self.lock_objects is not None:
            objects = self.lock_objects
        else:
            objects = self._objects()
        ret = []
        for obj in objects:
            if obj != self._get_attrs(cur_obj):
                ret.append(obj)
        return ret

    def unlock(self):
        """Unlocks all objects in this space."""
        self.lock_objects = None

    def lock(self):
        """Lock all objects in this space."""
        self.lock_objects = self.objects()

    def step(self, timestep=TIMESTEP):
        """Step all objects in this space while locking their positions."""
        self.lock()
        for obj in self.lock_objects:
            obj.step(timestep=timestep)
        self.unlock()


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
        return (f'Point(mass={self.mass}, pos={self.pos}, vel={self.vel},'
                'acc={self.acc})')

    def step_pos(self, timestep=TIMESTEP):
        """Step the position forward according to the points velocity."""
        self.pos = self.pos + self.vel*timestep

    def step_vel(self, timestep=TIMESTEP):
        """Step the velocity forward according to the points acceleration."""
        self.vel = self.vel + self.acc*timestep

    def update(self):
        """Update the acceleration according to the objects around it."""
        objects = self.space.objects(cur_obj=self)
        

    def step(self, timestep=TIMESTEP):
        """Step the point forward one timestep."""
        self.update()
        self.step_vel(timestep=timestep)
        self.step_pos(timestep=timestep)
