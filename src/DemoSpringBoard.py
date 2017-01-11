import pygame as game

from App import *
from VerletPhysics import *


class DemoSpringBoard(App):
    #
    world    = World(Vector(640.0, 480.0), Vector(0, 2), 4)
    board    = world.AddComposite()
    #
    segments = 5
    mousepos = Vector()
    previous = Vector()
    strength = 0.50


    #
    def Initialize(self):
        #
        for i in range(self.segments+1):
            self.board.AddParticles(
                self.world.AddParticle(50.0 + i * 100.0, 190.0), # y=210.0
                self.world.AddParticle(50.0 + i * 100.0, 290.0)) # y=270.0
        for i in range(0, 2*self.segments, 2):
            if i is 0:
                self.board.AddConstraints(
                    self.world.AddConstraint(self.board.particles[i+0], self.board.particles[i+1], 1.0))
            self.board.AddConstraints(
                self.world.AddConstraint(self.board.particles[i+0], self.board.particles[i+2], 1.0),
                self.world.AddConstraint(self.board.particles[i+0], self.board.particles[i+3], 1.0),
                self.world.AddConstraint(self.board.particles[i+1], self.board.particles[i+2], 1.0),
                self.world.AddConstraint(self.board.particles[i+1], self.board.particles[i+3], 1.0),
                self.world.AddConstraint(self.board.particles[i+2], self.board.particles[i+3], 1.0))
        self.board.particles[0].material.mass = 0.0
        self.board.particles[1].material.mass = 0.0


    #
    def Update(self):
        #
        self.mousepos = Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])
        if game.mouse.get_pressed()[0]:
            force = (self.mousepos - self.previous) * self.strength
            self.board.particles[10].ApplyForce(force)
            self.board.particles[11].ApplyForce(force)
        self.previous = self.mousepos
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
            dist = (c.node2.position - c.node1.position).magnitude() - c.target
            if dist < 0.0:
                dist = 0.0
            col  = (255, max(0.0, 255 - dist * 255), max(0.0, 255 - dist * 255))
            game.draw.line(self.screen, col, pos1, pos2, 3)
        game.display.update()


if __name__ == "__main__":
    print "Starting..."
    app = DemoSpringBoard("Spring Board", 640, 480, 30)
    app.Run()
    print "Ending..."
