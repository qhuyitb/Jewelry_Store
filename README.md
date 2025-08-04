# 🛍️ Jewelry Store

Jewelry Store là một ứng dụng web mô phỏng cửa hàng trực tuyến, giúp quản lý sản phẩm, đơn hàng, người dùng và thanh toán. Được xây dựng bằng **Flask (Python)**.

---

## 🚀 Tính năng chính
- 🛡️ Phân quyền người dùng (user / admin) và bảo vệ route quản trị
- 🧾 Quản lý sản phẩm (thêm, sửa, xóa)
- 🛒 Giỏ hàng và đặt hàng
- 👤 Đăng ký / đăng nhập / mã hóa mật khẩu (`bcrypt`)
- ✉️ Gửi email xác nhận đơn hàng / xác minh tài khoản (`Flask-Mail`)
- 💳 Tích hợp thanh toán qua `Stripe`
- 👨‍💼 Giao diện quản trị đơn giản

---

## 🛠️ Công nghệ sử dụng

| Thành phần     | Mô tả |
|----------------|------|
| Flask          | Web Framework |
| SQLAlchemy     | ORM cho Python |
| Microsoft SQL Server     | Hệ quản trị cơ sở dữ liệu chính |
| Flask-WTF      | Hỗ trợ xử lý form |
| Flask-Mail     | Gửi email SMTP |
| Flask-Login    | Quản lý phiên đăng nhập |
| bcrypt         | Mã hóa mật khẩu người dùng |
| Stripe         | Thanh toán trực tuyến |
| Ngrok          | Tạo public URL cho local server |
| HTML/CSS/JS    | Giao diện người dùng (Bootstrap) |

---
## ⚙️ Cài đặt nhanh

```bash
# Clone project
git clone https://github.com/yourusername/Mini_Store.git
cd Mini_Store

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Cài đặt thư viện
pip install -r requirements.txt

# Tạo file cấu hình .env (xem phần dưới)
# Chạy ứng dụng
python run.py
