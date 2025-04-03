import tkinter as tk
from tkinter import ttk
import random

def generate_sequence(n, sequence_type):
    """Tạo chuỗi giá trị theo loại chuỗi."""
    if n <= 1:
        return "Số lượng phần tử phải lớn hơn 1."
    n -= 1  # Giảm số lượng phần tử đi 1
    if sequence_type == "Không bị che":
        sequence = ",".join(["0"] * n)
    elif sequence_type == "Bị che":
        sequence = ",".join(["0" if i % 2 == 0 else "1" for i in range(n)])
    else:
        sequence = "Loại chuỗi không hợp lệ."
    return sequence

def generate_sequence_lane(n, sequence_type):
    """Tạo chuỗi giá trị cho Lane với quy tắc chia đều 1 và 2, 3 luôn nằm giữa và ở cuối."""
    if n <= 1:
        return "Số lượng phần tử phải lớn hơn 1."
    
    sequence = []
    count_1 = count_2 = (n - 2) // 2  # Chia đều số lượng 1 và 2
    if (n - 2) % 2 != 0:  # Nếu số lượng phần tử lẻ, thêm 1 vào 1
        count_1 += 1

    # Thêm giá trị 1 và 2 xen kẽ trước khi thêm 3 vào giữa
    for i in range(count_1):
        sequence.append(1)
    sequence.append(3)  # Thêm 3 vào giữa
    for i in range(count_2):
        sequence.append(2)
    sequence.append(3)  # Thêm 3 vào cuối

    return ",".join(map(str, sequence))

def on_generate_button_click(entry, sequence_type_var, result_entry, count_label, status_label):
    """Xử lý sự kiện khi nhấn nút Tạo chuỗi."""
    try:
        n = int(entry.get())
        sequence_type = sequence_type_var.get()
        result = generate_sequence(n, sequence_type)
        if n > 1 and "không hợp lệ" not in result:
            result_entry.delete(0, tk.END)  # Xóa nội dung cũ trong ô kết quả
            result_entry.insert(0, result)  # Hiển thị chuỗi kết quả trong ô
            count_label.config(text=f"Số lượng giá trị: {n - 1}", fg="green")
            status_label.config(text="Chuỗi đã được tạo thành công!", fg="green")
        else:
            count_label.config(text="")
            status_label.config(text=result, fg="red")
    except ValueError:
        count_label.config(text="")
        status_label.config(text="Vui lòng nhập một số nguyên hợp lệ.", fg="red")

def on_generate_button_click_lane(entry, sequence_type_var, result_entry, count_label, status_label):
    """Xử lý sự kiện khi nhấn nút Tạo chuỗi trong Lane."""
    try:
        n = int(entry.get())
        sequence_type = sequence_type_var.get()
        result = generate_sequence_lane(n, sequence_type)
        if n > 1 and "không hợp lệ" not in result:
            result_entry.delete(0, tk.END)  # Xóa nội dung cũ trong ô kết quả
            result_entry.insert(0, result)  # Hiển thị chuỗi kết quả trong ô
            count_label.config(text=f"Số lượng giá trị: {n}", foreground="green")
            status_label.config(text="Chuỗi đã được tạo thành công!", foreground="green")
        else:
            count_label.config(text="")
            status_label.config(text=result, foreground="red")
    except ValueError:
        count_label.config(text="")
        status_label.config(text="Vui lòng nhập một số nguyên hợp lệ.", foreground="red")

def on_copy_button_click(result_entry, status_label):
    """Xử lý sự kiện khi nhấn nút Sao chép."""
    result = result_entry.get()
    if result:
        root.clipboard_clear()  # Xóa clipboard hiện tại
        root.clipboard_append(result)  # Thêm chuỗi vào clipboard
        root.update()  # Cập nhật clipboard
        status_label.config(text="Đã sao chép chuỗi vào clipboard!", foreground="green")
    else:
        status_label.config(text="Không có chuỗi để sao chép.", foreground="red")

