import pygame

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_WIDTH = 5
PLAYER_HEIGHT = 150
BALL_RADIUS = 20
BALL_SPEED = 5
PLAYER_COLOR = 'white'
PLAYER_SPEED = 5
TEXT_COLOR = (255, 255, 255)  # White color

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)

        self.running = True
        self.play = True
        self.ball_direction_y = 1
        self.ball_direction_x = 1
        self.player1_pos = pygame.Rect(15, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.player2_pos = pygame.Rect(SCREEN_WIDTH - 15 - PLAYER_WIDTH, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.ball_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.p1_score = 0
        self.p2_score = 0

    def move_ball(self):
        self.ball_pos.x += BALL_SPEED * self.ball_direction_x
        self.ball_pos.y += BALL_SPEED * self.ball_direction_y

        # Check for collision with top or bottom of screen
        if self.ball_pos.y - BALL_RADIUS <= 0 or self.ball_pos.y + BALL_RADIUS >= SCREEN_HEIGHT:
            self.ball_direction_y *= -1  # Reverse vertical direction

        # Check for collision with left or right of screen (goals)
        if self.ball_pos.x - BALL_RADIUS <= 15:
            if self.ball_pos.y < self.player1_pos.y or self.ball_pos.y > self.player1_pos.y + PLAYER_HEIGHT:
                self.p2_score += 1
                self.play = False
                return 1
            else:
                self.ball_direction_x *= -1  # Reverse horizontal direction
        if self.ball_pos.x + BALL_RADIUS >= SCREEN_WIDTH - 15:
            if self.ball_pos.y < self.player2_pos.y or self.ball_pos.y > self.player2_pos.y + PLAYER_HEIGHT:
                self.p1_score += 1
                self.play = False
                return -1
            else:
                self.ball_direction_x *= -1  # Reverse horizontal direction

    def restart(self, point):
        self.ball_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.ball_direction_x = point
        self.ball_direction_y = point
        return True

    def render_score(self, text, position):
        text_surface = self.font.render(text, True, TEXT_COLOR)
        self.screen.blit(text_surface, position)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player2_pos.y > 5:
            self.player2_pos.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.player2_pos.y < SCREEN_HEIGHT - PLAYER_HEIGHT - 5:
            self.player2_pos.y += PLAYER_SPEED
        if keys[pygame.K_w] and self.player1_pos.y > 5:
            self.player1_pos.y -= PLAYER_SPEED
        if keys[pygame.K_s] and self.player1_pos.y < SCREEN_HEIGHT - PLAYER_HEIGHT - 5:
            self.player1_pos.y += PLAYER_SPEED

    def run(self):
        while self.running:
            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.play:
                point = self.move_ball()
            else:
                self.play = self.restart(point)

            self.handle_input()

            # Fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            # Render game objects
            pygame.draw.rect(self.screen, PLAYER_COLOR, self.player1_pos)
            pygame.draw.rect(self.screen, PLAYER_COLOR, self.player2_pos)
            pygame.draw.circle(self.screen, PLAYER_COLOR, (int(self.ball_pos.x), int(self.ball_pos.y)), BALL_RADIUS)

            score_text = f"{self.p1_score} : {self.p2_score}"
            self.render_score(score_text, (SCREEN_WIDTH // 2 - 53, 15))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    PongGame().run()
