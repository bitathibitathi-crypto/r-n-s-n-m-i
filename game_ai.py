import pygame
import random
from collections import deque

# --- CẤU HÌNH ---
WIDTH, HEIGHT = 1600, 900
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 1000 # Để tốc độ vừa phải để quan sát AI, hoặc 1000 nếu muốn chạy cực nhanh

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
        pygame.display.set_caption("Snake AI: BFS Mode")
        self.clock = pygame.time.Clock()
        self.font_main = pygame.font.SysFont('Arial', 100, bold=True)
        self.font_sub = pygame.font.SysFont('Arial', 50)
        self.best_score = best_score
        
        # --- LOAD ẢNH (Giống game_basic) ---
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
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
        self.head = self.snake[0]
        self.food = self.spawn_food()
        self.score = 0
        self.direction = "right" # Mặc định để xoay đầu ảnh
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
        obstacles = self.snake[:-1]
        path = self.get_bfs_path(self.head, self.food, obstacles)
        next_move = None
        
        if path:
            next_move = path[0]
            # Xác định hướng đi mới để xoay đầu ảnh
            if next_move[1] < self.head[1]: self.direction = "up"
            elif next_move[1] > self.head[1]: self.direction = "down"
            elif next_move[0] < self.head[0]: self.direction = "left"
            elif next_move[0] > self.head[0]: self.direction = "right"
        else:
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
                self.best_score = max(self.score, self.best_score)
                self.food = self.spawn_food()
            else:
                self.snake.pop()
        else:
            self.game_over = True

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

        # Vẽ rắn (Xoay đầu ảnh)
        for i, (x, y) in enumerate(self.snake):
            pos = (x * CELL_SIZE + 2, y * CELL_SIZE + 2)
            if self.head_img:
                if i == 0:
                    angles = {"up": 90, "down": 270, "left": 180, "right": 0}
                    rotated_head = pygame.transform.rotate(self.head_img, angles[self.direction])
                    self.screen.blit(rotated_head, pos)
                else:
                    self.screen.blit(self.body_img, pos)
            else:
                color = BLUE if i == 0 else GREEN
                pygame.draw.rect(self.screen, color, (pos[0], pos[1], CELL_SIZE-4, CELL_SIZE-4))
        
        # Vẽ mồi
        pygame.draw.ellipse(self.screen, RED, (self.food[0]*CELL_SIZE+4, self.food[1]*CELL_SIZE+4, CELL_SIZE-8, CELL_SIZE-8))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0,0))
            msg = self.font_main.render("GAME OVER", True, WHITE)
            score_txt = self.font_sub.render(f"Score: {self.score} | Best: {self.best_score}", True, WHITE)
            retry = self.font_sub.render("SPACE: Restart | ESC: Menu", True, WHITE)
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 150))
            self.screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2))
            self.screen.blit(retry, (WIDTH//2 - retry.get_width()//2, HEIGHT//2 + 100))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # Thoát bất kỳ lúc nào để về main.py
                        running = False
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset()
            if not self.game_over:
                self.play_step()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        return self.best_score # Trả về điểm cho main.py

def start_game(best_score=0):
    game = SnakeGameAI(best_score)
    return game.run()
