import pygame
import random
import sys
import matplotlib.pyplot as plt

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bubble Tap Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# Bubble settings
bubble_radius = 30
fall_speed = 1
score = 0
missed_bubbles = 0
bubbles_generated = 0  # Total bubbles generated
bubbles_burst = 0      # Total bubbles burst

# Define a Bubble class
class Bubble:
    def __init__(self):
        self.x = random.randint(bubble_radius, SCREEN_WIDTH - bubble_radius)
        self.y = -bubble_radius
        self.taps = random.randint(1, 5)  # Number of taps required
        self.initial_taps = self.taps     # Store initial taps for scoring
        self.color = self.random_color()  # Assign a random color

    def random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), bubble_radius)
        text = font.render(str(self.taps), True, WHITE)
        screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def fall(self):
        self.y += fall_speed

    def is_clicked(self, pos):
        return (self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2 < bubble_radius ** 2

# Initialize game variables
bubbles = []
spawn_time = pygame.time.get_ticks()

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for bubble in bubbles:
                if bubble.is_clicked(pos):
                    bubble.taps -= 1
                    if bubble.taps == 0:
                        score += 100 * bubble.initial_taps  # Use initial taps for scoring
                        bubbles_burst += 1  # Increment bubbles burst count
                        bubbles.remove(bubble)

    # Bubble spawning
    if pygame.time.get_ticks() - spawn_time > 1000:  # Spawn every second
        bubbles.append(Bubble())
        bubbles_generated += 1  # Increment bubbles generated count
        spawn_time = pygame.time.get_ticks()

    # Update bubbles
    for bubble in bubbles:
        bubble.fall()
        bubble.draw()
        if bubble.y - bubble_radius > SCREEN_HEIGHT:  # If bubble reaches the bottom
            missed_bubbles += 1
            bubbles.remove(bubble)
            if missed_bubbles >= 3:  # Game over condition
                running = False  # End game

    # Display score and missed bubbles count
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    missed_text = font.render(f"Missed Bubbles: {missed_bubbles}", True, BLACK)
    screen.blit(missed_text, (10, 50))

    # Refresh the screen
    pygame.display.flip()
    pygame.time.delay(10)

# Display Game Over Message
screen.fill(WHITE)
game_over_text = font.render("Game Over", True, BLACK)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
final_score_text = font.render(f"Final Score: {score}", True, BLACK)
screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
pygame.display.flip()
pygame.time.wait(2000)

# Plotting the graph
plt.figure(figsize=(8, 6))
plt.bar(['Bubbles Burst', 'Bubbles Generated'], [bubbles_burst, bubbles_generated], color=['blue', 'green'])
plt.xlabel("Bubble Actions")
plt.ylabel("Count")
plt.title("Bubble Game Summary")
plt.show()

# Quit pygame
pygame.quit()
sys.exit()
