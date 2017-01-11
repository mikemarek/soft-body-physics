import pygame as game

from App import *
from VerletPhysics import *


class DemoRope(App):
    #
    world    = World(Vector(640.0, 480.0), Vector(0, 2), 4)
    #
    grabbed  = None
    radius   = 20
    strength = 0.20


    #
    def Initialize(self):
        #
        rope = self.world.AddComposite()
        rope.AddParticles(
            self.world.AddParticle(self.world.hsize.x, 50.0),
            self.world.AddParticle(self.world.hsize.x, 90.0),
            self.world.AddParticle(self.world.hsize.x, 130.0),
            self.world.AddParticle(self.world.hsize.x, 170.0),
            self.world.AddParticle(self.world.hsize.x, 210.0),
            self.world.AddParticle(self.world.hsize.x, 250.0),
            self.world.AddParticle(self.world.hsize.x, 290.0),
            self.world.AddParticle(self.world.hsize.x, 330.0),
            self.world.AddParticle(self.world.hsize.x, 370.0),
            self.world.AddParticle(self.world.hsize.x, 410.0))
        rope.AddConstraints(
            self.world.AddConstraint(rope.particles[0], rope.particles[1], 1.0),
            self.world.AddConstraint(rope.particles[1], rope.particles[2], 1.0),
            self.world.AddConstraint(rope.particles[2], rope.particles[3], 1.0),
            self.world.AddConstraint(rope.particles[3], rope.particles[4], 1.0),
            self.world.AddConstraint(rope.particles[4], rope.particles[5], 1.0),
            self.world.AddConstraint(rope.particles[5], rope.particles[6], 1.0),
            self.world.AddConstraint(rope.particles[6], rope.particles[7], 1.0),
            self.world.AddConstraint(rope.particles[7], rope.particles[8], 1.0),
            self.world.AddConstraint(rope.particles[8], rope.particles[9], 1.0))
        rope.particles[0].material.mass = 0.0
        rope.particles[9].ApplyForce(Vector(400.0, -900.0))


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
        self.world.Simulate()


    #
    def Render(self):
        #
        self.screen.fill((24, 24, 24))
        for c in self.world.constraints:
            pos1 = (int(c.node1.position.x), int(c.node1.position.y))
            pos2 = (int(c.node2.position.x), int(c.node2.position.y))
            game.draw.line(self.screen, (255, 0, 0), pos1, pos2, 4)
        for p in self.world.particles:
            pos = (int(p.position.x), int(p.position.y))
            game.draw.circle(self.screen, (255, 255, 255), pos, 8, 0)
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


if __name__ == "__main__":
    print "Starting..."
    app = DemoRope("Swinging Rope", 640, 480, 30)
    app.Run()
    print "Ending..."
