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
        self.nodes = []  # List to store all node positions
        self.mode = 'draw'  # Mode can be 'draw' or 'drag'
        self.selected_node_index = None  # Index of the node being dragged

    def toggle_mode(self):
        if self.mode == 'draw':
            self.mode = 'drag'
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Change to hand cursor
        else:
            self.mode = 'draw'
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Change to default cursor

    def snap_to_node(self, mouse_pos, positive_node, negative_node, threshold=10):
        dist_to_positive = math.hypot(mouse_pos[0] - positive_node[0], mouse_pos[1] - positive_node[1])
        dist_to_negative = math.hypot(mouse_pos[0] - negative_node[0], mouse_pos[1] - negative_node[1])
        
        # Snap to the nearest node if within the threshold distance
        if dist_to_positive <= threshold:
            return positive_node
        elif dist_to_negative <= threshold:
            return negative_node
        
        # Also snap to any stored nodes
        for node in self.nodes:
            dist_to_node = math.hypot(mouse_pos[0] - node[0], mouse_pos[1] - node[1])
            if dist_to_node <= threshold:
                return node

        return mouse_pos
    
    def is_mouse_on_node(self, mouse_pos, node, threshold=10):
        return math.hypot(mouse_pos[0] - node[0], mouse_pos[1] - node[1]) <= threshold

    def handle_mouse_down(self, positive_node, negative_node):
        if self.mode == 'draw' and not self.begin:
            mouse_pos = pygame.mouse.get_pos()
            self.posStart = self.snap_to_node(mouse_pos, positive_node, negative_node)
            self.posStart = ((self.posStart[0] - self.camera.offset[0]) / self.camera.scale, 
                             (self.posStart[1] - self.camera.offset[1]) / self.camera.scale)
            self.begin = True
        elif self.mode == 'drag':
            mouse_pos = pygame.mouse.get_pos()
            for index, node in enumerate(self.nodes):
                if self.is_mouse_on_node(mouse_pos, node):
                    self.selected_node_index = index
                    break

    def handle_mouse_drag(self, screen, positive_node, negative_node):
        if self.mode == 'draw' and self.begin:
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
        elif self.mode == 'drag' and self.selected_node_index is not None:
            mouse_pos = pygame.mouse.get_pos()
            # Update the position of the selected node in the nodes list
            new_node_position = (mouse_pos[0], mouse_pos[1])
            self.nodes[self.selected_node_index] = new_node_position

            # Update the connected lines to move with the node
            for i, (start, end) in enumerate(self.points):
                # Check if the start or end of the line is connected to the selected node
                start_screen_pos = (start[0] * self.camera.scale + self.camera.offset[0], 
                                    start[1] * self.camera.scale + self.camera.offset[1])
                end_screen_pos = (end[0] * self.camera.scale + self.camera.offset[0], 
                                  end[1] * self.camera.scale + self.camera.offset[1])
                
                if self.is_mouse_on_node(start_screen_pos, self.nodes[self.selected_node_index]):
                    self.points[i] = (
                        ((new_node_position[0] - self.camera.offset[0]) / self.camera.scale, 
                         (new_node_position[1] - self.camera.offset[1]) / self.camera.scale), 
                        end
                    )
                elif self.is_mouse_on_node(end_screen_pos, self.nodes[self.selected_node_index]):
                    self.points[i] = (
                        start, 
                        ((new_node_position[0] - self.camera.offset[0]) / self.camera.scale, 
                         (new_node_position[1] - self.camera.offset[1]) / self.camera.scale)
                    )

    def handle_mouse_up(self, positive_node, negative_node):
        if self.mode == 'draw' and self.begin:
            posNow = pygame.mouse.get_pos()
            posNow_world = ((posNow[0] - self.camera.offset[0]) / self.camera.scale, 
                            (posNow[1] - self.camera.offset[1]) / self.camera.scale)
            posNow_world = self.snap_to_node((posNow_world[0] * self.camera.scale + self.camera.offset[0], 
                                              posNow_world[1] * self.camera.scale + self.camera.offset[1]), 
                                             positive_node, negative_node)
            posNow_world = ((posNow_world[0] - self.camera.offset[0]) / self.camera.scale, 
                            (posNow_world[1] - self.camera.offset[1]) / self.camera.scale)
            self.points.append((self.posStart, posNow_world))
            
            if posNow_world == posNow:
                new_node = (posNow_world[0] * self.camera.scale + self.camera.offset[0], 
                            posNow_world[1] * self.camera.scale + self.camera.offset[1])
                self.nodes.append(new_node)

            self.begin = False
        elif self.mode == 'drag' and self.selected_node_index is not None:
            self.selected_node_index = None  # Deselect the node after dragging

    def draw_stored_lines(self, screen):
        for start, end in self.points:
            scaled_start = (start[0] * self.camera.scale + self.camera.offset[0], start[1] * self.camera.scale + self.camera.offset[1])
            scaled_end = (end[0] * self.camera.scale + self.camera.offset[0], end[1] * self.camera.scale + self.camera.offset[1])
            pygame.draw.line(screen, (0, 255, 0), scaled_start, scaled_end, width=5)

        # Draw nodes at all stored node positions
        for node in self.nodes:
            pygame.draw.circle(screen, (0, 0, 255), node, int(5 * self.camera.scale))

    def clear_last_point(self):
        if self.points:
            logging.debug(f'Clearing last point: {self.points[-1]}')
            self.points.pop()

    def clear_all_points(self):
        logging.debug('Clearing all points')
        self.points.clear()
        self.nodes.clear()  # Clear nodes as well
