# camera.py

class Camera:
    def __init__(self, width, height, scale=1.0, zoom_speed=0.1):
        self.width = width
        self.height = height
        self.scale = scale
        self.zoom_speed = zoom_speed
        self.offset = [0, 0]
        self.dragging = False
        self.last_mouse_pos = None

    def start_drag(self, mouse_pos):
        self.dragging = True
        self.last_mouse_pos = mouse_pos

    def stop_drag(self):
        self.dragging = False

    # Update the "offset" based on mouse movement
    def drag(self, mouse_pos):
        if self.dragging and self.last_mouse_pos:
            self.offset[0] += (mouse_pos[0] - self.last_mouse_pos[0]) / self.scale
            self.offset[1] += (mouse_pos[1] - self.last_mouse_pos[1]) / self.scale
            self.last_mouse_pos = mouse_pos

    # Adjust "scale" based on the zoom direction
    def zoom(self, direction):
        if direction > 0:
            self.scale += self.zoom_speed
        elif direction < 0:
            self.scale = max(self.zoom_speed, self.scale - self.zoom_speed)


    def reset(self):
        self.offset = [0, 0]
        self.scale = 1.0