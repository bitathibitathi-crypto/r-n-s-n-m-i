import sys
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QDialog, QFrame
)
from PyQt6.QtCore import Qt
# Import các hàm từ các file game của bạn
# Đảm bảo các file này có hàm def start_game():
try:
    from game_basic import start_game as run_basic
    from game_obstacles import start_game as run_obstacles
    from game_ai import start_game as run_ai
except ImportError:
    # Tạo hàm giả lập nếu bạn chưa có file để tránh lỗi crash ngay lập tức
    def run_basic(): print("Chạy game cơ bản")
    def run_obstacles(): print("Chạy game vật cản")
    def run_ai(): print("Chạy game AI")

FILE_NAME = os.path.join(BASE_DIR, "users.txt")
SCORE_FILE = os.path.join(BASE_DIR, "highscores.txt")

# --- Khởi tạo dữ liệu ---
if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w").close()

if not os.path.exists(SCORE_FILE):
    with open(SCORE_FILE, "w") as f:
        f.write("basic|0\nobstacles|0\nai|0")

def load_users():
    users = {}
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            for line in f:
                line = line.strip()
                if "|" in line:
                    u, p = line.split("|")
                    users[u] = p
    return users

def save_user(u, p):
    with open(FILE_NAME, "a") as f:
        f.write(f"{u}|{p}\n")

# Sửa lại hàm lấy điểm để nhận vào tên người dùng
def get_scores(username):
    # Tạo tên file riêng cho từng user
    user_score_file = os.path.join(BASE_DIR, f"{username}_scores.txt")
    
    scores = {"basic": "0", "obstacles": "0", "ai": "0"}
    
    if os.path.exists(user_score_file):
        try:
            with open(user_score_file, "r") as f:
                for line in f:
                    if "|" in line:
                        mode, score = line.strip().split("|")
                        scores[mode] = score
        except:
            pass
    return scores

# Bạn cũng nên có hàm để lưu điểm riêng cho từng user sau này
def save_score(username, mode, score):
    user_score_file = os.path.join(BASE_DIR, f"{username}_scores.txt")
    scores = get_scores(username)
    scores[mode] = str(score)
    
    with open(user_score_file, "w") as f:
        for m, s in scores.items():
            f.write(f"{m}|{s}\n")

# --- Giao diện (CSS) ---
STYLESHEET = """
    QWidget {
        background-color: #2E7D32;
        color: white;
        font-family: "Segoe UI", sans-serif;
        font-size: 14px;
    }
    QLabel {
        font-weight: bold;
        color: #C8E6C9;
    }
    QLineEdit {
        background-color: #C8E6C9;
        color: #1B5E20;
        border: 2px solid #1B5E20;
        border-radius: 5px;
        padding: 8px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    QPushButton:hover { background-color: #66BB6A; }
"""

# --- Các Lớp Giao Diện ---

class HighScoreDialog(QDialog):
    def __init__(self, username): # Nhận thêm username
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Kỷ Lục của {username}")
        self.setFixedSize(300, 250)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout()
        title = QLabel(f"🏆 KỶ LỤC: {username}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; color: #FFD700; margin-bottom: 10px;")
        layout.addWidget(title)

        # Lấy điểm riêng của user này
        scores = get_scores(self.username)
        mapping = {"basic": "Cơ bản", "obstacles": "Vật cản", "ai": "Máy chơi"}
        
        for key, name in mapping.items():
            s = scores.get(key, "0")
            lbl = QLabel(f"{name}: {s} điểm")
            lbl.setStyleSheet("font-size: 16px; margin-bottom: 5px;")
            layout.addWidget(lbl)

        btn_close = QPushButton("Đóng")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        self.setLayout(layout)

class RegisterWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Đăng ký tài khoản")
        self.setFixedSize(350, 300)
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("ĐĂNG KÝ MỚI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.u_reg = QLineEdit(placeholderText="Tên đăng nhập")
        self.p_reg = QLineEdit(placeholderText="Mật khẩu")
        self.p_reg.setEchoMode(QLineEdit.EchoMode.Password)
        
        btn_submit = QPushButton("Xác nhận Đăng ký")
        btn_back = QPushButton("Quay lại")
        btn_back.setStyleSheet("background-color: #757575;")

        layout.addWidget(title)
        layout.addWidget(self.u_reg)
        layout.addWidget(self.p_reg)
        layout.addWidget(btn_submit)
        layout.addWidget(btn_back)
        self.setLayout(layout)

        btn_submit.clicked.connect(self.process_registration)
        btn_back.clicked.connect(self.close)

    def process_registration(self):
        u, p = self.u_reg.text(), self.p_reg.text()
        if not u or not p:
            QMessageBox.warning(self, "Lỗi", "Không được để trống!")
            return
        
        users = load_users()
        if u in users:
            QMessageBox.warning(self, "Lỗi", "Tài khoản đã tồn tại!")
        else:
            save_user(u, p)
            QMessageBox.information(self, "Thành công", "Đăng ký hoàn tất!")
            self.close()

    def closeEvent(self, event):
        self.login_window.show() # Hiện lại màn hình login khi đóng
        event.accept()

class ModeSelectionDialog(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username=username
        self.selected_mode = None
        self.setWindowTitle("Chọn chế độ")
        self.setFixedSize(350, 430)
        self.setStyleSheet(STYLESHEET)
        
        layout = QVBoxLayout()
        
        welcome = QLabel(f"Xin Chào, {username}!")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("font-size: 18px; color: #FFD700;")
        layout.addWidget(welcome)
        welcome2 = QLabel(f"Hãy chọn chế độ chơi!")
        welcome2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome2.setStyleSheet("font-size: 20px; color: #FFD700;")
        layout.addWidget(welcome2)
        modes = [
            ("🐍 Chế độ Cơ bản", "basic"),
            ("🧱 Chế độ Vật cản", "obstacles"),
            ("🤖 Chế độ AI", "ai")
        ]

        for text, m_id in modes:
            btn = QPushButton(text)
            btn.setFixedHeight(45)
            btn.clicked.connect(lambda checked, m=m_id: self.set_mode(m))
            layout.addWidget(btn)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #C8E6C9;")
        layout.addWidget(line)

        btn_score = QPushButton("🏆 XEM KỶ LỤC")
        btn_score.setStyleSheet("background-color: #FBC02D; color: #1B5E20;")
        btn_score.clicked.connect(self.open_scores)
        layout.addWidget(btn_score)

        btn_logout = QPushButton("🚪 Đăng xuất")
        btn_logout.setStyleSheet("background-color: #D32F2F; color: white;")
        btn_logout.clicked.connect(self.reject)
        layout.addWidget(btn_logout)

        self.setLayout(layout)

    def set_mode(self, mode):
        self.selected_mode = mode
        self.accept()

    def open_scores(self):
        score_dialog = HighScoreDialog(self.username)
        score_dialog.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            pass # Vô hiệu hóa phím ESC để bảng không bị đóng khi người dùng lỡ bấm
        else:
            super().keyPressEvent(event)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake Game - Login")
        self.setFixedSize(350, 320)
        self.setStyleSheet(STYLESHEET)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("SNAKE GAME LOGIN")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username = QLineEdit(placeholderText="Tên đăng nhập")
        self.password = QLineEdit(placeholderText="Mật khẩu")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        btn_login = QPushButton("Đăng nhập")
        btn_reg = QPushButton("Đăng ký tài khoản")
        btn_reg.setStyleSheet("background-color: #1976D2;")

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(btn_login)
        layout.addWidget(btn_reg)
        self.setLayout(layout)

        btn_login.clicked.connect(self.handle_login)
        btn_reg.clicked.connect(self.open_register)

    def closeEvent(self, event):
        QApplication.quit()

    def open_register(self):
        self.hide()
        self.reg_win = RegisterWindow(self)
        self.reg_win.show()

    def handle_login(self):
        users = load_users()
        u = self.username.text()
        p = self.password.text()

        if u in users and users[u] == p:
            self.hide() 
            
            # Vòng lặp để sau khi chơi xong quay lại Menu
            while True:
                mode_dialog = ModeSelectionDialog(u)
                if mode_dialog.exec():
                    chosen_mode = mode_dialog.selected_mode
                    
                    scores = get_scores(u)
                    current_best = int(scores.get(chosen_mode, 0))
                    
                    new_best = 0
                    if chosen_mode == "basic":
                        new_best = run_basic(current_best) # Khi nhấn ESC, hàm này kết thúc và chạy tiếp vòng lặp while
                    elif chosen_mode == "obstacles":
                        new_best = run_obstacles(current_best)
                    elif chosen_mode == "ai":
                        new_best = run_ai(current_best)
                        
                    if new_best is not None and new_best > current_best:
                        save_score(u, chosen_mode, new_best)
                else:
                    # Nếu nhấn Đăng xuất hoặc X thì quay lại màn hình Login
                    self.username.clear()
                    self.password.clear()
                    self.show()
                    break
        else:
            QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())
