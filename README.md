Báo cáo sản phẩm sáng tạo nội bộ chuyên môn 1 
Nhóm Thùng rác thông minh (Lê Hải Đăng, Ngô Bảo Lâm, Nguyễn Bá Hoài Văn, Hà Tuấn Kiệt, Nguyễn Ngọc Linh)

# I. TỔNG QUAN QUÁ TRÌNH VÀ SẢN PHẨM
### 1. Nguồn gốc
Trong bối cảnh môi trường đang ngày càng đối mặt với nhiều thách thức, việc quản lý rác thải hiệu quả trở thành một vấn đề cấp bách trên toàn cầu. Một trong những khâu quan trọng nhất nhưng cũng khó khăn nhất trong quá trình này là phân loại rác tại nguồn. Hiện nay, phần lớn rác thải sinh hoạt vẫn chưa được phân loại đúng cách trước khi thu gom, dẫn đến việc tái chế kém hiệu quả và gia tăng lượng rác chôn lấp, gây ô nhiễm đất, nước và không khí. Dựa trên vấn đề phổ biến và hiện trạng ngày nay của con người đối với vấn đề tái chế và phân loại rác thải, sản phẩm khoa học “Thùng rác thông minh” được đề xuất với chức năng mô phỏng cho việc giải quyết thực trạng này. 
### 2. Mô tả sản phẩm 
Sản phẩm khoa học “Thùng rác thông minh” là một chiếc thùng rác được thiết kế theo dạng hình hộp cùng một bộ khung làm bằng ống nhựa PVC, chia làm 4 ngăn để phân loại lần lượt là: Tái chế; Không tái chế; Nguy hiểm và Chưa phân loại. Trên trụ ống nhựa ở phần trung tâm có gắn một chiếc đĩa là nơi đặt rác và tự xoay, nghiêng để phân loại rác vào 4 ngăn. Đĩa quay được vận hành bằng các servo và model AI để nhận diện rác được lắp đặt ở phía trên của đĩa.
### 3. Ý nghĩa thực tiễn và tiềm năng của sản phẩm
Thùng rác thông minh có thể được ứng dụng trong các quán ăn, tiệm cà phê hay trong hộ gia đình và trường học giúp thuận tiện hoá việc phân loại rác thải tránh việc lãng phí thời gian.
Thùng rác thông minh có thể được ứng dụng để giáo dục cho trẻ em về ý thức phân loại rác thải ngay từ nhỏ.
Thùng rác thông minh có thể được dùng để hỗ trợ người cao tuổi và người khiếm thị trong việc phân loại các loại rác thải một cách dễ dàng và chính xác.

# II. CƠ SỞ KHOA HỌC
### Thị giác máy tính và xử lý hình ảnh
**Nguyên lý**: Khi rác được đặt vào, một camera tích hợp sẽ chụp ảnh vật thể. Các thuật toán xử lý ảnh sau đó sẽ phân tích hình ảnh này. 
**Cơ sở khoa học**: Lấy hình ảnh và dữ liệu từ vật để chuẩn bị các thao tác cho bước tiếp theo
### Trí tuệ nhân tạo và học máy
**Nguyên lý**: Dữ liệu đặc trưng được trích xuất từ hình ảnh sẽ được đưa vào một mô hình học máy.
**Huấn luyện mô hình**: Mô hình CNN được "huấn luyện" (training) trên một lượng lớn dữ liệu hình ảnh về các loại rác khác nhau (nhựa, giấy, kim loại, hữu cơ, v.v.) cùng với nhãn phân loại tương ứng. Trong quá trình huấn luyện, mạng nơ-ron sẽ tự động học cách nhận diện các mẫu (patterns) và đặc điểm độc đáo của từng loại rác.
**Dự đoán:** Khi một vật thể mới được đưa vào, mô hình đã huấn luyện sẽ phân tích các đặc trưng của nó và đưa ra dự đoán về loại rác.
**Cơ sở khoa học**: Học máy cho phép hệ thống học hỏi tự động học hỏi từ dữ liệu thô và trích xuất các đặc trưng phức tạp thành các dữ liệu hình ảnh đạt được độ chính xác cao trong thao tác nhận diện và phân loại.
# III. THỰC HIỆN SẢN PHẨM 
### Linh kiện và vật liệu
**Các linh kiện điện tử chính**:
 - ESP32 - S3 Camera
 - Động cơ Servo MG995 (2 cái)
 - Cảm biến hồng ngoại IR Sensor
 
**Các vật liệu khác**:
 - Ống nước
 - Thùng carton
 - Đĩa, trụ quay cho Servo (in 3D)
 
### Cách thức hoạt động
 - Khi được bật, thiết bị sẽ tự động kết nối Wifi vào hệ thống mạng đã được cấu hình sẵn để có thể giao tiếp với máy chủ.
 - Cảm biến IR sensor sẽ phát hiện khi có rác được đưa vào, từ đó ra lệnh để camera chụp ảnh. Hình ảnh sau đó sẽ được gửi đến máy chủ qua giao thức HTTP để xử lý.
 - Tại máy chủ, hình ảnh sẽ được phân tích bằng mô hình AI đã được huấn luyện sẵn nhằm phân loại rác. Kết quả nhận diện sau đó được gửi ngược về thiết bị tại thùng rác.
 - Thiết bị sẽ tiếp nhận kết quả và điều khiển động cơ servo xoay để đưa rác vào đúng ngăn thùng tương ứng với loại rác đã được phân loại.
 - Hệ thống servo bao gồm hai động cơ servo, được lắp đặt trên một trục quay được thiết kế để điều khiển đĩa quay theo hai trục khác nhau.

# Tổng kết
Dự án thùng rác thông minh có tính ứng dụng cao và có thể đáp ứng nhu cầu của con người đối với việc giải quyết thực trạng về phân loại rác thải cho việc kiểm soát và tái chế. Tuy vẫn tồn tại các khuyết điểm nhưng đều có thể khắc phục, nhằm đạt được độ hiệu quả cao nhất hướng đến nhu cầu chung của xã hội.

