import pygame as game

from App import *
from VerletPhysics import *


class DemoRagDoll(App):
    #
    world    = World(Vector(630.0, 480.0), Vector(0, 2), 4)
    ragdoll  = world.AddComposite()
    #
    grabbed  = None
    severed  = False
    radius   = 20
    strength = 0.20

    #
    def Initialize(self):
        #
        dome    = 40
        torso   = 60
        bicep   = 25
        forearm = 25
        thigh   = 35
        calf    = 35
        #
        head    = self.world.AddParticle( 320.0, 100.0 )
        waist   = self.world.AddParticle( head.position.x,              head.position.y + torso )
        lelbow  = self.world.AddParticle( head.position.x - bicep,      head.position.y         )
        lhand   = self.world.AddParticle( lelbow.position.x - forearm,  lelbow.position.y       )
        relbow  = self.world.AddParticle( head.position.x + bicep,      head.position.y         )
        rhand   = self.world.AddParticle( relbow.position.x + forearm,  relbow.position.y       )
        lknee   = self.world.AddParticle( waist.position.x - thigh,     waist.position.y        )
        lfoot   = self.world.AddParticle( lknee.position.x,             lknee.position.y + calf )
        rknee   = self.world.AddParticle( waist.position.x + thigh,     waist.position.y        )
        rfoot   = self.world.AddParticle( rknee.position.x,             rknee.position.y + calf )

        self.ragdoll.AddParticles(
            head, waist, lelbow, lhand, relbow, rhand, lknee, lfoot, rknee, rfoot)
        self.ragdoll.AddConstraints(
            self.world.AddConstraint(head,   waist,  1.0),
            self.world.AddConstraint(head,   lelbow, 1.0),
            self.world.AddConstraint(head,   relbow, 1.0),
            self.world.AddConstraint(waist,  lknee,  1.0),
            self.world.AddConstraint(waist,  rknee,  1.0),
            self.world.AddConstraint(lelbow, lhand,  1.0),
            self.world.AddConstraint(relbow, rhand,  1.0),
            self.world.AddConstraint(lknee,  lfoot,  1.0),
            self.world.AddConstraint(rknee,  rfoot,  1.0))
        self.ragdoll.SetMaterial(Material(0.8, 0.1, 1.0))


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
        if game.key.get_pressed()[game.K_SPACE] and not self.severed:
            cknee1  = self.ragdoll.constraints[3]
            cknee2  = self.ragdoll.constraints[4]
            lknee   = self.ragdoll.particles[6]
            rknee   = self.ragdoll.particles[8]
            head    = self.ragdoll.particles[0]
            waist1  = self.ragdoll.particles[2]
            waist2  = self.world.AddParticle(waist1.position.x, waist1.position.y)
            self.ragdoll.AddParticles(waist2)
            self.ragdoll.AddConstraints(
            self.world.AddConstraint(waist2, lknee,  1.0, 35),
            self.world.AddConstraint(waist2, rknee,  1.0, 35))
            self.ragdoll.constraints.remove(cknee1)
            self.ragdoll.constraints.remove(cknee2)
            self.world.constraints.remove(cknee1)
            self.world.constraints.remove(cknee2)
            self.severed = True
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
            game.draw.line(self.screen, (255, 255, 255), pos1, pos2, 5)
        for p in self.world.particles:
            pos = (int(p.position.x), int(p.position.y))
            game.draw.circle(self.screen, (255, 255, 255), pos, 2, 0)
        h = (int(self.ragdoll.particles[0].position.x), int(self.ragdoll.particles[0].position.y))
        game.draw.circle(self.screen, (255, 255, 255), h, 12, 0)
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
    app = DemoRagDoll("RagDoll", 640, 480, 30)
    app.Run()
    print "Ending..."
