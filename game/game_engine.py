import pygame
from .paddle import Paddle
from .ball import Ball
import time
import os

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height, win_score=5):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.win_score = win_score

        # Paddles and ball
        self.player = Paddle(10, height // 2 - self.paddle_height // 2,
                             self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - self.paddle_height // 2,
                         self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 12, 12, width, height)

        # Scores
        self.player_score = 0
        self.ai_score = 0

        # Font
        self.font = pygame.font.SysFont("Arial", 32)
        self.large_font = pygame.font.SysFont("Arial", 48)

        # States
        self.game_over = False
        self.winner_text = ""
        self.replay_menu_active = False

        # Load sound effects
        pygame.mixer.init()
        self.sound_wall = self._load_sound("assets/wall.wav")
        self.sound_paddle = self._load_sound("assets/paddle.wav")
        self.sound_score = self._load_sound("assets/score.wav")

    def _load_sound(self, path):
        """Helper to safely load sounds"""
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        return None

    def play_sound(self, sound):
        if sound:
            sound.play()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-self.player.speed, self.height)
        if keys[pygame.K_s]:
            self.player.move(self.player.speed, self.height)

    def update(self):
        # Replay menu or game over: don't update ball/paddles
        if self.replay_menu_active or self.game_over:
            return

        # Move and check collisions
        prev_vx, prev_vy = self.ball.velocity_x, self.ball.velocity_y
        self.ball.move()

        # Play wall sound when velocity_y flipped
        if self.ball.velocity_y != prev_vy:
            self.play_sound(self.sound_wall)

        collided = self.ball.check_collision(self.player, self.ai)
        if collided:
            self.play_sound(self.sound_paddle)

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.play_sound(self.sound_score)
            self._after_score(towards_player=False)
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.play_sound(self.sound_score)
            self._after_score(towards_player=True)

        # AI tracking
        self.ai.auto_track(self.ball, self.height)

        # Check win
        if self.player_score >= self.win_score or self.ai_score >= self.win_score:
            self.game_over = True
            self.winner_text = "Player Wins!" if self.player_score > self.ai_score else "AI Wins!"
            # Small pause before showing menu
            pygame.time.delay(600)
            self.replay_menu_active = True

    def _after_score(self, towards_player):
        self.ball.reset(towards_player=towards_player)
        pygame.time.delay(400)

    def render(self, screen):
        # Draw field
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4 - player_text.get_width() // 2, 20))
        screen.blit(ai_text, (self.width * 3 // 4 - ai_text.get_width() // 2, 20))

        # Game over overlay
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            text = self.large_font.render(self.winner_text, True, WHITE)
            screen.blit(text, ((self.width - text.get_width()) // 2, self.height // 2 - 80))

        # Replay Menu
        if self.replay_menu_active:
            self._render_replay_menu(screen)

    def _render_replay_menu(self, screen):
        lines = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Quit"
        ]
        for i, line in enumerate(lines):
            txt = self.font.render(line, True, WHITE)
            screen.blit(txt, ((self.width - txt.get_width()) // 2, self.height // 2 + i * 40))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_3]:
            self._reset_game(win_score=2)  # best of 3 → first to 2
        elif keys[pygame.K_5]:
            self._reset_game(win_score=3)
        elif keys[pygame.K_7]:
            self._reset_game(win_score=4)
        elif keys[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _reset_game(self, win_score=None):
        if win_score:
            self.win_score = win_score
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.replay_menu_active = False
        self.winner_text = ""
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2
        self.ball.reset()
