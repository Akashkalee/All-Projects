import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (150, 255, 150)
LIGHT_RED = (255, 150, 150)
LIGHT_BLUE = (150, 150, 255)

# Set up the display
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Set up clock
CLOCK = pygame.time.Clock()
FPS_EASY = 10
FPS_MEDIUM = 15
FPS_HARD = 20

# Fonts for text display
SMALL_FONT = pygame.font.SysFont('comicsansms', 25)
MEDIUM_FONT = pygame.font.SysFont('comicsansms', 35)
LARGE_FONT = pygame.font.SysFont('comicsansms', 50)

def text_objects(text, font, color):
    """Create text surface and rectangle"""
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    """Create an interactive button with rounded corners for snake-like appearance"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Create a surface for the button with alpha channel
    button_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        color = active_color
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        color = inactive_color
    
    # Draw rounded rectangle
    radius = h // 2
    rect = pygame.Rect(0, 0, w, h)
    
    # Draw the main rounded rectangle
    pygame.draw.rect(button_surface, color, rect, border_radius=radius)
    
    # Add snake-like details
    pygame.draw.circle(button_surface, color, (radius, h//2), radius)  # Left end
    pygame.draw.circle(button_surface, color, (w - radius, h//2), radius)  # Right end
    
    # Add text
    text_surf, text_rect = text_objects(msg, SMALL_FONT, BLACK)
    text_rect.center = (w//2, h//2)
    button_surface.blit(text_surf, text_rect)
    
    # Draw the final button
    GAME_DISPLAY.blit(button_surface, (x, y))

def show_score(score):
    """Display the current score on the screen"""
    score_text = SMALL_FONT.render(f"Score: {score}", True, WHITE)
    GAME_DISPLAY.blit(score_text, [10, 10])

def draw_snake(snake_list):
    """Draw the snake on the screen"""
    for i, block in enumerate(snake_list):
        # Make the head a different color
        if i == len(snake_list) - 1:
            pygame.draw.rect(GAME_DISPLAY, YELLOW, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])
        else:
            pygame.draw.rect(GAME_DISPLAY, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def message(msg, color, y_displace=0, size='small'):
    """Display a message on the screen"""
    if size == 'small':
        font = SMALL_FONT
    elif size == 'medium':
        font = MEDIUM_FONT
    elif size == 'large':
        font = LARGE_FONT
    
    text_surf, text_rect = text_objects(msg, font, color)
    text_rect.center = (WIDTH // 2, HEIGHT // 2 + y_displace)
    GAME_DISPLAY.blit(text_surf, text_rect)

def pause_game():
    """Pause the game until user presses C to continue"""
    paused = True
    
    GAME_DISPLAY.fill(BLACK)
    message("Paused", WHITE, -50, 'large')
    message("Press C to continue or Q to quit", WHITE, 50, 'medium')
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        CLOCK.tick(5)

def choose_difficulty():
    """Let the user choose the game difficulty"""
    difficulty_selected = False
    fps = FPS_MEDIUM  # Default difficulty
    
    while not difficulty_selected:
        GAME_DISPLAY.fill(BLACK)
        message("Select Difficulty", WHITE, -100, 'large')
        
        # Create buttons for different difficulties
        button("Easy", 100, 200, 100, 50, GREEN, LIGHT_GREEN, set_difficulty, FPS_EASY)
        button("Medium", 250, 200, 100, 50, BLUE, LIGHT_BLUE, set_difficulty, FPS_MEDIUM)
        button("Hard", 400, 200, 100, 50, RED, LIGHT_RED, set_difficulty, FPS_HARD)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    fps = FPS_EASY
                    difficulty_selected = True
                elif event.key == pygame.K_m:
                    fps = FPS_MEDIUM
                    difficulty_selected = True
                elif event.key == pygame.K_h:
                    fps = FPS_HARD
                    difficulty_selected = True
        
        CLOCK.tick(15)
    
    return fps

def set_difficulty(fps):
    """Set the game difficulty and start the game"""
    game_loop(fps)

def game_intro():
    """Show game introduction screen"""
    intro = True
    
    while intro:
        GAME_DISPLAY.fill(BLACK)
        message("SNAKE GAME", GREEN, -100, 'large')
        message("Eat food to grow your snake!", WHITE, -30)
        message("Use arrow keys to move", WHITE, 10)
        message("Press P to pause the game", WHITE, 50)
        
        # Create buttons for start and quit
        button("Play", 150, 300, 100, 50, GREEN, LIGHT_GREEN, choose_difficulty)
        button("Quit", 350, 300, 100, 50, RED, LIGHT_RED, quit)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    choose_difficulty()
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        CLOCK.tick(15)

def game_loop(fps=FPS_MEDIUM):
    """Main game loop"""
    game_over = False
    game_exit = False
    
    # Initial snake position
    x = WIDTH // 2
    y = HEIGHT // 2
    
    # Initial movement direction
    x_change = 0
    y_change = 0
    
    # Snake body
    snake_list = []
    snake_length = 1
    
    # Initial food position
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    
    while not game_exit:
        
        # Game over screen
        while game_over:
            GAME_DISPLAY.fill(BLACK)
            message("Game Over!", RED, -50, 'large')
            message(f"Final Score: {snake_length - 1}", WHITE, 0, 'medium')
            
            # Create buttons for play again and quit
            button("Play Again", 125, 300, 150, 50, GREEN, LIGHT_GREEN, choose_difficulty)
            button("Quit", 375, 300, 100, 50, RED, LIGHT_RED, quit)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        choose_difficulty()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:  # Prevent 180-degree turns
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_p:
                    pause_game()
        
        # Check for boundary collisions
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_over = True
        
        # Update snake position
        x += x_change
        y += y_change
        
        # Draw game elements
        GAME_DISPLAY.fill(BLACK)
        
        # Draw border
        pygame.draw.rect(GAME_DISPLAY, BLUE, [0, 0, WIDTH, HEIGHT], 2)
        
        # Draw food
        pygame.draw.rect(GAME_DISPLAY, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        
        snake_head = [x, y]
        snake_list.append(snake_head)
        
        # Remove extra segments if snake hasn't eaten food
        if len(snake_list) > snake_length:
            del snake_list[0]
        
        # Check for self-collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True
        
        draw_snake(snake_list)
        show_score(snake_length - 1)
        
        pygame.display.update()
        
        # Check if snake has eaten food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
        
        CLOCK.tick(fps)
    
    pygame.quit()
    quit()

# Start the game
if __name__ == "__main__":
    game_intro() 