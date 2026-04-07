import pygame
import random
from collections import deque

# --- CẤU HÌNH ---
WIDTH, HEIGHT =1590, 900
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 198 # Tăng tốc độ để xem AI chạy

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
        pygame.display.set_caption("Snake AI: BFS Blind Mode (Space to Restart)")
        self.clock = pygame.time.Clock()
        self.font_main = pygame.font.SysFont('Arial', 100, bold=True)
        self.font_sub = pygame.font.SysFont('Arial', 50)
        self.best_score = best_score
        self.reset()

    def reset(self):
        """Khởi tạo lại toàn bộ trạng thái game"""
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2)]
        self.food = self.spawn_food()
        self.score = 0
        self.direction = "right"
        self.last_direction = "right"
        self.game_over = False
        self.frame_count = 0

    def spawn_food(self):
        while True:
            food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if food not in self.snake:
                return food

    def play_step(self):
        if not self.game_over and self.frame_count % 6 == 0:
            # Cập nhật hướng đi hiện tại trước khi di chuyển
            self.last_direction = self.direction

            # Di chuyển đầu rắn
            head_x, head_y = self.snake[0]

            if self.direction == "right":
                head_x += 1
            elif self.direction == "left":
                head_x -= 1
            elif self.direction == "up":
                head_y -= 1
            elif self.direction == "down":
                head_y += 1
            
            #check crash with edge
            if head_x < 0 or head_x >= COLS or head_y < 0 or head_y >= ROWS:
                self.game_over = True

            #check crash with body
            if (head_x, head_y) in self.snake[1:]: # Có thể tối ưu với dict/set O(1) 
                self.game_over = True

            #Update điểm cao nhất nếu ngỏm
            if self.game_over:
                self.best_score = max(self.score, self.best_score)
                return

            self.snake.insert(0, (head_x,head_y))

            # Kiểm tra ăn táo
            if (head_x, head_y) == self.food:
                self.score += 1
                self.food = self.spawn_food() # Táo mới
            else:
                self.snake.pop()

            

    def draw(self):
        self.screen.fill(BLACK)
        
        # Vẽ lưới
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (WIDTH, y))

        # Vẽ rắn & mồi
        for i, (x, y) in enumerate(self.snake):
            color = BLUE if i == 0 else GREEN
            pygame.draw.rect(self.screen, color, (x*CELL_SIZE+2, y*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4))
        
        pygame.draw.ellipse(self.screen, RED, (self.food[0]*CELL_SIZE+4, self.food[1]*CELL_SIZE+4, CELL_SIZE-8, CELL_SIZE-8))

        # Overlay khi Game Over
        if self.game_over:
            # Tạo hiệu ứng màn hình tối lại
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0,0))
            
            # Text thông báo
            msg = self.font_main.render("GAME OVER", True, WHITE)
            retry = self.font_sub.render("Press SPACE to Restart or ESC to Return to Menu", True, WHITE)
            score_txt = self.font_sub.render(f"Final Score: {self.score}", True, WHITE)
            
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 300))
            self.screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2-75))
            self.screen.blit(retry, (WIDTH//2 - retry.get_width()//2, HEIGHT//2 + 40))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.frame_count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Bắt sự kiện phím Space để chơi lại hoặc ESC để thoát
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.last_direction != "down":   #last_direction xử lý nhiều hướng trong 1 frame
                        self.direction = "up"
                    if event.key == pygame.K_DOWN and self.last_direction != "up":
                        self.direction = "down"
                    if event.key == pygame.K_LEFT and self.last_direction != "right":
                        self.direction = "left"
                    if event.key == pygame.K_RIGHT and self.last_direction != "left":
                        self.direction = "right"
                    if event.key == pygame.K_ESCAPE and self.game_over:
                        running = False
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset()

            if not self.game_over:
                self.play_step()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
def start_game(best_score=0):
    game = SnakeGameAI(best_score)
    game.run()
    return max(game.best_score, game.score)

