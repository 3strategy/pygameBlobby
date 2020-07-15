# game class (main)
try:
    import sys
    from player import *
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


    # Initialise sprites' groups
    playersprites = pygame.sprite.RenderPlain(players)


    # Game loop
    while 1:

        screen.blit(background, (0, 0))  # this acts as a clear screen (try without and see how everything smears)

        playersprites.update()  # it matters if you update the player before or after the ball.

        playersprites.draw(screen)
        pygame.display.flip()  # refreshses the display with the content of 'screen'


if __name__ == '__main__':
    main()