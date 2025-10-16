import pygame
import random
import math

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = int(x)
        self.original_y = int(y)
        self.x = float(x)
        self.y = float(y)
        self.width = int(width)
        self.height = int(height)
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)
        self.speed = 5
        self._set_random_velocity()

    def _set_random_velocity(self):
        angle = random.uniform(-0.4 * math.pi, 0.4 * math.pi)
        dir_x = random.choice([-1, 1])
        self.velocity_x = dir_x * self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce on top/bottom
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        """
        Return True if paddle hit (for sound)
        """
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            self.x = player_rect.right + 0.1
            self._bounce_off_paddle(player_rect)
            return True
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            self.x = ai_rect.left - self.width - 0.1
            self._bounce_off_paddle(ai_rect)
            return True
        return False

    def _bounce_off_paddle(self, paddle_rect):
        self.velocity_x *= -1
        paddle_center = paddle_rect.centery
        ball_center = self.y + self.height / 2
        offset = (ball_center - paddle_center) / (paddle_rect.height / 2)
        self.velocity_y += offset * 4.0

        max_speed = 10
        cur_speed = math.hypot(self.velocity_x, self.velocity_y)
        if cur_speed > max_speed:
            scale = max_speed / cur_speed
            self.velocity_x *= scale
            self.velocity_y *= scale

    def reset(self, towards_player=None):
        self.x = float(self.original_x)
        self.y = float(self.original_y)
        if towards_player is True:
            dir_choice = -1
        elif towards_player is False:
            dir_choice = 1
        else:
            dir_choice = random.choice([-1, 1])
        angle = random.uniform(-0.4 * math.pi, 0.4 * math.pi)
        self.velocity_x = dir_choice * self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))
