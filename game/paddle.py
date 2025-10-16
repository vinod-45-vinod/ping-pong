import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.speed = 7

    def move(self, dy, screen_height):
        # Use paddle's speed limit per-frame
        dy = max(-self.speed, min(self.speed, dy))
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def auto_track(self, ball, screen_height):
        # Track the center of the ball for smoother following
        ball_center_y = ball.y + ball.height / 2
        paddle_center_y = self.y + self.height / 2
        if ball_center_y < paddle_center_y - 5:
            self.move(-self.speed, screen_height)
        elif ball_center_y > paddle_center_y + 5:
            self.move(self.speed, screen_height)
