import pygame

from .bird import Bird
from .pipe import Pipe
from .sounds import SoundEffects

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
BLACK = (0, 0, 0)

# speed (pixels/frame), gap height (pixels), spawn interval (frames)
DIFFICULTIES = {
    "Easy": {"speed": 3, "gap": 200, "interval": 120},
    "Medium": {"speed": 4, "gap": 160, "interval": 90},
    "Hard": {"speed": 6, "gap": 130, "interval": 60},
}


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 30)
        self.small_font = pygame.font.SysFont("Arial", 22)
        self.title_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 165))
        self.sounds = SoundEffects()
        self.reset("Medium")

    def reset(self, difficulty="Medium"):
        """Start a fresh round while keeping the shared sound manager."""
        if difficulty not in DIFFICULTIES:
            difficulty = "Medium"

        settings = DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.pipe_speed = settings["speed"]
        self.pipe_gap = settings["gap"]
        self.pipe_interval = settings["interval"]
        self.bird = Bird(self.width // 4, self.height // 2)
        self.pipes = [
            Pipe(self.width + 100, self.height, gap=self.pipe_gap, speed=self.pipe_speed)
        ]
        self._spawn_timer = 0
        self.score = 0
        self.game_over = False
        return True

    @staticmethod
    def circle_rect_collision(circle_x, circle_y, radius, rect):
        """Return whether a circle intersects an axis-aligned pygame.Rect."""
        closest_x = max(rect.left, min(circle_x, rect.right))
        closest_y = max(rect.top, min(circle_y, rect.bottom))
        dx = circle_x - closest_x
        dy = circle_y - closest_y
        return dx * dx + dy * dy <= radius * radius

    def handle_event(self, event):
        """Handle one event; return True only when a restart occurred."""
        if event.type == pygame.QUIT:
            return False

        if self.game_over:
            if event.type == pygame.KEYDOWN:
                choices = {
                    pygame.K_1: "Easy",
                    pygame.K_2: "Medium",
                    pygame.K_3: "Hard",
                }
                if event.key in choices:
                    self.reset(choices[event.key])
                    return True
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            # Ignore mouse clicks and all gameplay input while game over.
            return False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird.flap()
            self.sounds.play_flap()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()
            self.sounds.play_flap()
        return False

    def handle_input(self):
        # Flapping is event-driven, so no continuous polling is required.
        pass

    def _end_game(self):
        """Enter the game-over state and play the hit sound exactly once."""
        if self.game_over:
            return
        self.game_over = True
        self.sounds.play_death()

    def update(self):
        if self.game_over:
            return

        self.bird.update()
        if (
            self.bird.y - self.bird.radius <= 0
            or self.bird.y + self.bird.radius >= self.height
        ):
            self._end_game()
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(
                Pipe(self.width, self.height, gap=self.pipe_gap, speed=self.pipe_speed)
            )

        # Move pipes first, then check every collision before awarding any points.
        for pipe in self.pipes:
            pipe.move()
            if self.circle_rect_collision(
                self.bird.x, self.bird.y, self.bird.radius, pipe.top_rect()
            ) or self.circle_rect_collision(
                self.bird.x, self.bird.y, self.bird.radius, pipe.bottom_rect()
            ):
                self._end_game()
                return

        for pipe in self.pipes:
            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
                self.sounds.play_score()

        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

    def render(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        pygame.draw.circle(
            screen, WHITE, (int(self.bird.x), int(self.bird.y)), self.bird.radius
        )
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        difficulty_text = self.small_font.render(
            f"Difficulty: {self.difficulty}", True, WHITE
        )
        screen.blit(score_text, (10, 10))
        screen.blit(difficulty_text, (10, 45))

        if self.game_over:
            screen.blit(self.overlay, (0, 0))
            self._blit_centered(screen, self.title_font.render("Game Over", True, WHITE), self.height // 2 - 105)
            self._blit_centered(screen, self.font.render(f"Final Score: {self.score}", True, WHITE), self.height // 2 - 48)
            self._blit_centered(screen, self.small_font.render(f"Difficulty: {self.difficulty}", True, WHITE), self.height // 2 - 8)
            self._blit_centered(screen, self.small_font.render("1 - Easy     2 - Medium     3 - Hard", True, WHITE), self.height // 2 + 42)
            self._blit_centered(screen, self.small_font.render("Choose a difficulty to play again", True, WHITE), self.height // 2 + 75)
            self._blit_centered(screen, self.small_font.render("Q or ESC - Quit", True, WHITE), self.height // 2 + 108)

    def _blit_centered(self, screen, surface, center_y):
        screen.blit(surface, (self.width // 2 - surface.get_width() // 2, center_y))
