import pygame
import random
from collections import deque

# --- CẤU HÌNH ---
WIDTH, HEIGHT = 1590, 900
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 100 

# Màu sắc
WHITE = (220, 220, 220)
BLACK = (15, 15, 15)
RED = (255, 60, 60)
GREEN = (40, 200, 80)
BLUE = (0, 150, 255)
GRAY = (100, 100, 100)

class SnakeGameAI:
    def __init__(self, best_score=0):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game - Basic Mode")
        self.clock = pygame.time.Clock()
        self.font_main = pygame.font.SysFont('Arial', 100, bold=True)
        self.font_sub = pygame.font.SysFont('Arial', 50) 
        self.best_score = best_score
        
        # --- LOAD ẢNH ---
        try:
            self.head_img = pygame.image.load('snake_head.png').convert_alpha()
            self.body_img = pygame.image.load('snake_body.png').convert_alpha()
            self.head_img = pygame.transform.scale(self.head_img, (CELL_SIZE-2, CELL_SIZE-2))
            self.body_img = pygame.transform.scale(self.body_img, (CELL_SIZE-2, CELL_SIZE-2))
        except:
            self.head_img = None 
            print("Cảnh báo: Không tìm thấy file ảnh!")

        self.reset()

    def reset(self):
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2)]
        self.food = self.spawn_food()
        self.score = 0
        self.direction = "right"
        self.last_direction = "right"
        self.game_over = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if food not in self.snake:
                return food

    def play_step(self):
        if not self.game_over:
            self.last_direction = self.direction
            head_x, head_y = self.snake[0]

            if self.direction == "up": head_y -= 1
            elif self.direction == "down": head_y += 1
            elif self.direction == "left": head_x -= 1
            elif self.direction == "right": head_x += 1
            
            if head_x < 0 or head_x >= COLS or head_y < 0 or head_y >= ROWS or (head_x, head_y) in self.snake:
                self.game_over = True
                self.best_score = max(self.score, self.best_score)
                return

            self.snake.insert(0, (head_x, head_y))
            if (head_x, head_y) == self.food:
                self.score += 1
                self.food = self.spawn_food()
            else:
                self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)
        
        # Vẽ lưới ẩn
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (25, 25, 25), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (25, 25, 25), (0, y), (WIDTH, y))

        # Vẽ rắn
        for i, (x, y) in enumerate(self.snake):
            pos = (x * CELL_SIZE + 2, y * CELL_SIZE + 2)
            if self.head_img:
                if i == 0: # Nếu là đầu thì xoay ảnh
                    # Pygame xoay ngược chiều kim đồng hồ, nên Up=90, Left=180, Down=270, Right=0
                    angles = {"up": 90, "down": 270, "left": 180, "right": 0}
                    rotated_head = pygame.transform.rotate(self.head_img, angles[self.direction])
                    self.screen.blit(rotated_head, pos)
                else:
                    self.screen.blit(self.body_img, pos)
            else:
                color = GREEN if i == 0 else BLUE
                pygame.draw.rect(self.screen, color, (pos[0], pos[1], CELL_SIZE-4, CELL_SIZE-4))

        # Vẽ mồi
        pygame.draw.ellipse(self.screen, RED, (self.food[0]*CELL_SIZE+4, self.food[1]*CELL_SIZE+4, CELL_SIZE-8, CELL_SIZE-8))

        # Giao diện Game Over
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0,0))
            
            msg = self.font_main.render("GAME OVER", True, WHITE)
            score_txt = self.font_sub.render(f"Score: {self.score} | Best: {self.best_score}", True, WHITE)
            retry = self.font_sub.render("SPACE: Restart | ESC: Menu", True, (200, 200, 200))
            
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 100))
            self.screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2 + 20))
            self.screen.blit(retry, (WIDTH//2 - retry.get_width()//2, HEIGHT//2 + 100))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_UP and self.last_direction != "down": self.direction = "up"
                        elif event.key == pygame.K_DOWN and self.last_direction != "up": self.direction = "down"
                        elif event.key == pygame.K_LEFT and self.last_direction != "right": self.direction = "left"
                        elif event.key == pygame.K_RIGHT and self.last_direction != "left": self.direction = "right"
                    
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset()

            if not self.game_over:
                self.play_step()
            
            self.draw()
            self.clock.tick(15 + self.score // 5)
        
        pygame.quit()
        return self.best_score

def start_game(best_score=0):
    game = SnakeGameAI(best_score)
    return game.run()
