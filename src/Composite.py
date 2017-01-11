# Composite.py
# Created by Michael Marek (2015)
# A collection of particles and constraints all linked together in order to make a larger composite
# shape (soft-body).


from Vector import *
from Particle import *
from Constraint import *


class Composite:
    #
    particles   = list()    # list of particles composing this shape
    constraints = list()    # list of constraints composing this shape


    # Class constructor. Add passed particles and constraints to composite lists.
    #
    # @param    *params     tuple of Particle and Constraint objects defining this shape
    # @return   null
    #
    def __init__(self, *params):
        for param in self.traverse(params):
            if isinstance(param, Particle):
                self.particles.append(param)
            elif isinstance(param, Constraint):
                self.constraints.append(param)
            print len(self.particles)


    # Add an arbitrary number of particles to this shape.
    #
    # @param    *particles  tuple of Particle objects
    # @return   null
    #
    def AddParticles(self, *particles):
        for particle in particles:
            if isinstance(particle, Particle):
                self.particles.append(particle)


    # Add an arbitrary number of constraints to this shape.
    #
    # @param    *constraints    tuple of Constraint objects
    # @return   null
    #
    def AddConstraints(self, *constraints):
        for constraint in constraints:
            if isinstance(constraint, Constraint):
                self.constraints.append(constraint)


    # Set a global material to all particles in this shape.
    #
    # @param    material    material to be applied to all particles
    # @return   null
    #
    def SetMaterial(self, material):
        for particle in self.particles:
            particle.material = material


    # Traverses and nested tuples and yields only the values inside. Used for parsing class
    # constructor arguements; it is beneficial to pass two tuples, one of particles and the other
    # of constraints, so that the particles get added to the composite first, allowing the
    # constraints to immediately reference them in the constructor.
    #
    # @param    o       tuple of objects and/or tuples
    # @yield    Object  instance found within the passed tuple
    #
    def traverse(self, o):
        if isinstance(o, (list, tuple)):
            for value in o:
                for subvalue in self.traverse(value):
                    yield subvalue
        else:
            yield o
