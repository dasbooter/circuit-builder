import pygame
import math
#import time

clock = pygame.time.Clock()
pygame.init()
points = []
begin = False
scale = 1.0
zoom_speed = 0.1
camera_offset = [0, 0]  # Initial camera offset
dragging = False  # Flag to track if we are dragging the camera
pygame.display.set_caption(f"{clock}, {scale}")

# Node positions for the positive and negative terminals
positive_node = None
negative_node = None

# Define the snap radius
snap_radius = 15

try:
    screen = pygame.display.set_mode((1280, 1024))
    def draw_battery(screen, center, radius, scale, camera_offset):
        global positive_node, negative_node
        # Adjust center based on camera offset and scaling
        scaled_center = (center[0] * scale + camera_offset[0], center[1] * scale + camera_offset[1])
        # Draw the battery (circle)
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

    def snap_to_node(mouse_pos, positive_node, negative_node, threshold=10):
        # Calculate distance from mouse position to each node
        dist_to_positive = math.hypot(mouse_pos[0] - positive_node[0], mouse_pos[1] - positive_node[1])
        dist_to_negative = math.hypot(mouse_pos[0] - negative_node[0], mouse_pos[1] - negative_node[1])
        
        # Snap to the nearest node if within the threshold distance
        if dist_to_positive <= threshold:
            return positive_node
        elif dist_to_negative <= threshold:
            return negative_node
        return mouse_pos
    
    while True:
        screen.fill((75, 75, 75)) # Fill the screen with black
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

                if event.key == pygame.K_HOME:
                    camera_offset = [0, 0]
                    scale = 1.0

            if event.type == pygame.MOUSEWHEEL:
                # Adjust the scaling factor based on the mouse wheel movement
                if event.y > 0:  # Scroll up to zoom in
                    scale += zoom_speed
                elif event.y < 0:  # Scroll down to zoom out
                    scale = max(zoom_speed, scale - zoom_speed)  # Prevent scale from going negative or zero

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # Middle mouse button
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:  # Middle mouse button
                    dragging = False

        if dragging:
            current_mouse_pos = pygame.mouse.get_pos()
            camera_offset[0] += (current_mouse_pos[0] - last_mouse_pos[0]) / scale
            camera_offset[1] += (current_mouse_pos[1] - last_mouse_pos[1]) / scale
            last_mouse_pos = current_mouse_pos

        if any(pygame.mouse.get_pressed()) and not begin and not dragging:
            mouse_pos = pygame.mouse.get_pos()
            # Snap to the closest node (positive or negative) for the start position
            posStart = snap_to_node(mouse_pos, positive_node, negative_node, snap_radius)
            # Adjust start position by subtracting the camera offset and scaling
            posStart = ((posStart[0] - camera_offset[0]) / scale, (posStart[1] - camera_offset[1]) / scale)
            begin = True

        if begin and not dragging:
            posNow = pygame.mouse.get_pos()
            # Adjust current position by subtracting the camera offset and scaling
            posNow = ((posNow[0] - camera_offset[0]) / scale, (posNow[1] - camera_offset[1]) / scale)
            # Snap to the closest node (positive or negative) for the end position
            posNow = snap_to_node((posNow[0] * scale + camera_offset[0], posNow[1] * scale + camera_offset[1]), positive_node, negative_node, snap_radius)
            # Draw the red line considering camera offset and scaling
            pygame.draw.line(screen, (255, 0, 0), 
                             (posStart[0] * scale + camera_offset[0], posStart[1] * scale + camera_offset[1]), 
                             posNow, 
                             width=2)
                                                                                            
        if not any(pygame.mouse.get_pressed()) and begin:
            posNow = pygame.mouse.get_pos()
            # Adjust end position by subtracting the camera offset and scaling
            posNow = ((posNow[0] - camera_offset[0]) / scale, (posNow[1] - camera_offset[1]) / scale)
            # Snap to the closest node (positive or negative) for the end position
            posNow = snap_to_node((posNow[0] * scale + camera_offset[0], posNow[1] * scale + camera_offset[1]), positive_node, negative_node, snap_radius)
            # Adjust end position back to world coordinates
            posNow = ((posNow[0] - camera_offset[0]) / scale, (posNow[1] - camera_offset[1]) / scale)
            # Store the original points, not scaled points
            points.append((posStart, posNow))
            begin = False

        # Draw all the stored lines with scaling and camera offset applied
        for i in range(len(points)):
            scaled_start = (points[i][0][0] * scale + camera_offset[0], points[i][0][1] * scale + camera_offset[1])
            scaled_end = (points[i][1][0] * scale + camera_offset[0], points[i][1][1] * scale + camera_offset[1])
            pygame.draw.line(screen, (0, 255, 0), scaled_start, scaled_end, width=5)
        
        draw_battery(screen, center=(640, 300), radius=50, scale=scale, camera_offset=camera_offset)
        pygame.display.flip()
        clock.tick(30)

except Exception as e:
    print(f"ERROR: {e}")

finally:
    pygame.quit ()