# Hàm xử lý sự kiện khi nhấn nút "Đếm Giá Trị"
def on_count_button_click(entry, result_text, status_label):
    """Xử lý sự kiện khi nhấn nút Đếm Giá Trị."""
    try:
        input_text = entry.get()
        if not input_text:
            raise ValueError("Chuỗi giá trị không được để trống.")
        
        # Tách chuỗi thành danh sách các giá trị
        values = input_text.split(",")
        values = [v.strip() for v in values if v.strip().isdigit()]  # Loại bỏ khoảng trắng và kiểm tra số hợp lệ
        
        if not values:
            raise ValueError("Chuỗi giá trị không hợp lệ. Vui lòng nhập các số, phân tách bằng dấu phẩy.")
        
        # Đếm số lần xuất hiện của từng giá trị
        counts = {}
        for value in values:
            counts[value] = counts.get(value, 0) + 1
        
        # Hiển thị kết quả
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)  # Xóa nội dung cũ
        for value, count in counts.items():
            result_text.insert(tk.END, f"Giá trị {value}: {count} lần\n")
        result_text.config(state="disabled")  # Không cho phép chỉnh sửa kết quả
        
        status_label.config(text="Đếm giá trị thành công!", fg="green")
    except ValueError as e:
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.config(state="disabled")
        status_label.config(text=str(e), fg="red")

