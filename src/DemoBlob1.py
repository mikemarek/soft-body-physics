import math
import pygame as game

from App import *
from VerletPhysics import *


class DemoBlob(App):
    #
    world    = World(Vector(630.0, 470.0), Vector(0, 2), 10)
    blob     = world.AddComposite()
    blobsize = 100
    skinsize = 10
    #
    grabbed  = None
    radius   = blobsize-skinsize
    strength = 0.10

    #
    def Initialize(self):
        #
        j = 0.1
        k = 0.9
        steps = 30

        mat = Material(1.0, 0.0, 1.0)

        outer = []
        inner = []
        kinex = []
        
        # center anchor point
        self.blob.AddParticles(self.world.AddParticle(self.world.hsize.x, self.world.hsize.y, mat))

        # outer skin
        offset = (2.0 * math.pi) / (2 * steps)
        for i in range(steps):
            x = self.world.hsize.x + self.blobsize * math.cos(i * (2.0 * math.pi) / steps + offset)
            y = self.world.hsize.y + self.blobsize * math.sin(i * (2.0 * math.pi) / steps + offset)
            outer.append(self.world.AddParticle(x, y, mat))

        # inner skin
        for i in range(steps):
            x = self.world.hsize.x + (self.blobsize - self.skinsize) * math.cos(i * (2.0 * math.pi) / steps)
            y = self.world.hsize.y + (self.blobsize - self.skinsize) * math.sin(i * (2.0 * math.pi) / steps)
            inner.append(self.world.AddParticle(x, y, mat))

        # connect outer skin
        for i in range(1, steps):
            kinex.append(self.world.AddConstraint(outer[i-1], outer[i], k))
        kinex.append(self.world.AddConstraint(outer[len(outer)-1], outer[0], k))

        # connect inner skin
        for i in range(1, steps):
            kinex.append(self.world.AddConstraint(inner[i-1], inner[i], k))
        kinex.append(self.world.AddConstraint(inner[len(inner)-1], inner[0], k))

        # connect outer-inner skins
        for i in range(steps):
            kinex.append(self.world.AddConstraint(outer[i], inner[i], k))
        for i in range(1, steps):
            kinex.append(self.world.AddConstraint(outer[i-1], inner[i], k))
        kinex.append(self.world.AddConstraint(outer[len(outer)-1], inner[0], k))

        # connect inner skins to anchor point
        for i in range(steps):
            kinex.append(self.world.AddConstraint(self.blob.particles[0], inner[i], j))

        self.blob.AddParticles(outer, inner)
        self.blob.AddConstraints(kinex)

    #
    def Update(self):
        #
        if game.mouse.get_pressed()[0]:
            mouse = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
            if self.grabbed == None:
                distance = mouse.distance(self.blob.particles[0].position)
                if distance < self.radius:
                    self.grabbed = self.blob.particles[0]
            if self.grabbed != None:
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


if __name__ == "__main__":
    print "Starting..."
    app = DemoBlob("Loco Roco", 640, 480, 30)
    app.Run()
    print "Ending..."
