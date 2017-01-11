# World.py
# Created by Michael Marek (2015)
# A simulation space for our soft-body physics simulation. All simulated objects need a place to do
# so, and this world can be used to define global constants within the simulation (such as gravity
# and simulation time steps), as well as manage all of the simulated objects in a single place.


from Vector import *
from Particle import *
from Constraint import *
from Composite import *
from Material import *


class World:
    #
    size        = Vector(0.0, 0.0)  # world size/boundaries
    hsize       = Vector(0.0, 0.0)  # half-size world size/boundaries
    gravity     = Vector(0.0, 0.0)  # global gravitational acceleration
    step        = 0                 # time step
    delta       = 0.0               # delta time (1.0 / time step)
    #
    particles   = list()            # list of all particles being simulated
    constraints = list()            # list of all constraints being simulated
    composites  = list()            # list of all composite shapes being simulated


    # Class constructor. Initialize the simulation world. Set global constants.
    #
    # @param    s   simulation world size
    # @param    g   global acceleration constant
    # @param    t   number of time steps to simulate per simlation step
    #
    def __init__(self, s=Vector(0.0, 0.0), g=Vector(0.0, 9.8), t=8):
        self.size      = s
        self.hsize     = 0.5 * s
        self.gravity   = g
        if t < 1:
            self.step  = 1
            self.delta = 1.0
        else:
            self.step  = t
            self.delta = 1.0 / self.step


    # Simulate a number of time steps on our simulation world. For each time step, we satisfy
    # constraints between particles, accelerate all particles by the universal gravitational
    # acceleration, simulate motion of each particle, then constraint the particles to the
    # simulation world boundaries.
    #
    # @param    null
    # @return   null
    #
    def Simulate(self):
        for i in range(self.step):
            for particle in self.particles:
                particle.Accelerate(self.gravity)
                particle.Simulate()
                particle.Restrain()
                particle.ResetForces()
            for constraint in self.constraints:
                constraint.Relax()



    # Create and add a particle to the simulation world.
    #
    # @param    x           horizontal position of the particle
    # @param    y           vertical position of the particle
    # @return   Particle    object reference of the new particle
    #
    def AddParticle(self, x, y, mat=None):
        particle = Particle(self, x, y, mat)
        self.particles.append(particle)
        return particle


    # Create and add a constraint between two particles in the simulation world.
    #
    # @param    p1          first particle to be constrained
    # @param    p2          second particle to be constrained
    # @param    s           constraint spring stiffness [0.0, 1.0]
    # @param    d           distance constraint (default seperating distance)
    # @return   Constraint  object reference of the new constraint
    #
    def AddConstraint(self, p1, p2, s, d=None):
        constraint = Constraint(p1, p2, s, d)
        self.constraints.append(constraint)
        return constraint


    # Create and add a composite shape to the simulation world.
    #
    # @param    *params     multiple parameters of Particles and Constraints that make up the shape
    # @return   Composite   object reference of the new composite
    #
    def AddComposite(self, *params):
        composite = Composite(params)
        self.composites.append(composite)
        return composite
