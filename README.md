# Lời mở đầu

## Chức năng 
Dự án này cho phép thực hiện:
- Cài đặt các cron-job bằng thư viện celery
- Cài đặt các back-ground task
- Cho phép khởi tạo các back-ground task thông qua api


## Công nghệ sử dụng

- Python 3.8
- Flask 1.1.1
- Celery 5.0.5
- Redis (sử dụng như message queue của celery)
- PostgreSQL (Để đảm bảo việc có thể phình to về mặt chức năng, database của bài toán thay đổi thành RDBMS)

# Về dự án:
Phiên bản demo: (DONE)
- Cài đặt cron-job thực hiện tự động chạy gọi đến healthCheck API vào mỗi giờ.
- Xây dựng API cho phép thực hiện khởi động một background-task bất kỳ.

Phiên bản ứng dụng: (DONE)
- Sử dụng database HR_schema xây dựng các model database. Có thể sử dụng database_script/Script_HR_postgre.sql để import vào P
- Thực hiện cài đặt hàng ngày vào lúc 8h sáng, thực hiện quét database của HR, lấy ra danh sách các nhân viên có ngày vào công ty vào nostgreSQLgày hiện tại. Thực hiện gửi email chúc mừng.
- Cho phép HR Staff có thể retry lại tác vụ gửi mail nếu lúc 8h gửi không thành công 
