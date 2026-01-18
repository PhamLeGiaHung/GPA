from guizero import App, Text, TextBox, PushButton, ListBox, Box, Combo, info

app = App(title="Ứng dụng quản lý điểm", width=420, height=520,bg="lightblue")

# ====== DATA ======
ds_diem = []   # lưu dạng [mon, diem]

# ====== GIAO DIỆN ======
Text(app, text="ỨNG DỤNG QUẢN LÝ ĐIỂM", size=16, color="blue")

input_box = Box(app, layout="grid")
Text(input_box, text="Chọn môn:", grid=[0,0], align="left")
mon_combo = Combo(input_box, options=["Toán", "Văn", "Anh", "Lý", "Hóa"], grid=[1,0], align="left")

Text(input_box, text="Điểm số:", grid=[0,1], align="left")
diem_box = TextBox(input_box, width=10, grid=[1,1], align="left")

# ====== HÀM XỬ LÝ ======
def tinh_trung_binh():
    if not ds_diem:
        return 0
    tong = sum(float(item[1]) for item in ds_diem)
    return round(tong / len(ds_diem), 2)

def cap_nhat_giao_dien():
    # Cập nhật danh sách hiển thị
    listbox.clear()
    for mon, diem in ds_diem:
        listbox.append(f"{mon}: {diem}")
    
    # Cập nhật dòng chữ điểm trung bình
    dtb = tinh_trung_binh()
    text_dtb.value = f"ĐIỂM TRUNG BÌNH: {dtb}"
    
    # Đổi màu chữ nếu điểm cao hoặc thấp
    if dtb >= 8: text_dtb.text_color = "green"
    elif dtb < 5: text_dtb.text_color = "red"
    else: text_dtb.text_color = "black"

def them_mon():
    mon = mon_combo.value
    diem = diem_box.value.strip()

    if diem == "":
        info("Thông báo", "Vui lòng nhập điểm!")
        return

    try:
        val = float(diem)
        if val < 0 or val > 10:
            info("Lỗi", "Điểm phải từ 0 đến 10!")
            return
    except ValueError:
        info("Lỗi", "Điểm phải là số!")
        return

    ds_diem.append([mon, diem])
    cap_nhat_giao_dien()
    diem_box.value = ""

def xoa_mon():
    if listbox.value is None: return
    index = listbox.items.index(listbox.value)
    ds_diem.pop(index)
    cap_nhat_giao_dien()

def sua_mon():
    if listbox.value is None: return
    index = listbox.items.index(listbox.value)
    diem = diem_box.value.strip()
    if diem != "":
        ds_diem[index] = [mon_combo.value, diem]
        cap_nhat_giao_dien()

def chon_mon():
    if listbox.value is None: return
    index = listbox.items.index(listbox.value)
    mon_combo.value = ds_diem[index][0]
    diem_box.value = ds_diem[index][1]

# ====== NÚT BẤM ======
button_box = Box(app)
btn1 = PushButton(button_box, text="Thêm ➕", command=them_mon, align="left")
btn2 = PushButton(button_box, text="Sửa⚙️", command=sua_mon, align="left")
btn3 = PushButton(button_box, text="Xóa🗑️", command=xoa_mon, align="left")
btn1.bg = "lightgreen"
btn2.bg = "yellow"
btn3.bg = "tomato"

Text(app, text="\nDanh sách môn đã nhập (Dài):")
listbox = ListBox(app, width=100, height=250) # Tăng height để danh sách dài hơn
listbox.when_selected = chon_mon

# HIỂN THỊ ĐIỂM TRUNG BÌNH
text_dtb = Text(app, text="ĐIỂM TRUNG BÌNH: 0", size=14, font="Arial bold")

def xuat_file():
    with open("ket_qua.txt", "w", encoding="utf-8") as f:
        f.write(f"BẢNG ĐIỂM - ĐTB: {tinh_trung_binh()}\n")
        f.write("-" * 20 + "\n")
        for mon, diem in ds_diem:
            f.write(f"{mon}: {diem}\n")
    info("Thành công", "Đã xuất file!")

btn4 = PushButton(app, text="Xuất file", command=xuat_file, width="fill")
btn4.bg = "grey"

app.display()