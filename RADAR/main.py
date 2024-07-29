import pygame
from radar import AbstractCar, RadarCar, ImageRadarCar

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Radar Environment")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def create_objects():
    objects = []
    for _ in range(5):
        obj = pygame.Rect(100 * _, 100, 50, 50)
        objects.append(obj)
    return objects

def main():
    run = True
    clock = pygame.time.Clock()
    #car = RadarCar(5, 5)
    car = ImageRadarCar(5, 5, car_image_path="assets\\BlueStrip_1.png")
    objects = create_objects()

    while run:
        clock.tick(60)
        WIN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Toggle radar visibility with 'R' key
                    car.radar_visible = not car.radar_visible

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            car.rotate(right=True)
        if keys[pygame.K_UP]:
            car.move_forward()
        if keys[pygame.K_DOWN]:
            car.move_backward()

        car.reduce_speed()
        car.draw(WIN)
        car.radar(WIN, objects)

        for obj in objects:
            pygame.draw.rect(WIN, BLACK, obj)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
