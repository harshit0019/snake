import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GAME_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = GAME_SIZE // GRID_SIZE
SIDEBAR_WIDTH = WINDOW_SIZE - GAME_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)  # Darker green
LIGHT_GREEN = (144, 238, 144)  # Light green for snake gradient
RED = (220, 20, 60)  # Crimson red for food
GRAY = (169, 169, 169)
DARK_GRAY = (40, 40, 40)
PURPLE = (147, 112, 219)

# Initialize game window
screen = pygame.display.set_mode((WINDOW_SIZE, GAME_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 30, 255) for c in color)
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Snake:
    def __init__(self):
        self.body = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = [1, 0]
        self.grow = False
        
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= GRID_COUNT or 
            new_head[1] < 0 or new_head[1] >= GRID_COUNT):
            return False
            
        if new_head in self.body[1:]:
            return False
            
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True
        
    def change_direction(self, new_direction):
        if (self.direction[0] != -new_direction[0] or 
            self.direction[1] != -new_direction[1]):
            self.direction = new_direction

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
        
    def generate_position(self, snake_body):
        while True:
            position = (random.randint(0, GRID_COUNT-1), 
                       random.randint(0, GRID_COUNT-1))
            if position not in snake_body:
                return position

def draw_game_background():
    # Draw checkered background
    for row in range(GRID_COUNT):
        for col in range(GRID_COUNT):
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, DARK_GRAY,
                               (col * GRID_SIZE, row * GRID_SIZE,
                                GRID_SIZE, GRID_SIZE))

def draw_snake(snake):
    # Draw snake body with gradient effect
    for i, segment in enumerate(snake.body):
        color_factor = 1 - (i / len(snake.body)) * 0.5
        segment_color = tuple(int(c * color_factor) for c in LIGHT_GREEN)
        
        # Draw rounded rectangle for each segment
        x = segment[0] * GRID_SIZE
        y = segment[1] * GRID_SIZE
        pygame.draw.rect(screen, segment_color,
                        (x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2),
                        border_radius=5)

def draw_food(food):
    # Draw food with a glowing effect
    x = food.position[0] * GRID_SIZE
    y = food.position[1] * GRID_SIZE
    
    # Draw outer glow
    pygame.draw.circle(screen, (255, 100, 100),
                      (x + GRID_SIZE//2, y + GRID_SIZE//2),
                      GRID_SIZE//2)
    # Draw inner food
    pygame.draw.circle(screen, RED,
                      (x + GRID_SIZE//2, y + GRID_SIZE//2),
                      GRID_SIZE//3)

def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0
    high_score = 0
    game_over = False
    game_active = True
    
    # Create buttons
    restart_button = Button(GAME_SIZE + 50, 200, 120, 50, "Restart", PURPLE)
    quit_button = Button(GAME_SIZE + 50, 280, 120, 50, "Quit", RED)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and game_active and not game_over:
                if event.key == pygame.K_UP:
                    snake.change_direction([0, -1])
                elif event.key == pygame.K_DOWN:
                    snake.change_direction([0, 1])
                elif event.key == pygame.K_LEFT:
                    snake.change_direction([-1, 0])
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction([1, 0])
                    
            # Handle button events
            if restart_button.handle_event(event):
                snake = Snake()
                food = Food(snake.body)
                score = 0
                game_over = False
                game_active = True
            if quit_button.handle_event(event):
                pygame.quit()
                sys.exit()

        if game_active and not game_over:
            if not snake.move():
                game_over = True
                high_score = max(score, high_score)

            if snake.body[0] == food.position:
                snake.grow = True
                food = Food(snake.body)
                score += 10

        # Draw game area
        screen.fill(BLACK)
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, GAME_SIZE, GAME_SIZE))
        draw_game_background()
        
        # Draw game elements
        draw_snake(snake)
        draw_food(food)
        
        # Draw sidebar
        pygame.draw.rect(screen, BLACK, (GAME_SIZE, 0, SIDEBAR_WIDTH, GAME_SIZE))
        
        # Draw scores
        font = pygame.font.Font(None, 48)
        score_text = font.render(f'Score: {score}', True, WHITE)
        high_score_text = font.render(f'Best: {high_score}', True, WHITE)
        screen.blit(score_text, (GAME_SIZE + 20, 50))
        screen.blit(high_score_text, (GAME_SIZE + 20, 100))
        
        # Draw buttons
        restart_button.draw(screen)
        quit_button.draw(screen)

        if game_over:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render('Game Over!', True, RED)
            text_rect = game_over_text.get_rect(center=(GAME_SIZE//2, GAME_SIZE//2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()
        clock.tick(12)  # Slightly faster game speed

if __name__ == "__main__":
    main()
