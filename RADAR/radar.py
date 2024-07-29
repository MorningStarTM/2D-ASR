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



class RadarCar:
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
            distances.append(math.floor(dist))
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

        def line_intersect_line(p1, p2, q1, q2):
            # Returns the intersection point of two line segments
            def ccw(a, b, c):
                return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
            return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

        def intersection_point(p1, p2, q1, q2):
            # Returns the intersection point of two line segments
            A1 = p2[1] - p1[1]
            B1 = p1[0] - p2[0]
            C1 = A1 * p1[0] + B1 * p1[1]

            A2 = q2[1] - q1[1]
            B2 = q1[0] - q2[0]
            C2 = A2 * q1[0] + B2 * q1[1]

            det = A1 * B2 - A2 * B1
            if det == 0:
                return None
            x = (B2 * C1 - B1 * C2) / det
            y = (A1 * C2 - A2 * C1) / det
            return (x, y)

        def point_in_rect(point, rect):
            x, y = point
            return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

        points = [
            (rect_x1, rect_y1), (rect_x2, rect_y1),
            (rect_x2, rect_y2), (rect_x1, rect_y2)
        ]
        edges = [
            (points[0], points[1]),
            (points[1], points[2]),
            (points[2], points[3]),
            (points[3], points[0])
        ]

        nearest_dist = None
        for edge in edges:
            p1, p2 = edge
            if line_intersect_line(start, end, p1, p2):
                ip = intersection_point(start, end, p1, p2)
                if ip and point_in_rect(ip, rect):
                    dist = math.hypot(ip[0] - start[0], ip[1] - start[1])
                    if nearest_dist is None or dist < nearest_dist:
                        nearest_dist = dist
        return nearest_dist

def blit_rotate_center(win, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    win.blit(rotated_image, new_rect.topleft)



class ImageRadarCar:
    """
    Base class for Car
    """
    def __init__(self, max_vel, rotation_vel, car_image_path):
        self.img = pygame.image.load(car_image_path)
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
            distances.append(math.floor(dist))
            if dist < length:
                end_x = self.x + math.cos(angle) * dist
                end_y = self.y - math.sin(angle) * dist
            if self.radar_visible:
                pygame.draw.line(win, (255, 0, 0), (self.x+30, self.y+20), (end_x, end_y), 1)
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

        def line_intersect_line(p1, p2, q1, q2):
            # Returns the intersection point of two line segments
            def ccw(a, b, c):
                return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
            return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

        def intersection_point(p1, p2, q1, q2):
            # Returns the intersection point of two line segments
            A1 = p2[1] - p1[1]
            B1 = p1[0] - p2[0]
            C1 = A1 * p1[0] + B1 * p1[1]

            A2 = q2[1] - q1[1]
            B2 = q1[0] - q2[0]
            C2 = A2 * q1[0] + B2 * q1[1]

            det = A1 * B2 - A2 * B1
            if det == 0:
                return None
            x = (B2 * C1 - B1 * C2) / det
            y = (A1 * C2 - A2 * C1) / det
            return (x, y)

        def point_in_rect(point, rect):
            x, y = point
            return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

        points = [
            (rect_x1, rect_y1), (rect_x2, rect_y1),
            (rect_x2, rect_y2), (rect_x1, rect_y2)
        ]
        edges = [
            (points[0], points[1]),
            (points[1], points[2]),
            (points[2], points[3]),
            (points[3], points[0])
        ]

        nearest_dist = None
        for edge in edges:
            p1, p2 = edge
            if line_intersect_line(start, end, p1, p2):
                ip = intersection_point(start, end, p1, p2)
                if ip and point_in_rect(ip, rect):
                    dist = math.hypot(ip[0] - start[0], ip[1] - start[1])
                    if nearest_dist is None or dist < nearest_dist:
                        nearest_dist = dist
        return nearest_dist

