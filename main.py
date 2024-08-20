import pygame
import math
from camera import Camera
from mouse_controller import MouseController
#import time

clock = pygame.time.Clock()
pygame.init()

# Initialize camera and mouse controller
camera = Camera(width=1280, height=1024, scale=1.0, zoom_speed=0.1)
mouse_controller = MouseController(camera) 

pygame.display.set_caption(f"{clock}, {camera.scale}")

# Node positions for the positive and negative terminals
positive_node = None
negative_node = None

# Define the snap radius of nodes (only for battery currently)
snap_radius = 15

try:
    screen = pygame.display.set_mode((1280, 1024))
    def draw_battery(screen, center, radius, scale, camera_offset):
        global positive_node, negative_node
        # Adjust center based on camera offset and scaling
        scaled_center = (center[0] * scale + camera_offset[0], center[1] * scale + camera_offset[1])
        # Draw the battery 
        pygame.draw.circle(screen, (255, 0, 0), scaled_center, int(radius * scale), width=2)
        # Calculate the positions for the positive and negative terminals
        positive_position = (scaled_center[0] + int(radius * scale), scaled_center[1])
        negative_position = (scaled_center[0] - int(radius * scale), scaled_center[1])
        # Update global node positions
        positive_node = positive_position
        negative_node = negative_position
        # Draw the positive terminal (red dot)
        pygame.draw.circle(screen, (255, 0, 0), positive_position, int(5 * scale))
        # Draw the negative terminal (black dot)
        pygame.draw.circle(screen, (0, 0, 0), negative_position, int(5 * scale))
    
    while True:
        screen.fill((75, 75, 75)) # Fill the screen with grey
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                if event.key == pygame.K_DELETE:
                    mouse_controller.clear_last_point()

                if event.key == pygame.K_END:
                    mouse_controller.clear_all_points()

                if event.key == pygame.K_HOME:
                    camera.reset()

            if event.type == pygame.MOUSEWHEEL:
                camera.zoom(event.y)  # Zoom in or out
                continue  # Skip the rest of the loop for this event

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # Middle mouse button
                    camera.start_drag(pygame.mouse.get_pos())
                elif event.button == 1:  # Left mouse button
                    mouse_controller.handle_mouse_down(positive_node, negative_node)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:  # Middle mouse button
                    camera.stop_drag()
                elif event.button == 1:  # Left mouse button
                    mouse_controller.handle_mouse_up(positive_node, negative_node)

        if camera.dragging:
            camera.drag(pygame.mouse.get_pos())

        mouse_controller.handle_mouse_drag(screen, positive_node, negative_node)
        mouse_controller.draw_stored_lines(screen)
        
        draw_battery(screen, center=(640, 300), radius=50, scale=camera.scale, camera_offset=camera.offset)
        pygame.display.flip()
        clock.tick(30)

except Exception as e:
    print(f"ERROR: {e}")

finally:
    pygame.quit ()