if __name__ == "__main__":
    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Tạo Chuỗi Giá Trị")
    root.geometry("800x600")  # Đặt kích thước cửa sổ
    root.configure(bg="#f0f0f0")  # Màu nền cửa sổ

    # Cấu hình lưới để các thành phần mở rộng
    root.rowconfigure(0, weight=1)  # Hàng đầu tiên (Notebook) mở rộng
    root.rowconfigure(1, weight=0)  # Hàng cuối cùng (Bản quyền) cố định
    root.columnconfigure(0, weight=1)

    # Tạo Notebook (tab container)
    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky="nsew")  # Đặt Notebook ở hàng đầu tiên

    # Tùy chỉnh giao diện với ttk.Style
    style = ttk.Style()
    style.configure("TNotebook", background="#f0f0f0", foreground="#333", font=("Helvetica", 12))
    style.configure("TNotebook.Tab", font=("Helvetica", 12), padding=[10, 5])
    style.configure("TButton", font=("Helvetica", 12), padding=5)
    style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0", foreground="#333")

    # Tab Road
    tab_road = ttk.Frame(notebook)
    notebook.add(tab_road, text="Road")

    # Nhãn hướng dẫn
    label = tk.Label(tab_road, text="Nhập số lượng phần tử:", font=("Arial", 12))
    label.pack(pady=10)

    # Ô nhập liệu
    entry_road = tk.Entry(tab_road, font=("Arial", 12))
    entry_road.pack(pady=5)

    # Nhãn chọn loại chuỗi
    sequence_type_label = tk.Label(tab_road, text="Chọn loại chuỗi:", font=("Arial", 12))
    sequence_type_label.pack(pady=5)

    # Tùy chọn loại chuỗi
    sequence_type_var_road = tk.StringVar(value="Không bị che")
    sequence_type_dropdown = tk.OptionMenu(tab_road, sequence_type_var_road, "Không bị che", "Bị che")
    sequence_type_dropdown.pack(pady=5)

    # Nút tạo chuỗi
    result_entry_road = tk.Entry(tab_road, font=("Arial", 12), state="normal")
    count_label_road = tk.Label(tab_road, text="", font=("Arial", 12), fg="green")
    status_label_road = tk.Label(tab_road, text="", font=("Arial", 10), fg="blue")
    generate_button = tk.Button(
        tab_road,
        text="Tạo Chuỗi",
        font=("Arial", 12),
        command=lambda: on_generate_button_click(entry_road, sequence_type_var_road, result_entry_road, count_label_road, status_label_road),
    )
    generate_button.pack(pady=10)

    # Nhãn kết quả
    result_label = tk.Label(tab_road, text="Kết quả:", font=("Arial", 12))
    result_label.pack(pady=5)

    # Ô hiển thị kết quả (cho phép sao chép)
    result_entry_road.pack(pady=5)

    # Nhãn hiển thị số lượng giá trị
    count_label_road.pack(pady=5)

    # Nút sao chép
    copy_button = tk.Button(
        tab_road,
        text="Sao Chép",
        font=("Arial", 12),
        command=lambda: on_copy_button_click(result_entry_road, status_label_road),
    )
    copy_button.pack(pady=10)

    # Nhãn trạng thái
    status_label_road.pack(pady=10)

    # Tab Lane
    tab_lane = ttk.Frame(notebook)
    notebook.add(tab_lane, text="Lane")

    # Nhãn hướng dẫn
    label_lane = tk.Label(tab_lane, text="Nhập số lượng phần tử:", font=("Arial", 12))
    label_lane.pack(pady=10)

    # Ô nhập liệu
    entry_lane = tk.Entry(tab_lane, font=("Arial", 12))
    entry_lane.pack(pady=5)

    # Nhãn chọn loại chuỗi
    sequence_type_label_lane = tk.Label(tab_lane, text="Chọn loại chuỗi:", font=("Arial", 12))
    sequence_type_label_lane.pack(pady=5)

    # Tùy chọn loại chuỗi
    sequence_type_var_lane = tk.StringVar(value="Không bị che")
    sequence_type_dropdown_lane = tk.OptionMenu(tab_lane, sequence_type_var_lane, "Không bị che", "Bị che")
    sequence_type_dropdown_lane.pack(pady=5)

    # Nút tạo chuỗi
    result_entry_lane = tk.Entry(tab_lane, font=("Arial", 12), state="normal")
    count_label_lane = tk.Label(tab_lane, text="", font=("Arial", 12), fg="green")
    status_label_lane = tk.Label(tab_lane, text="", font=("Arial", 10), fg="blue")
    generate_button_lane = tk.Button(
        tab_lane,
        text="Tạo Chuỗi",
        font=("Arial", 12),
        command=lambda: on_generate_button_click_lane(entry_lane, sequence_type_var_lane, result_entry_lane, count_label_lane, status_label_lane),
    )
    generate_button_lane.pack(pady=10)

    # Nhãn kết quả
    result_label_lane = tk.Label(tab_lane, text="Kết quả:", font=("Arial", 12))
    result_label_lane.pack(pady=5)

    # Ô hiển thị kết quả (cho phép sao chép)
    result_entry_lane.pack(pady=5)

    # Nhãn hiển thị số lượng giá trị
    count_label_lane.pack(pady=5)

    # Nút sao chép
    copy_button_lane = tk.Button(
        tab_lane,
        text="Sao Chép",
        font=("Arial", 12),
        command=lambda: on_copy_button_click(result_entry_lane, status_label_lane),
    )
    copy_button_lane.pack(pady=10)

    # Nhãn trạng thái
    status_label_lane.pack(pady=10)

    # Tab Đếm Giá Trị
    tab_count = ttk.Frame(notebook)
    notebook.add(tab_count, text="Đếm Giá Trị")

    # Nhãn hướng dẫn
    label_count = tk.Label(tab_count, text="Nhập chuỗi giá trị (phân tách bằng dấu phẩy):", font=("Arial", 12))
    label_count.pack(pady=10)

    # Ô nhập liệu
    entry_count = tk.Entry(tab_count, font=("Arial", 12))
    entry_count.pack(pady=5)

    # Nút đếm giá trị
    status_label_count = tk.Label(tab_count, text="", font=("Arial", 10), fg="blue")
    count_button = tk.Button(
        tab_count,
        text="Đếm Giá Trị",
        font=("Arial", 12),
        command=lambda: on_count_button_click(entry_count, result_text_count, status_label_count),
    )
    count_button.pack(pady=10)

    # Nhãn kết quả
    result_label_count = tk.Label(tab_count, text="Kết quả:", font=("Arial", 12))
    result_label_count.pack(pady=5)

    # Khung chứa ô hiển thị kết quả và thanh cuộn
    result_frame = ttk.Frame(tab_count)
    result_frame.pack(pady=5, fill="both", expand=True)

    # Thanh cuộn dọc
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Ô hiển thị kết quả
    result_text_count = tk.Text(
        result_frame,
        font=("Arial", 12),
        height=10,
        wrap="word",
        yscrollcommand=scrollbar.set,
        bg="#f9f9f9",  # Màu nền nhạt
        fg="#333",  # Màu chữ
        relief="solid",  # Viền
        bd=1,  # Độ dày viền
    )
    result_text_count.pack(side="left", fill="both", expand=True)

    # Kết nối thanh cuộn với ô hiển thị kết quả
    scrollbar.config(command=result_text_count.yview)

    # Nhãn trạng thái
    status_label_count.pack(pady=10)

    # Thêm nhãn bản quyền ở cuối cửa sổ
    copyright_label = tk.Label(
        root,
        text="© 2025 By Dino TestWorks",
        font=("Arial", 10),
        fg="gray",
        bg="#f0f0f0"
    )
    copyright_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)  # Đặt ở hàng cuối cùng

    # Chạy vòng lặp giao diện
    root.mainloop()