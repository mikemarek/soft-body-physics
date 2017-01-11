import pygame as game

from App import *
from VerletPhysics import *


class DemoTriangle(App):
    #
    world    = World(Vector(640.0, 480.0), Vector(2, 0), 4)
    #
    grabbed  = None
    radius   = 20
    strength = 0.20


    #
    def Initialize(self):
        #
        mat = Material(1.0, 1.0, 1.0)

        self.world.AddParticle(250, 250, mat)
        self.world.AddParticle(350, 150, mat)
        self.world.AddParticle(450, 250, mat)

        self.world.AddConstraint(self.world.particles[0], self.world.particles[1], 0.5)
        self.world.AddConstraint(self.world.particles[1], self.world.particles[2], 0.5)
        self.world.AddConstraint(self.world.particles[2], self.world.particles[0], 0.5)

        self.world.particles[0].ApplyImpulse(Vector(-10.0, -7.0))
        self.world.particles[2].ApplyImpulse(Vector(-10.0, +7.0))


    #
    def Update(self):
        #
        if game.mouse.get_pressed()[0]:
            if self.grabbed == None:
                closest = self.ClosestPoint()
                if closest[1] < self.radius:
                    self.grabbed = closest[0]
            if self.grabbed != None:
                mouse = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
                force = (mouse - self.grabbed.position) * self.strength
                self.grabbed.ApplyImpulse(force)
        else:
            self.grabbed = None
        #
        if game.key.get_pressed()[game.K_ESCAPE]:
            self.Exit()
        #
        self.world.Simulate()


    #
    def Render(self):
        #
        self.screen.fill((24, 24, 24))
        for p in self.world.particles:
            pos = (int(p.position.x), int(p.position.y))
            game.draw.circle(self.screen, (255, 0, 0), pos, 10, 0)
        for c in self.world.constraints:
            pos1 = (int(c.node1.position.x), int(c.node1.position.y))
            pos2 = (int(c.node2.position.x), int(c.node2.position.y))
            game.draw.line(self.screen, (255, 0, 0), pos1, pos2, 2)
        game.display.update()


    #
    def ClosestPoint(self):
        mouse    = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
        closest  = None
        distance = float('inf')
        for particle in self.world.particles:
            d = mouse.distance(particle.position)
            if d < distance:
                closest  = particle
                distance = d
        return (closest, distance)


#
if __name__ == "__main__":
    print "Starting..."
    #
    app = DemoTriangle("Triangle", 640, 480, 30)
    app.Run()
    #
    print "Ending..."
