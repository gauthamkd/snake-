import pygame, random

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)

START_SPEED = 5        # starting moves per second (change this to taste)
FRUITS_PER_LEVEL = 2   # speed goes up by 1 after this many fruits

def restart_game():
    snake = [(200, 200)]
    direction = (20, 0)
    food = (random.randrange(20, 380, 20), random.randrange(20, 380, 20))
    score = 0
    speed = START_SPEED
    return snake, direction, food, score, speed

snake, direction, food, score, speed = restart_game()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_y:
                    snake, direction, food, score, speed = restart_game()
                    game_over = False
                elif event.key == pygame.K_n:
                    running = False
            else:
                if event.key == pygame.K_UP and direction != (0, 20):
                    direction = (0, -20)
                elif event.key == pygame.K_DOWN and direction != (0, -20):
                    direction = (0, 20)
                elif event.key == pygame.K_LEFT and direction != (20, 0):
                    direction = (-20, 0)
                elif event.key == pygame.K_RIGHT and direction != (-20, 0):
                    direction = (20, 0)

    if not running:
        break

    if not game_over:
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (head[0] <= 0 or head[0] >= 380 or
            head[1] <= 0 or head[1] >= 380 or
            head in snake[:-1]):
            game_over = True
        else:
            snake.insert(0, head)

            if head == food:
                score += 1
                speed = START_SPEED + score // FRUITS_PER_LEVEL  # +1 speed every 2 fruits

                while True:
                    food = (random.randrange(20, 380, 20), random.randrange(20, 380, 20))
                    if food not in snake:
                        break
            else:
                snake.pop()

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 400, 400), 4)

    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, 20, 20))

    pygame.draw.rect(screen, (255, 0, 0), (*food, 20, 20))

    # Scoreboard
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    speed_text = small_font.render("Speed: " + str(speed) + " moves/sec", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(speed_text, (10, 40))

    if game_over:
        pygame.draw.rect(screen, (30, 30, 30), (15, 145, 370, 110))
        title = font.render("GAME OVER!", True, (255, 60, 60))
        message = small_font.render("Do you want to restart?", True, (255, 255, 255))
        options = small_font.render("Press Y = Yes     Press N = No", True, (255, 220, 0))
        screen.blit(title, title.get_rect(center=(200, 170)))
        screen.blit(message, message.get_rect(center=(200, 205)))
        screen.blit(options, options.get_rect(center=(200, 235)))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()