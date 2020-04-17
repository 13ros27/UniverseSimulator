"""The classes to hold information about items in space and space itself."""

TIMESTEP = 0.01


class Point:
    """A point in space with mass."""

    def __init__(self, mass, pos, vel):
        """Create the point with its initial attributes."""
        self.mass = mass
        self.pos = pos
        self.vel = vel

    def step_pos(self, timestep=TIMESTEP):
        """Step the position forward according to the points velocity."""
        self.pos = self.pos + self.vel*TIMESTEP

    def step(self, timestep=TIMESTEP):
        """Step the point forward one timestep."""
        self.step_pos(timestep=timestep)
