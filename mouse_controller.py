import pygame
import math
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MouseController:
    def __init__(self, camera, snap_radius=15):
        self.camera = camera
        self.snap_radius = snap_radius
        self.posStart = None
        self.begin = False
        self.points = []

    def snap_to_node(self, mouse_pos, positive_node, negative_node):
        dist_to_positive = math.hypot(mouse_pos[0] - positive_node[0], mouse_pos[1] - positive_node[1])
        dist_to_negative = math.hypot(mouse_pos[0] - negative_node[0], mouse_pos[1] - negative_node[1])

        if dist_to_positive <= self.snap_radius:
            return positive_node
        elif dist_to_negative <= self.snap_radius:
            return negative_node
        return mouse_pos

    def handle_mouse_down(self, positive_node, negative_node):
        if not self.begin:
            mouse_pos = pygame.mouse.get_pos()
            self.posStart = self.snap_to_node(mouse_pos, positive_node, negative_node)
            self.posStart = ((self.posStart[0] - self.camera.offset[0]) / self.camera.scale, 
                             (self.posStart[1] - self.camera.offset[1]) / self.camera.scale)
            self.begin = True

    def handle_mouse_drag(self, screen, positive_node, negative_node):
        if self.begin:
            posNow = pygame.mouse.get_pos()
            posNow_world = ((posNow[0] - self.camera.offset[0]) / self.camera.scale, 
                            (posNow[1] - self.camera.offset[1]) / self.camera.scale)
            posNow_world = self.snap_to_node((posNow_world[0] * self.camera.scale + self.camera.offset[0], 
                                              posNow_world[1] * self.camera.scale + self.camera.offset[1]), 
                                             positive_node, negative_node)
            pygame.draw.line(screen, (255, 0, 0), 
                             (self.posStart[0] * self.camera.scale + self.camera.offset[0], 
                              self.posStart[1] * self.camera.scale + self.camera.offset[1]), 
                             posNow_world, width=2)

    def handle_mouse_up(self, positive_node, negative_node):
        if self.begin:
            posNow = pygame.mouse.get_pos()
            posNow_world = ((posNow[0] - self.camera.offset[0]) / self.camera.scale, 
                            (posNow[1] - self.camera.offset[1]) / self.camera.scale)
            posNow_world = self.snap_to_node((posNow_world[0] * self.camera.scale + self.camera.offset[0], 
                                              posNow_world[1] * self.camera.scale + self.camera.offset[1]), 
                                             positive_node, negative_node)
            posNow_world = ((posNow_world[0] - self.camera.offset[0]) / self.camera.scale, 
                            (posNow_world[1] - self.camera.offset[1]) / self.camera.scale)
            self.points.append((self.posStart, posNow_world))
            self.begin = False

    def draw_stored_lines(self, screen):
        for start, end in self.points:
            scaled_start = (start[0] * self.camera.scale + self.camera.offset[0], start[1] * self.camera.scale + self.camera.offset[1])
            scaled_end = (end[0] * self.camera.scale + self.camera.offset[0], end[1] * self.camera.scale + self.camera.offset[1])
            pygame.draw.line(screen, (0, 255, 0), scaled_start, scaled_end, width=5)

    def clear_last_point(self):
        if self.points:
            logging.debug(f'Clearing last point: {self.points[-1]}')
            self.points.pop()

    def clear_all_points(self):
        logging.debug('Clearing all points')
        self.points.clear()
