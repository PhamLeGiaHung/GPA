from guizero import App, Text, TextBox, PushButton, ListBox, Box, Combo, info

# ====== KHỞI TẠO ======
app = App(title="Ứng dụng quản lý điểm", width=420, height=550, bg="lightblue")
ds_diem = [] 

# ====== HÀM XỬ LÝ ======
def tinh_trung_binh():
    if not ds_diem: return 0
    tong = sum(float(item[1]) for item in ds_diem)
    return round(tong / len(ds_diem), 2)

def cap_nhat_giao_dien():
    listbox.clear()
    for mon, diem in ds_diem:
        listbox.append(f"{mon}: {diem}")
    dtb = tinh_trung_binh()
    text_dtb.value = f"ĐIỂM TRUNG BÌNH: {dtb}"
    if dtb >= 8: text_dtb.text_color = "green"
    elif dtb < 5: text_dtb.text_color = "red"
    else: text_dtb.text_color = "black"

def them_mon():
    mon_moi = mon_combo.value
    diem_nhap = diem_box.value.strip()

    if diem_nhap == "":
        info("Thông báo", "Vui lòng nhập điểm!")
        return

    # KIỂM TRA TRÙNG MÔN
    for item in ds_diem:
        if item[0] == mon_moi:
            info("Lỗi", f"Môn {mon_moi} đã có trong danh sách!")
            return

    # KIỂM TRA ĐIỂM (KHÔNG QUÁ 10)
    try:
        val = float(diem_nhap)
        if val < 0 or val > 10:
            info("Lỗi", "Điểm số phải nằm trong khoảng từ 0 đến 10!")
            return
    except ValueError:
        info("Lỗi", "Điểm số phải là một con số!")
        return

    ds_diem.append([mon_moi, str(val)])
    cap_nhat_giao_dien()
    diem_box.value = ""

def sua_mon():
    if listbox.value is None:
        info("Thông báo", "Hãy chọn một môn trong danh sách để sửa!")
        return
    
    index = listbox.items.index(listbox.value)
    diem_nhap = diem_box.value.strip()

    try:
        val = float(diem_nhap)
        if 0 <= val <= 10:
            # Khi sửa, ta cập nhật lại cả môn và điểm tại vị trí đã chọn
            ds_diem[index] = [mon_combo.value, str(val)]
            cap_nhat_giao_dien()
        else:
            info("Lỗi", "Điểm phải từ 0 đến 10!")
    except ValueError:
        info("Lỗi", "Vui lòng nhập số điểm hợp lệ!")

def xoa_mon():
    if listbox.value is None: return
    index = listbox.items.index(listbox.value)
    ds_diem.pop(index)
    cap_nhat_giao_dien()

def chon_mon():
    if listbox.value is None: return
    # Tách chuỗi "Toán: 8.0" để lấy dữ liệu đổ ngược vào ô nhập
    selected_text = listbox.value
    mon_name = selected_text.split(":")[0]
    # Tìm trong ds_diem để lấy điểm chính xác
    for item in ds_diem:
        if item[0] == mon_name:
            mon_combo.value = item[0]
            diem_box.value = item[1]
            break

# ====== GIAO DIỆN (UI) ======
Text(app, text="ỨNG DỤNG QUẢN LÝ ĐIỂM", size=16, color="blue", font="Arial bold")

# Đã xóa tham số padding=10 để tránh lỗi TypeError
input_box = Box(app, layout="grid")
Text(input_box, text="Chọn môn:  ", grid=[0,0], align="left")
mon_combo = Combo(input_box, options=["Toán", "Văn", "Anh", "Lý", "Hóa", "Sinh", "Tin"], grid=[1,0], align="left")

Text(input_box, text="Điểm (0-10):", grid=[0,1], align="left")
diem_box = TextBox(input_box, width=10, grid=[1,1], align="left")

# Box cho các nút bấm
button_box = Box(app)
btn1 = PushButton(button_box, text="Thêm ➕", command=them_mon, align="left")
btn2 = PushButton(button_box, text="Sửa ⚙️", command=sua_mon, align="left")
btn3 = PushButton(button_box, text="Xóa 🗑️", command=xoa_mon, align="left")
btn1.bg = "lightgreen"
btn2.bg = "yellow"
btn3.bg = "tomato"

Text(app, text="\nDanh sách môn đã nhập:")
listbox = ListBox(app, width=300, height=200)
listbox.when_selected = chon_mon

text_dtb = Text(app, text="ĐIỂM TRUNG BÌNH: 0", size=14, font="Arial bold")

app.display()