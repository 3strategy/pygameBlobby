# game class (main)
try:
    import sys
    from player import *
    from ball import *
except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((screenx, screeny))

    pygame.display.set_caption('Blobby')

    background = pygame.image.load('data\\beachback.jpg')
    background = pygame.transform.scale(background, (screenx, screeny))
    background = background.convert()

    # Initialise players, net, and ball
    players = (Player("left"), Player("right"))
    net = Net()
    pointer = Pointer()
    ball = Ball(players, net, pointer)
    Player.ball = ball  # give player a static reference to ball.

    # Initialise sprites' groups
    playersprites = pygame.sprite.RenderPlain(players)
    ballsprites = pygame.sprite.RenderPlain(ball, pointer)

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (250, 250, 250))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx

    # Initialise clock
    clock = pygame.time.Clock()

    # Game loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(54)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            # OOP:Don't ask for the information you need to do the work;
            # ask for the object that has information to do the work for you. (Allen Hollub)
            for player in players:
                player.move(event)


        info = f'{players[0].h_state}  {players[1].h_state}'
        # note the : after which comes the formmating (here .1f for 1 decimal point)
        text = font.render(info, 1, (250, 250, 250))

        screen.blit(background, (0, 0))  # this acts as a clear screen (try without and see how everything smears)
        screen.blit(text, textpos)  # if we blit to background we are smearing.

        playersprites.update()  # it matters if you update the player before or after the ball.
        ballsprites.update()  # calls the update method on sprite

        playersprites.draw(screen)
        ballsprites.draw(screen)  # blits every sprite to the screen.

        pygame.display.flip()  # refreshses the display with the content of 'screen'


if __name__ == '__main__':
    main()