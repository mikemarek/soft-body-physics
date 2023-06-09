import math
import pygame as game

from App import *
from VerletPhysics import *


class DemoBlob(App):
    #
    world    = World(Vector(630.0, 470.0), Vector(0, 2), 6)
    blob     = world.AddComposite()
    blobsize = 100
    #
    grabbed  = None
    radius   = 20
    strength = 0.10

    #
    def Initialize(self):
        #
        k = 0.7
        steps = 40

        mat = Material(1.0, 0.0, 0.9)

        outer = []
        kinex = []

        # outer skin
        for i in range(steps):
            x = self.world.hsize.x + self.blobsize * math.cos(i * (2.0 * math.pi) / steps)
            y = self.world.hsize.y + self.blobsize * math.sin(i * (2.0 * math.pi) / steps)
            outer.append(self.world.AddParticle(x, y, mat))

        # connect outer skin
        for i in range(1, steps):
            kinex.append(self.world.AddConstraint(outer[i-1], outer[i], k))
        kinex.append(self.world.AddConstraint(outer[len(outer)-1], outer[0], k))
        for i in range(steps // 2):
            to = i + steps // 2
            if to >= steps:
                to -= steps
            kinex.append(self.world.AddConstraint(outer[i], outer[to], k))

        self.blob.AddParticles(outer)
        self.blob.AddConstraints(kinex)

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
            game.draw.line(self.screen, (255, 255, 255), pos1, pos2, 1)
        for p in self.world.particles:
            pos = (int(p.position.x), int(p.position.y))
            game.draw.circle(self.screen, (255, 255, 255), pos, 2, 0)
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
    print("Starting...")
    app = DemoBlob("Loco Roco", 640, 480, 30)
    app.Run()
    print("Ending...")
