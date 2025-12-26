# MVC Template

This is the template for an AiiDAlab app based on the MVC design

## Installation

This Jupyter-based app is intended to be run with [AiiDAlab](https://www.materialscloud.org/aiidalab).

Assuming that the app was registered, you can install it directly via the app store in AiiDAlab or on the command line with:
```
aiidalab install mvc
```
Otherwise, you can also install it directly from the repository:
```
aiidalab install mvc@https://github.com/qmat-group/mvc
```

## Usage

Here may go a few sreenshots / animated gifs illustrating how to use the app.

## License

MIT

## Contact

hung.dangthe@phenikaa-uni.edu.vn
# FrameWorkMVC

Thư mục này chứa các mẫu (templates) chuẩn hóa để tạo AiiDA plugins và các ứng dụng MVC sử dụng `traitlets` và `ipywidgets`. Mục tiêu là cung cấp một cấu trúc thống nhất giúp các thành viên trong team dễ dàng tiếp cận và phát triển.

## Cấu Trúc Thư Mục

- `plugin_template/`: Chứa các mẫu cho AiiDA `CalcJob` và `Parser`.
- `mvc_template/`: Chứa các mẫu để xây dựng giao diện tương tác (widgets) theo mô hình Model-View-Controller.

## Hướng Dẫn Sử Dụng

### Phát Triển Plugin (Plugin Development)

1. Sao chép `plugin_template/calculation.py` vào thư mục plugin của bạn và đổi tên/chỉnh sửa class `TemplateCalcJob`.
2. Sao chép `plugin_template/parser.py` vào thư mục plugin của bạn và đổi tên/chỉnh sửa class `TemplateParser`.
3. Đăng ký plugin trong `pyproject.toml` hoặc `setup.py` sử dụng `entry_points`.

### Phát Triển Ứng Dụng MVC (MVC Application Development)

Để tạo một ứng dụng giao diện (App) trên JupyterHub, chúng ta sử dụng mô hình MVC. Thay vì viết tất cả code trong một file `.ipynb` dài và khó quản lý, chúng ta chia nhỏ code thành các file `.py` riêng biệt.

1. Sao chép nội dung của `mvc_template/` vào thư mục ứng dụng của bạn.
2. **Model (`model.py`)**: Nơi định nghĩa dữ liệu và logic nghiệp vụ. Sử dụng `traitlets` để tạo các biến có khả năng phản ứng (reactive). Tại đây bạn sẽ xử lý việc submit job AiiDA, theo dõi trạng thái và xử lý kết quả.
3. **View (`view.py`)**: Nơi định nghĩa giao diện người dùng (UI) sử dụng `ipywidgets`. File này chỉ chứa các widget và bố cục (layout), không chứa logic xử lý dữ liệu.
4. **Controller (`controller.py`)**: Là cầu nối giữa Model và View.
    - Lắng nghe sự kiện từ View (ví dụ: bấm nút) để cập nhật Model.
    - Lắng nghe thay đổi từ Model (ví dụ: job chạy xong) để cập nhật View.
5. **Launcher (`launcher.ipynb`)**: Đây là file notebook dùng để chạy ứng dụng. Nó chỉ đơn giản là import App và hiển thị ra màn hình. Người dùng cuối sẽ mở file này.

## Tại sao lại dùng MVC và tách file .py?

- **Dễ bảo trì**: Code logic (Model) tách biệt với giao diện (View). Khi muốn sửa giao diện, bạn không sợ làm hỏng logic tính toán.
- **Tái sử dụng**: Model có thể được sử dụng lại cho các giao diện khác nhau hoặc chạy ngầm không cần giao diện.
- **Làm việc nhóm**: Mọi người dễ dàng đọc hiểu code của nhau hơn khi tuân theo một cấu trúc chung.
- **Quản lý phiên bản (Git)**: File `.py` dễ diff và merge hơn file `.ipynb` rất nhiều.

## Chi Tiết Các Thành Phần MVC

### Model (`model.py`)

- Chứa các `traitlets` đại diện cho input parameters, trạng thái tính toán, và kết quả.
- Chứa hàm `calculate()` để submit job.
- Chứa thread ngầm (`threading`) để theo dõi trạng thái job AiiDA mà không làm đơ giao diện.

### View (`view.py`)

- Khởi tạo các widgets: `FloatText`, `IntText`, `Button`, `ProgressBar`, `HTML`...
- Sắp xếp layout bằng `VBox`, `HBox`.

### Controller (`controller.py`)

- Dùng `traitlets.link` để đồng bộ dữ liệu 2 chiều giữa Model và View (ví dụ: nhập số vào ô text -> cập nhật biến trong Model).
- Đăng ký các hàm xử lý sự kiện (`observe`, `on_click`).

### Phát Triển Giao Diện Bằng YAML (New Feature)

Để đơn giản hóa việc quản lý giao diện phức tạp, bạn có thể định nghĩa UI trong file `.yaml` thay vì viết code Python trong `view.py`.

1. **Tạo file `view.yaml`**: Định nghĩa cấu trúc widget.

    ```yaml
    layout: VBox
    children:
      - type: FloatText
        description: "Input A:"
        key: input_a  # Key này sẽ được dùng để bind với Model
      - type: Button
        description: "Calculate"
        key: calculate_btn
        event: calculate # Tên sự kiện để bind với Controller (_on_calculate)
    ```

2. **Sử dụng `YAMLView`**:
    Trong `view.py` hoặc `app.ipynb`:

    ```python
    from mvc_template.view import YAMLView
    view = YAMLView('view.yaml')
    ```

3. **Controller tự động binding**:
    Controller sẽ tự động:
    - Link `model.input_a` <-> `view.widgets_dict['input_a'].value`
    - Bind `view.widgets_dict['calculate_btn'].on_click` -> `controller._on_calculate`

Xem ví dụ chi tiết tại thư mục `FrameWorkMVC/example`.
