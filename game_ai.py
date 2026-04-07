import pygame
import random
from collections import deque

# --- CẤU HÌNH ---
WIDTH, HEIGHT = 1600, 900
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 1000 # Tăng tốc độ để xem AI chạy

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
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
        self.head = self.snake[0]
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if food not in self.snake:
                return food

    def get_bfs_path(self, start, target, obstacles):
        queue = deque([start])
        visited = {start: None}

        while queue:
            current = queue.popleft()
            if current == target:
                path = []
                while current in visited and visited[current] is not None:
                    path.append(current)
                    current = visited[current]
                return path[::-1]

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                next_node = (current[0] + dx, current[1] + dy)
                if (0 <= next_node[0] < COLS and 0 <= next_node[1] < ROWS and 
                    next_node not in visited and next_node not in obstacles):
                    visited[next_node] = current
                    queue.append(next_node)
        return None

    def play_step(self):
        # BFS tìm đường
        obstacles = self.snake[:-1]
        path = self.get_bfs_path(self.head, self.food, obstacles)

        next_move = None
        if path:
            next_move = path[0]
        else:
            # Nếu mù, thử đi vào ô trống bất kỳ lân cận
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                temp = (self.head[0] + dx, self.head[1] + dy)
                if (0 <= temp[0] < COLS and 0 <= temp[1] < ROWS and temp not in self.snake):
                    next_move = temp
                    break

        if next_move:
            self.head = next_move
            self.snake.insert(0, self.head)
            if self.head == self.food:
                self.score += 1
                if self.score > self.best_score:
                    self.best_score = self.score
                self.food = self.spawn_food()
            else:
                self.snake.pop()
        else:
            self.game_over = True

        # Check va chạm
        if (self.head[0] < 0 or self.head[0] >= COLS or 
            self.head[1] < 0 or self.head[1] >= ROWS or 
            self.head in self.snake[1:]):
            self.game_over = True

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Bắt sự kiện phím Space để chơi lại hoặc tab để thoát
                if event.type == pygame.KEYDOWN:
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