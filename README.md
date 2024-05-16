# DemoProject
Phiên bản python là 3.10.14
## ***Docker***
### Cách setup:
- Tạo Folder model trong project sao cho cùng cấp với các thư mục theo thứ tự Project/model 
- Tải và lưu mô hình vào thư mục model
- Link download: [link](https://drive.google.com/file/d/1U0ieHwFPmLQv_Ph73YliwXg4ARyvyArF/view?usp=sharing)
- Chạy ./build.sh với Macos, Linux và ./build.bat với Window
- Hoặc có thể chạy DOCKER_BUILDKIT=0 docker-compose up -d --build -t 10000

## ***Set up ở máy cá nhân***
- Làm các bước tương tự với Docker ở trên nhưng ở bước chạy lệnh build thì thay thế bằng lệnh pip install -r requirements.txt
