# Material.py
# Created by Michael Marek (2015)
# Each simulated particle has a unique material. The material specifies physical properties about
# that particle, including it's coefficient of friction, it's coefficient of restitution, and it's
# physical mass.


class Material:
    #
    friction = 0.4  # coefficient of friction [0.0, 1.0] (0 = ice, 1 = glue)
    bounce   = 0.4  # coefficient of resitution [0.0, 1.0] (0 = inelastic, 1 = elastic)
    mass     = 1.0  # physical mass


    # Class constructor. Define the material's/particle's properties.
    #
    # @param    f   coefficient of friction [0.0, 1.0]
    # @param    b   coefficient of restitution [0.0, 1.0]
    # @param    m   mass
    # @return   null
    #
    def __init__(self, f=0.4, b=0.4, m=1.0, d=0.01):
        #
        if f >= 0.0 and f <= 1.0:
            self.friction = f
        if b >= 0.0 and b <= 1.0:
            self.bounce = b
        if m >= 0.0:
            self.mass = m
