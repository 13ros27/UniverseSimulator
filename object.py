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
        return self

    def __mul__(self, other):
        """Multiply a vector by a number."""
        if isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise TypeError('Can only multiply a vector by a number')
        return self


class Space:
    """Space for any item to exist in."""

    def __init__(self):
        """Create a blank list of objects."""
        self.objects = []
        self.lock_objects = None

    def add(self, object):
        """Add an object to the space."""
        self.objects.append(object)
        self.lock_objects = None

    def _objects(self):
        objects = []
        for obj in self.objects:
            objects.append({'mass': obj.mass, 'pos': obj.pos})
        return objects

    def objects(self, cur_obj=None):
        """Return the mass and position of all objects except the given one."""
        if self.lock_objects is not None:
            objects = self.lock_objects
        else:
            objects = self._objects()
        ret = []
        for obj in objects:
            if obj != cur_obj:
                ret.append(obj)
        return ret

    def unlock(self):
        """Unlocks all objects in this space."""
        self.lock_objects = None

    def lock(self):
        """Lock all objects in this space."""
        self.lock_objects = self.objects()

    def step(self):
        """Step all objects in this space while locking their positions."""
        self.lock()
        for obj in self.lock_objects:
            obj.step()
        self.unlock()


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
