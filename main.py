import pygame
#import time

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(f"{clock}")
points = []
begin = False

try:
    screen = pygame.display.set_mode((1280, 1024))
    while True:
        screen.fill((0, 0, 0)) # Fill the screen with black
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                if event.key == pygame.K_DELETE:
                    del points[-1]

                if event.key == pygame.K_END:
                    points.clear()

        if any(pygame.mouse.get_pressed()) and not begin:
            posStart = pygame.mouse.get_pos()
            begin = True

        if begin:
            posNow = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255, 0, 0), (posStart[0], posStart[1]), (posNow[0], posNow[1]), width=2)
                                                                                            

        if not any(pygame.mouse.get_pressed()) and begin:
            points.append((posStart, posNow))
            begin = False

        for i in range(len(points)):
            pygame.draw.line(screen, (0, 255, 0), (points[i][0][0], points[i][0][1]), (points[i][1][0], points[i][1][1]), width=5)
        
        pygame.display.flip()
        clock.tick(30)

except Exception as e:
    print(f"ERROR: {e}")

finally:
    pygame.quit ()
