# App.y
# Created by Michael Marek (2015)
# An extention class of Pygame for quick and easy use of the API. This class handles most of the
# required management to get a Pygame application running, such as initializing the window and its
# properties, clearing the screen every frame, and handling keyboard and mouse input.


import pygame as game


class App:
    #
    running   = True                            # keep the application running
    screen    = None                            # window handler pointer
    title     = "Application"                   # application window title
    size      = (0, 0)                          # application window size
    center    = (0, 0)                          # application window position
    flags     = game.HWSURFACE | game.DOUBLEBUF # hardware acceleration and double buffering
    framerate = 30                              # application frame rate


    # Class constructor. Initialize the Pygame window with a title, position, and frame rate.
    #
    # @param    t   application title
    # @param    x   window x-position
    # @param    y   window y-position
    # @param    f   application frame rate
    # @return   null
    #
    def __init__(self, t="Application", x=550, y=400, f=30):
        self.title     = t
        self.size      = (x, y)
        self.center    = (x/2, y/2)
        self.framerate = f
        self.Initialize()


    # Run the application. Manages core functionality of the application, such as updating the
    # window every frame and refreshing the screen, user input through keyboard and mouse, renders
    # content onto the screen, and cleans up the window process once it is time to exit.
    #
    # @param    null
    # @return   null
    #
    def Run(self):
        game.init()
        game.display.set_caption(self.title)
        self.screen  = game.display.set_mode(self.size, self.flags)
        self.running = True
        #
        while self.running:
            for event in game.event.get():
                self.HandleEvent(event)
            self.Update()
            self.Render()
            game.time.delay(int(1000 / self.framerate))
        self.CleanUp()


    # Handles keyboard and mouse events inputted by the end-user.
    #
    # @param    event   Event Object with information on the particular event
    # @return   null
    #
    def HandleEvent(self, event):
        if event.type == game.QUIT:
            self.running = False


    # Clears memory after the application has exited.
    #
    # @param    null
    # @return   null
    #
    def CleanUp(self):
        game.quit()


    # Exit the application.
    #
    # @param    null
    # @return   null
    #
    def Exit(self):
        self.running = False


    # User-defined function that is called a single time after the application has started, but
    # before the main game update loop. Used to define variables and objects before they are called
    # upon every game loop.
    #
    # @param    null
    # @return   null
    #
    def Initialize(self):
        pass


    # User-defined function that is called once per frame. Core game loop that the user can use to
    # update content within their own applicaitons.
    #
    # @param    null
    # @return   null
    #
    def Update(self):
        pass


    # User-defined function that is called once per frame, after the game update function. Used to
    # draw user-created content onto the screen every game loop.
    def Render(self):
        pass
