import pygame
import random

# --- CẤU HÌNH ---
WIDTH, HEIGHT = 1590, 900
CELL_SIZE = 30
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 120 

# Màu sắc
WHITE = (220, 220, 220)
BLACK = (15, 15, 15)
RED = (255, 60, 60)
GREEN = (40, 200, 80)
BLUE = (0, 150, 255)
GRAY = (80, 80, 80)

class SnakeGame:
    def __init__(self, best_score=0):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game: Hardcore Levels")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('Arial', 80, bold=True)
        self.font_main = pygame.font.SysFont('Arial', 100, bold=True)
        self.font_sub = pygame.font.SysFont('Arial', 40)
        
        self.best_score = best_score
        self.state = "MENU"
        self.current_level = 1
        self.obstacles = []
        
    def load_level(self, level):
        """Định nghĩa vật cản cho 5 màn chơi khó"""
        self.obstacles = []
        
        if level == 1:
            # Màn 1: Khung giam (The Ring) - Một vòng tường lớn bao quanh với 4 cửa ra
            for x in range(10, COLS - 10):
                self.obstacles.extend([(x, 8), (x, ROWS - 9)])
            for y in range(8, ROWS - 8):
                self.obstacles.extend([(10, y), (COLS - 11, y)])
            # Đục lỗ (tạo cửa)
            for x in range(COLS//2 - 2, COLS//2 + 3):
                if (x, 8) in self.obstacles: self.obstacles.remove((x, 8))
                if (x, ROWS - 9) in self.obstacles: self.obstacles.remove((x, ROWS - 9))
            for y in range(ROWS//2 - 2, ROWS//2 + 3):
                if (10, y) in self.obstacles: self.obstacles.remove((10, y))
                if (COLS - 11, y) in self.obstacles: self.obstacles.remove((COLS - 11, y))

        elif level == 2:
            # Màn 2: 9 Căn phòng (Tic-Tac-Toe) - Chia lưới thành 9 ô, chỉ có kẽ hở nhỏ
            for x in [COLS//3, 2*COLS//3]:
                for y in range(ROWS):
                    if y not in range(ROWS//2 - 3, ROWS//2 + 4) and y not in [3, ROWS-4]:
                        self.obstacles.append((x, y))
            for y in [ROWS//3, 2*ROWS//3]:
                for x in range(COLS):
                    if x not in range(COLS//2 - 3, COLS//2 + 4) and x not in [4, COLS-5]:
                        self.obstacles.append((x, y))

        elif level == 3:
            # Màn 3: Răng cưa (Zig-Zag Teeth) - Buộc phải lạng lách liên tục
            for i in range(1, 5):
                x = i * (COLS // 5)
                if i % 2 == 1:
                    # Tường cắm từ trên xuống
                    for y in range(0, ROWS - 8):
                        self.obstacles.append((x, y))
                else:
                    # Tường cắm từ dưới lên
                    for y in range(8, ROWS):
                        self.obstacles.append((x, y))

        elif level == 4:
            # Màn 4: Pháo đài kép (The Fortress) - 2 lớp hình vuông đồng tâm
            # Lớp ngoài
            for x in range(4, COLS - 4): self.obstacles.extend([(x, 4), (x, ROWS - 5)])
            for y in range(4, ROWS - 4): self.obstacles.extend([(4, y), (COLS - 5, y)])
            # Lớp trong
            for x in range(14, COLS - 14): self.obstacles.extend([(x, 10), (x, ROWS - 11)])
            for y in range(10, ROWS - 10): self.obstacles.extend([(14, y), (COLS - 15, y)])
            # Đục lỗ (Cửa ra vào chéo nhau)
            for y in range(ROWS//2 - 2, ROWS//2 + 2):
                 if (4, y) in self.obstacles: self.obstacles.remove((4, y))
                 if (COLS-5, y) in self.obstacles: self.obstacles.remove((COLS-5, y))
            for x in range(COLS//2 - 2, COLS//2 + 2):
                 if (x, 10) in self.obstacles: self.obstacles.remove((x, 10))
                 if (x, ROWS-11) in self.obstacles: self.obstacles.remove((x, ROWS-11))

        elif level == 5:
            # Màn 5: Bãi mìn (Minefield) - Vô số khối vuông rải rác khắp bản đồ
            for x in range(2, COLS - 2, 4):
                for y in range(2, ROWS - 2, 4):
                    self.obstacles.extend([(x, y), (x+1, y), (x, y+1), (x+1, y+1)])
            
            # Xóa các chướng ngại vật ở giữa để rắn có chỗ sinh ra an toàn
            center_safe_zone = [(cx, cy) for cx in range(COLS//2 - 4, COLS//2 + 4) for cy in range(ROWS//2 - 4, ROWS//2 + 4)]
            self.obstacles = [obs for obs in self.obstacles if obs not in center_safe_zone]

    def reset(self):
        self.load_level(self.current_level)
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
            if food not in self.snake and food not in self.obstacles:
                return food

    def play_step(self):
        if not self.game_over and self.frame_count % 6 == 0:
            self.last_direction = self.direction
            head_x, head_y = self.snake[0]

            if self.direction == "up": head_y -= 1
            elif self.direction == "down": head_y += 1
            elif self.direction == "left": head_x -= 1
            elif self.direction == "right": head_x += 1

            new_head = (head_x, head_y)

            # Check va chạm biên, thân rắn và tường
            if (head_x < 0 or head_x >= COLS or head_y < 0 or head_y >= ROWS or 
                new_head in self.snake or new_head in self.obstacles):
                self.game_over = True
                self.best_score = max(self.score, self.best_score)
                return

            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.score += 1
                self.food = self.spawn_food()
            else:
                self.snake.pop()

    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.font_title.render("HARDCORE SNAKE", True, RED)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        
        instructions = [
            "MÀN 1: Khung giam",
            "MÀN 2: 9 căn phòng",
            "MÀN 3: Zig-zag",
            "MÀN 4: Pháo đài",
            "MÀN 5: Bãi mìn (Siêu khó)"
        ]
        
        for i, text in enumerate(instructions):
            surf = self.font_sub.render(text, True, WHITE)
            self.screen.blit(surf, (WIDTH//2 - surf.get_width()//2, 300 + i * 70))
            
        best_surf = self.font_sub.render(f"Best Score: {self.best_score}", True, GREEN)
        self.screen.blit(best_surf, (WIDTH//2 - best_surf.get_width()//2, HEIGHT - 100))
        pygame.display.flip()

    def draw_game(self):
        self.screen.fill(BLACK)
        # # Vẽ lưới
        # for x in range(0, WIDTH, CELL_SIZE):
        #     pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, HEIGHT))
        # for y in range(0, HEIGHT, CELL_SIZE):
        #     pygame.draw.line(self.screen, (30, 30, 30), (0, y), (WIDTH, y))


        # Vẽ vật cản (Màu xám sáng hơn để dễ nhìn thấy mối nguy hiểm)
        for x, y in self.obstacles:
            pygame.draw.rect(self.screen, (130, 130, 130), (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
        
        # Vẽ rắn & mồi
        for i, (x, y) in enumerate(self.snake):
            color = BLUE if i == 0 else GREEN
            pygame.draw.rect(self.screen, color, (x*CELL_SIZE+2, y*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4))
        
        pygame.draw.ellipse(self.screen, RED, (self.food[0]*CELL_SIZE+4, self.food[1]*CELL_SIZE+4, CELL_SIZE-8, CELL_SIZE-8))

        # Hiển thị điểm
        score_txt = self.font_sub.render(f"Level: {self.current_level} | Score: {self.score}", True, WHITE)
        self.screen.blit(score_txt, (20, 20))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0,0))
            
            msg = self.font_main.render("GAME OVER", True, WHITE)
            retry = self.font_sub.render("SPACE: Restart | TAB: Menu", True, WHITE)
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 100))
            self.screen.blit(retry, (WIDTH//2 - retry.get_width()//2, HEIGHT//2 + 50))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            if self.state == "MENU":
                self.draw_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1: self.current_level = 1; self.state = "PLAYING"; self.reset()
                        if event.key == pygame.K_2: self.current_level = 2; self.state = "PLAYING"; self.reset()
                        if event.key == pygame.K_3: self.current_level = 3; self.state = "PLAYING"; self.reset()
                        if event.key == pygame.K_4: self.current_level = 4; self.state = "PLAYING"; self.reset()
                        if event.key == pygame.K_5: self.current_level = 5; self.state = "PLAYING"; self.reset()

            elif self.state == "PLAYING":
                self.frame_count += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.last_direction != "down": self.direction = "up"
                        if event.key == pygame.K_DOWN and self.last_direction != "up": self.direction = "down"
                        if event.key == pygame.K_LEFT and self.last_direction != "right": self.direction = "left"
                        if event.key == pygame.K_RIGHT and self.last_direction != "left": self.direction = "right"
                        if event.key == pygame.K_ESCAPE and self.game_over: running = False
                        if event.key == pygame.K_SPACE and self.game_over: self.reset()
                        if event.key == pygame.K_TAB: self.state = "MENU"

                self.play_step()
                self.draw_game()
                self.clock.tick(FPS)

        pygame.quit()

def start_game(best_score=0):
    game = SnakeGame(best_score)
    game.run()
    return max(game.best_score, game.score)