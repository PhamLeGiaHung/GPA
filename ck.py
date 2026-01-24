from guizero import App, Text, TextBox, PushButton, ListBox, Box, Combo, info

# ====== KHỞI TẠO ======
app = App(title="Ứng dụng quản lý điểm", width=420, height=620, bg="lightblue")
ds_diem = [] 

# ====== HÀM XỬ LÝ ======
def tinh_trung_binh():
    if not ds_diem: return 0
    tong = sum(float(item[1]) for item in ds_diem)
    return round(tong / len(ds_diem), 2)

def xep_loai(dtb):
    if dtb >= 8.0: return "GIỎI 🏆"
    if dtb >= 6.5: return "KHÁ 👍"
    if dtb >= 5.0: return "TRUNG BÌNH 😐"
    return "YẾU ⚠"

def cap_nhat_giao_dien():
    listbox.clear()
    for mon, diem in ds_diem:
        # Căn lề ljust giúp danh sách thẳng hàng hơn
        listbox.append(f"{mon}: {diem}")
    
    dtb = tinh_trung_binh()
    loai = xep_loai(dtb)
    
    text_dtb.value = f"ĐIỂM TRUNG BÌNH: {dtb}"
    text_loai.value = f"HỌC LỰC: {loai}"
    
    # Đổi màu chữ theo điểm số
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

    try:
        val = float(diem_nhap)
        if 0 <= val <= 10:
            ds_diem.append([mon_moi, str(val)])
            cap_nhat_giao_dien()
            diem_box.value = ""
        else:
            info("Lỗi", "Điểm số phải từ 0 đến 10!")
    except ValueError:
        info("Lỗi", "Điểm số phải là một con số!")

def sua_mon():
    if listbox.value is None:
        info("Thông báo", "Hãy chọn một môn để sửa!")
        return
    
    index = listbox.items.index(listbox.value)
    diem_nhap = diem_box.value.strip()

    try:
        val = float(diem_nhap)
        if 0 <= val <= 10:
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
    diem_box.value = ""

def chon_mon():
    if listbox.value is None: return
    # Tách dữ liệu từ dòng được chọn "Toán: 8.0"
    selected_text = listbox.value
    mon_name = selected_text.split(":")[0]
    for item in ds_diem:
        if item[0] == mon_name:
            mon_combo.value = item[0]
            diem_box.value = item[1]
            break

def xuat_file():
    if not ds_diem:
        info("Thông báo", "Danh sách trống!")
        return
    try:
        dtb = tinh_trung_binh()
        with open("bang_diem.txt", "w", encoding="utf-8") as f:
            f.write("========== BẢNG ĐIỂM CHI TIẾT ==========\n")
            for i, (mon, diem) in enumerate(ds_diem, 1):
                f.write(f"{i}. {mon}: {diem} điểm\n")
            f.write("-" * 40 + "\n")
            f.write(f"ĐIỂM TRUNG BÌNH: {dtb}\n")
            f.write(f"HỌC LỰC: {xep_loai(dtb)}\n")
            f.write("========================================\n")
        info("Thành công", "Đã lưu vào file bang_diem.txt")
    except Exception as e:
        info("Lỗi", f"Không thể xuất file: {e}")

# ====== GIAO DIỆN (UI) ======
Text(app, text="QUẢN LÝ ĐIỂM HỌC TẬP", size=18, color="blue", font="Arial bold")

input_box = Box(app, layout="grid", border=True)
input_box.bg = "white"
Text(input_box, text=" Chọn môn:  ", grid=[0,0], align="left")
mon_combo = Combo(input_box, options=["Toán", "Văn", "Anh", "Lý", "Hóa", "Sinh", "Tin", "Sử", "Địa"], grid=[1,0], align="left")

Text(input_box, text=" Điểm (0-10):", grid=[0,1], align="left")
diem_box = TextBox(input_box, width=10, grid=[1,1], align="left")

button_box = Box(app)
btn1 = PushButton(button_box, text="Thêm ➕", command=them_mon, align="left")
btn2 = PushButton(button_box, text="Sửa ⚙️", command=sua_mon, align="left")
btn3 = PushButton(button_box, text="Xóa 🗑️", command=xoa_mon, align="left")
btn1.bg = "#a5d6a7"; btn2.bg = "#fff59d"; btn3.bg = "#ef9a9a"

Text(app, text="\nDANH SÁCH ĐÃ NHẬP:")
listbox = ListBox(app, width=300, height=150) # height=10 dòng
listbox.bg = "white"
listbox.when_selected = chon_mon

text_dtb = Text(app, text="ĐIỂM TRUNG BÌNH: 0", size=14, font="Arial bold")
text_loai = Text(app, text="HỌC LỰC: ---", size=12, color="blue")

btn_xuat = PushButton(app, text="XUẤT BẢNG ĐIỂM RA FILE .TXT 📄", command=xuat_file, width="fill")
btn_xuat.bg = "white"

app.display()