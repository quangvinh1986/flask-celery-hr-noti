# Lời mở đầu

## Chức năng 
Dự án này cho phép thực hiện:
- Cặt cron-job bằng thư viện celery
- Cài đặt các back-ground task
- Cho phép khởi tạo các back-ground task thông qua api


## Công nghệ sử dụng

- Python 3.8
- Flask 1.1.1
- Celery 5.0.5
- Redis (sử dụng như message queue của celery)

# Về dự án:
Phiên bản demo: (DONE)
- Cài đặt cron-job thực hiện tự động chạy gọi đến healthCheck API vào mỗi giờ.
- Xây dựng API cho phép thực hiện khởi động một background-task bất kỳ.

Phiên bản ứng dụng: (in-comming) 
- Sử dụng database HR_schema.sqlite xây dựng các model database
- Thực hiện cài đặt hàng ngày vào lúc 8h sáng, thực hiện quét database của HR, lấy ra danh sách các nhân viên có ngày vào công ty vào ngày hiện tại. Thực hiện gửi email chúc mừng.
- Cho phép HR staff có thể gửi thông báo đến một phòng bất kỳ thông qua email (HR staff không quan tâm đến kết quả gửi)
