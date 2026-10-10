import pygame

from game.game_engine import GameEngine


WIDTH, HEIGHT = 500, 700
FPS = 60
SKY_BLUE = (135, 206, 235)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird - Pygame Version")
    clock = pygame.time.Clock()
    engine = GameEngine(WIDTH, HEIGHT)
    running = True

    while running:
        screen.fill(SKY_BLUE)
        restart_happened = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            # If a restart key was handled, ignore the rest of this event batch
            # for gameplay so a queued Space event cannot flap the fresh bird.
            if not restart_happened:
                restart_happened = engine.handle_event(event)

        engine.handle_input()
        engine.update()
        engine.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
