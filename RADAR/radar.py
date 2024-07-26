import pygame
import math

class AbstractCar:
    """
    Base class for Car
    """
    def __init__(self, max_vel, rotation_vel):
        self.img = pygame.Surface((40, 20))  # Placeholder for car, a simple rectangle
        self.img.fill((0, 255, 0))  # Green color
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.START_POS = (250, 350)  # Default start position
        self.x, self.y = self.START_POS
        self.acceration = 0.1
        self.radar_visible = True

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceration / 2, 0)
        self.move()

    def radar(self, win, objects):
        length = 150
        num_rays = 8
        distances = []
        for i in range(num_rays):
            angle = math.radians(self.angle + i * (360 / num_rays))
            end_x = self.x + math.cos(angle) * length
            end_y = self.y - math.sin(angle) * length
            dist = self.get_distance_to_objects((self.x, self.y), (end_x, end_y), objects)
            distances.append(dist)
            if dist < length:
                end_x = self.x + math.cos(angle) * dist
                end_y = self.y - math.sin(angle) * dist
            if self.radar_visible:
                pygame.draw.line(win, (255, 0, 0), (self.x, self.y), (end_x, end_y), 1)
        print("Distances: ", distances)

    def get_distance_to_objects(self, start, end, objects):
        min_distance = math.hypot(end[0] - start[0], end[1] - start[1])
        for obj in objects:
            dist = self.line_rect_collision(start, end, obj)
            if dist is not None and dist < min_distance:
                min_distance = dist
        return min_distance

    def line_rect_collision(self, start, end, rect):
        x1, y1 = start
        x2, y2 = end
        rect_x1, rect_y1 = rect.topleft
        rect_x2, rect_y2 = rect.bottomright

        def line_intersect_rect(x1, y1, x2, y2, rx1, ry1, rx2, ry2):
            for px, py in ((rx1, ry1), (rx2, ry1), (rx2, ry2), (rx1, ry2)):
                if ((px - x1) * (y2 - y1) == (py - y1) * (x2 - x1)):
                    return math.hypot(px - x1, py - y1)
            return None

        distances = [
            line_intersect_rect(x1, y1, x2, y2, rect_x1, rect_y1, rect_x2, rect_y1),
            line_intersect_rect(x1, y1, x2, y2, rect_x2, rect_y1, rect_x2, rect_y2),
            line_intersect_rect(x1, y1, x2, y2, rect_x2, rect_y2, rect_x1, rect_y2),
            line_intersect_rect(x1, y1, x2, y2, rect_x1, rect_y2, rect_x1, rect_y1)
        ]
        distances = [d for d in distances if d is not None]
        return min(distances) if distances else None

def blit_rotate_center(win, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    win.blit(rotated_image, new_rect.topleft)
