import pygame
import time
import random

pygame.font.init()

# Constants
m = '0'  # Default high score if the file is empty
SW = 10
SH = 20
SV = 2
PW = 50  
PH = 60  
PV = 2
W, H = 1080, 720

# Reading the high score from the file
try:
    with open('score.txt', 'r') as r:
        l = r.readlines()
        if l:
            m = l[-1].strip()  # Get the last line and strip any extra whitespace/newlines
except FileNotFoundError:
    pass  # If the file doesn't exist, keep default high score as 0

# Initialize Window and Font
WIN = pygame.display.set_mode((W, H))
pygame.display.set_caption('Pypro')
F = pygame.font.SysFont("Arial Bold", 40)
BG = pygame.transform.scale(pygame.image.load('s.jpg'), (W, H))
c = pygame.time.Clock()

# Drawing function
def drawing(player, elapsed, stars):
    WIN.blit(BG, (0, 0))
    tt = F.render(f"Elapsed time: {round(elapsed)}s", 1, 'white')
    WIN.blit(tt, (0, 0))
    pygame.draw.rect(WIN, 'red', player)
    for star in stars:
        pygame.draw.rect(WIN, "green", star)
    
    # Display current high score
    hs2 = F.render(f"Current high score: {m}", 1, 'white')
    WIN.blit(hs2, (0, H - hs2.get_height()))  # Corrected the positioning
    
    pygame.display.update()

# Game over screen handler
def game_over(elapsed):
    run = True
    while run:
        lost_text = F.render(f"You Lost! Press 'R' to Restart. You survived: {round(elapsed)}s", 1, 'white')
        WIN.blit(lost_text, (W / 2 - lost_text.get_width() / 2, H / 2 - lost_text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart on 'R' key press
                    main()

# Main game loop
def main():
    global m  # Access the high score outside the main function
    player = pygame.Rect(540, H - PH, PW, PH)
    sai = 2000
    sc = 0
    stars = []
    run = True
    start = time.time()
    hit = False  # Initialize the hit flag
    
    while run:
        # Frame control
        c.tick(144)
        sc += c.get_time()  # Adds time in milliseconds
        
        # Star generation
        if sc > sai and not hit:
            for _ in range(3):
                sx = random.randint(0, W - SW)
                star = pygame.Rect(sx, -SH, SW, SH)
                stars.append(star)
            sai = max(200, sai - 50)
            sc = 0
        
        elapsed = time.time() - start
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        
        # Player movement (only if not hit)
        if not hit:
            if keys[pygame.K_a] and player.x - PV > 0:
                player.x -= PV
            if keys[pygame.K_d] and player.x + PV < W - PW:
                player.x += PV
        
        # Star movement and collision
        if not hit:  # Only move stars if not hit
            for star in stars[:]:
                star.y += SV
                if star.y > H:
                    stars.remove(star)
                elif star.colliderect(player):
                    stars.remove(star)
                    hit = True
                    break
        
        # Check for loss and display game over
        if hit:
            # Update high score if the player survived longer than the current high score
            if elapsed > float(m):
                m = str(round(elapsed))  # Update high score and convert it to string
                with open('score.txt', 'a') as f:
                    f.write(f"{m}\n")  # Write the new high score to the file

            game_over(elapsed)
        
        # Draw everything
        if not hit:
            drawing(player, elapsed, stars)
    
    pygame.quit()

if __name__ == "__main__":
    main()
