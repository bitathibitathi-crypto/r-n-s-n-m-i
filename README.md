Dự án Rắn Săn Mồi (Snake Game) của bạn thực sự rất ấn tượng! Việc kết hợp giao diện quản lý người dùng bằng PyQt6 với engine xử lý game bằng Pygame, cộng thêm thuật toán AI (BFS) và thiết kế màn chơi đa dạng cho thấy sự đầu tư rất tỉ mỉ. 

Dưới đây là bản mô tả chi tiết (file `README.md`) được thiết kế chuẩn mực, rõ ràng và đầy đủ thông tin để bạn đưa lên GitHub hoặc lưu trữ cho dự án.

***

# 🐍 Trò Chơi Rắn Săn Mồi Đa Chế Độ (Multi-mode Snake Game & AI)

> Một phiên bản nâng cấp toàn diện của tựa game Rắn Săn Mồi kinh điển. Dự án này được xây dựng bằng Python, tích hợp hệ thống quản lý tài khoản qua giao diện PyQt6, lưu trữ kỷ lục cá nhân và bao gồm 3 chế độ chơi riêng biệt: Cơ bản, Vượt chướng ngại vật (Hardcore), và AI tự động chơi (Sử dụng thuật toán BFS).

## 🌟 Tính Năng Nổi Bật

* **Hệ thống Tài khoản Cá nhân:** Đăng nhập, đăng ký và quản lý người dùng bằng giao diện đồ họa hiện đại.
* **Lưu trữ Kỷ lục (Highscores):** Điểm cao nhất của từng chế độ được lưu trữ cục bộ dưới dạng file `.txt` riêng biệt cho mỗi tài khoản.
* **Đa dạng Chế độ chơi:** Cung cấp trải nghiệm từ thư giãn đến thử thách cực đại, hoặc đơn giản là ngồi xem máy chơi.
* **Thuật toán Trí tuệ Nhân tạo:** AI sử dụng thuật toán Tìm kiếm theo chiều rộng (BFS - Breadth-First Search) để tính toán đường đi ngắn nhất đến thức ăn và tránh vật cản.
* **Thiết kế Màn chơi Hardcore:** 5 cấp độ khó với kiến trúc vật cản phức tạp như Khung giam, Zig-zag, Bãi mìn.

---

## 📂 Cấu Trúc Dự Án

Dự án được chia thành các module độc lập giúp dễ dàng bảo trì và phát triển:

| Tên File | Vai trò & Chức năng chính |
| :--- | :--- |
| `main.py` | Cốt lõi giao diện người dùng (GUI) bằng PyQt6. Xử lý Đăng nhập/Đăng ký, Menu chọn chế độ và xem Điểm cao. |
| `game_basic.py` | Chế độ rắn săn mồi truyền thống. Tập trung vào cơ chế cốt lõi: di chuyển, ăn mồi, tăng độ dài và tính điểm. |
| `game_obstacles.py` | Chế độ Hardcore. Tích hợp menu chọn 5 màn chơi với các hệ thống vật cản (obstacles) logic và phức tạp. |
| `game_ai.py` | Chế độ AI. Máy tự động chơi bằng cách áp dụng thuật toán BFS để quét bản đồ, tìm đường đi tối ưu đến vị trí thức ăn. |
| `users.txt` | File dữ liệu (tự động tạo) lưu trữ thông tin Đăng nhập/Mật khẩu của người chơi. |
| `[username]_scores.txt` | File dữ liệu (tự động tạo) lưu trữ điểm kỷ lục của từng người chơi theo các chế độ tương ứng. |

---

## ⚙️ Yêu Cầu Hệ Thống & Cài Đặt

Để chạy được tựa game này, máy tính của bạn cần cài đặt Python 3.x và các thư viện hỗ trợ đồ họa.

**Bước 1: Clone dự án về máy**
Tải toàn bộ mã nguồn về thư mục cục bộ của bạn.

**Bước 2: Cài đặt các thư viện cần thiết**
Mở Terminal hoặc Command Prompt và chạy lệnh sau:
```bash
pip install pygame PyQt6
```

**Bước 3: Khởi động game**
Chạy file giao diện chính để bắt đầu trò chơi:
```bash
python main.py
```

---

## 🎮 Hướng Dẫn Chơi & Các Chế Độ

### 1. Chế Độ Cơ Bản (Basic Mode)
Luật chơi kinh điển. Tránh đụng vào tường và đuôi của chính mình.
* **Phím Mũi tên (Lên/Xuống/Trái/Phải):** Điều hướng hướng đi của rắn.
* **SPACE:** Chơi lại khi Game Over.
* **ESC:** Thoát game và quay về Menu giao diện.

### 2. Chế Độ Vật Cản (Hardcore Obstacles)
Chế độ này có một Menu riêng bên trong Pygame. Bạn cần chọn màn chơi trước khi bắt đầu.
* **Phím 1 đến 5:** Chọn cấp độ tương ứng (Màn 1: Khung giam, Màn 2: 9 Căn phòng, Màn 3: Zig-zag, Màn 4: Pháo đài, Màn 5: Bãi mìn).
* **Phím Mũi tên:** Điều khiển rắn né tránh vật cản (màu xám), tường và thân rắn.
* **TAB:** Quay lại Menu chọn màn chơi của Pygame.
* **ESC:** Thoát hoàn toàn về Menu chính của PyQt6.

### 3. Chế Độ Trí Tuệ Nhân Tạo (AI Mode)
Chế độ rảnh tay. AI sẽ tự động phân tích bản đồ và tìm đường ngắn nhất tới mồi. Game được thiết lập ở mức FPS rất cao (1000) để bạn quan sát tốc độ xử lý của thuật toán.
* **SPACE:** Khởi động lại AI khi bị Game Over (Trong trường hợp "mù đường" không thể tìm lối thoát).
* **ESC:** Trở về Menu chính.

---

## 🧠 Phía Sau Các Dòng Code (Cơ Chế Hoạt Động)

* **Giao diện PyQt6:** Sử dụng `QDialog` và `QWidget` kết hợp với StyleSheet (CSS) để tạo giao diện phẳng, màu sắc xanh lá đặc trưng của game Rắn. Cơ chế vòng lặp `while True` trong hàm `handle_login` giúp game liền mạch, tự động quay lại Menu chọn chế độ sau khi tắt màn hình Pygame.
* **Thuật toán BFS (Breadth-First Search):** Trong file `game_ai.py`, hàm `get_bfs_path` sử dụng cấu trúc hàng đợi kép `deque` để quét các ô lân cận. Nó mô phỏng việc lan rộng ra tứ phía để tìm đường ngắn nhất mà không bị đi xuyên qua vật cản là chính thân con rắn `self.snake[:-1]`.
* **Tối ưu Frame Rate:** Sử dụng `pygame.time.Clock().tick(FPS)` để giới hạn số khung hình, đảm bảo tốc độ game nhất quán ở mọi cấu hình máy tính. File AI có FPS cao để minh họa tính toán, trong khi file Basic giới hạn ở mức có thể điều khiển bằng tay.

---
> **Lưu ý:** Các file dữ liệu người dùng (`users.txt` và file điểm cao) lưu mật khẩu ở dạng văn bản thuần túy (plain text) để dễ dàng kiểm tra phục vụ mục đích học tập.
