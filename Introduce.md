# Hướng Dẫn Sử Dụng Hệ Thống Tính Toán Vật Lý AiiDA

Tài liệu này hướng dẫn cách cấu hình, cài đặt và phát triển giao diện cho hệ thống tính toán sử dụng framework AiiDA.

- Đầu tiên hãy clone 2 repo sau 
  - Aiida quad(Plugin): https://github.com/qmat-group/aiida-quad.git
  - Aiida MVC: https://github.com/qmat-group/aiidalab-mvc.git
 
Sử dụng lệnh `git clone { link repo }`

## Bước 1: Cấu Hình và Setup Hệ Thống

Hệ thống được tổ chức thành hai phần chính trong thư mục `setup`:

- **`setup/config`**: Chứa các file cấu hình định dạng YAML.
- **`setup/build`**: Chứa các script tự động hóa quá trình setup.

### 1.1 Chỉnh Sửa File Cấu Hình

Trước khi chạy script, bạn cần kiểm tra và chỉnh sửa thông tin trong các file config phù hợp với hệ thống thực tế của bạn:

- **Config Computer**: Vào `setup/config/computer/`.
  - Mở các file `.yaml` (ví dụ: `pias_computer.yaml`).
  - File này chứa cả thông tin setup (hostname, work_dir...) và thông tin user/auth.
  - Chỉnh sửa các thông tin cần thiết trong cùng một file.
- **Config Code**: Vào `setup/config/code/`.
  - Mở các file `.yaml` (ví dụ: `code_quad.yaml`).
  - Chỉnh sửa đường dẫn đến file thực thi (`filepath_executable`), tên computer tương ứng, và các lệnh `prepend_text` (như load module, activate environment).

### 1.2 Chạy Script Setup

Sau khi cấu hình xong, bạn sử dụng các script trong `/setup/build` để nạp thông tin vào AiiDA database.

**Tính năng chọn lọc**:
Mặc định script sẽ chạy tất cả các file `.yaml` trong thư mục config. Nếu muốn chỉ chạy một số file nhất định, bạn mở file script `.sh` và sửa biến `TARGET_FILES` ở đầu file:

```bash
# Ví dụ: chỉ chạy file pias.yaml
TARGET_FILES=("pias.yaml")
```

- **Chạy toàn bộ (Khuyên dùng)**:

  ```bash
  cd setup/build
  bash setup.sh
  ```

  Script này sẽ tự động chạy tuần tự setup computer trước, sau đó đến setup code.

- **Chạy riêng lẻ**:
  - Chỉ setup computer: `bash setup_computer.sh`
  - Chỉ setup code: `bash create_update-code.sh` (Sử dụng khi bạn chỉ muốn cập nhật hoặc thêm code mới).

---

## Bước 2: Cài Đặt Plugin (Build Code)

Để AiiDA nhận diện được plugin tính toán (ví dụ `aiida-quad`), bạn cần cài đặt nó vào môi trường python hiện tại.

1. Di chuyển vào thư mục chứa source code của plugin (ví dụ `demo/aiida-quad`).
2. Chạy lệnh cài đặt ở chế độ development:

   ```bash
   pip install -e .
   ```

   *Lưu ý: Cần kích hoạt môi trường ảo (virtualenv/conda) chứa AiiDA trước khi chạy lệnh này.*

---

## Bước 3: Thiết Kế và Chỉnh Sửa Giao Diện (View)

Giao diện người dùng được xây dựng theo mô hình MVC (Model-View-Controller) và nằm trong thư mục `demo/aiidalab-mvc`. Cấu trúc View được định nghĩa bằng file YAML, giúp bạn dễ dàng chỉnh sửa mà không cần can thiệp sâu vào code Python.

### 3.1 Vị Trí File Cấu Hình View

- File cấu hình giao diện: `demo/aiidalab-mvc/src/views/yaml_elements/view.yaml`
- Logic load view: `demo/aiidalab-mvc/src/views/view.py`

### 3.2 Cách Chỉnh Sửa

Mở file `view.yaml` và thay đổi cấu trúc cây widgets. Các widget được lồng nhau thông qua thuộc tính `children`.

**Ví dụ cấu trúc YAML:**

```yaml
type: VBox
children:
  - type: HTML
    value: "<h3>My App Title</h3>"
  - type: HBox
    children:
      - type: FloatText
        description: "Input A"
        key: "input_a"  # Key để bind với Model
```

### 3.3 Bảng Các Element Input/Output Hỗ Trợ

Dưới đây là danh sách các widget thông dụng (dựa trên `ipywidgets`) bạn có thể sử dụng trong file YAML:

| Element Type | Mô tả | Thuộc tính quan trọng | Input/Output |
| :--- | :--- | :--- | :--- |
| **FloatText** | Ô nhập liệu số thực | `value`, `description`, `disabled` | Input |
| **IntText** | Ô nhập liệu số nguyên | `value`, `description` | Input |
| **Text** | Ô nhập liệu văn bản | `value`, `placeholder` | Input |
| **Button** | Nút bấm | `description`, `button_style`, `icon` | Action |
| **Dropdown** | Menu thả xuống | `options`, `value`, `description` | Input |
| **Checkbox** | Hộp kiểm (True/False) | `value`, `description` | Input |
| **HTML** | Hiển thị nội dung HTML | `value` | Output |
| **Label** | Nhãn văn bản đơn giản | `value` | Output |
| **Output** | Vùng hiển thị kết quả log/plot | (Thường dùng `widgets_dict` trong code để print vào) | Output |
| **VBox** | Container xếp dọc | `children` (list) | Layout |
| **HBox** | Container xếp ngang | `children` (list) | Layout |

---

## Bước 4: Kiểm Tra và Chạy Ứng Dụng

1. **Kiểm tra file YAML**:
   Chạy script kiểm tra để đảm bảo file `view.yaml` hợp lệ và đầy đủ các widget cần thiết.

   ```bash
   cd demo/aiidalab-mvc/src/views
   python verify_yaml.py
   ```

2. **Khởi chạy ứng dụng**:
   Mở Jupyter Notebook và chạy file `demo/aiidalab-mvc/launcher.ipynb`.
   - Notebook sẽ load Model, View (từ YAML), và Controller.
   - Giao diện sẽ hiển thị ngay trong notebook để bạn tương tác.

Chúc bạn thành công với hệ thống AiiDA!
