import pygame
from game.game_engine import GameEngine
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load sounds
def load_sound(filename):
    path = os.path.join("assets", filename)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    else:
        print(f"Warning: {filename} not found!")
        return None

paddle_sound = load_sound(r"C:\Users\Vinod G R\OneDrive\Desktop\lab4\ping-pong\assets\paddle.wav")
wall_sound = load_sound(r"C:\Users\Vinod G R\OneDrive\Desktop\lab4\ping-pong\assets\wall.wav")
score_sound = load_sound(r"C:\Users\Vinod G R\OneDrive\Desktop\lab4\ping-pong\assets\score.wav")
# Create GameEngine
engine = GameEngine(WIDTH, HEIGHT,
                    paddle_sound=paddle_sound,
                    wall_sound=wall_sound,
                    score_sound=score_sound)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
