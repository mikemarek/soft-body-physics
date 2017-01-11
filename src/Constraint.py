# Constraint.py
# Created by Michael Marek (2015)
# Creates a constraint between two particles in the simulation world. Once the constraint is
# created and two points are specified, the constraint attempts to maintain that initial distance
# between the two particles. The constraint is modelled as a spring, and as such, is mathematically
# defined using Hooke's law. If the particle's become too close or two far apart, a force is
# applied to each in order to restore the distance equilibrium. For our purposes, since we model
# the motion of particles using Verlet integration, we directly adjust the impulse of the
# particles to move them, rather than apply a force.


import math

from Vector import *
from Particle import *


class Constraint:
    #
    node1  = None   # first constrained particle
    node2  = None   # second constrained particle
    target = 0.0    # target distance the particles try to maintain from one another
    stiff  = 1.0    # Hooke's law spring constant [0.0, 1.0] (0 = no spring, 1 = rigid bar)
    damp   = 0.0    # Hooke's law dampening constant


    # Class constructor. Grab references of the two constrained particles, get a specified spring
    # constant for the constraint, and establish a target distance between the particles.
    #
    # @param    p1  first particle constrained
    # @param    p2  second particle constrained
    # @param    s   spring constant [0.0, 1.0]
    # @param    d   distance constraint (default seprerating distance)
    # @return   null
    #
    def __init__(self, p1, p2, s, d=None):
        #
        self.node1  = p1
        self.node2  = p2
        self.stiff  = s
        if d is None:
            self.target = math.sqrt((p2.position.x - p1.position.x)**2 + (p2.position.y - p1.position.y)**2)
        else:
            self.target = d


    # Attempt to maintain the target distance between the two constrained particles. Calculate the
    # distance between the two particles and apply a restoring impulse to each particle.
    #
    # @param    null
    # @return   null
    #
    def Relax(self):
        #
        D = self.node2.position - self.node1.position
        F = 0.5 * self.stiff * (D.length() - self.target) * D.normalized()
        if self.node1.material.mass != 0.0 and not self.node2.material.mass:
            self.node1.ApplyImpulse(2.0 * +F)
        elif not self.node1.material.mass and self.node2.material.mass != 0.0:
            self.node2.ApplyImpulse(2.0 * -F)
        else:
            self.node1.ApplyImpulse(+F)
            self.node2.ApplyImpulse(-F)
