"""The class structures to hold information about items in space."""


class Point:
    """A point in space with mass."""

    def __init__(self, mass, pos, vel):
        """Create the point with its initial attributes."""
        self.mass = mass
        self.pos = pos
        self.vel = vel
