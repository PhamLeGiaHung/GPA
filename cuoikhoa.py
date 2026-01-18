from guizero import App, Text, TextBox, PushButton, ListBox, Box

app = App(title="Ứng dụng quản lý điểm", width=420, height=420)

# ====== DATA ======
ds_diem = []   # lưu dạng (mon, diem)

# ====== GIAO DIỆN ======
Text(app, text="ỨNG DỤNG QUẢN LÝ ĐIỂM", size=16)

input_box = Box(app)

Text(input_box, text="Tên môn:")
mon_box = TextBox(input_box, width=20)

Text(input_box, text="Điểm:")
diem_box = TextBox(input_box, width=10)

# ====== DANH SÁCH ======
Text(app, text="Danh sách môn:")
listbox = ListBox(app, width=40, height=10)

# ====== HÀM ======
def cap_nhat_listbox():
    listbox.clear()
    for mon, diem in ds_diem:
        listbox.append(f"{mon}: {diem}")

def them_mon():
    mon = mon_box.value.strip()
    diem = diem_box.value.strip()

    if mon == "" or diem == "":
        return

    if not diem.replace(".", "", 1).isdigit():
        return

    ds_diem.append((mon, diem))
    cap_nhat_listbox()
    mon_box.value = ""
    diem_box.value = ""

def xoa_mon():
    if listbox.value == "":
        return

    index = listbox.items.index(listbox.value)
    ds_diem.pop(index)
    cap_nhat_listbox()

def sua_mon():
    if listbox.value == "":
        return

    index = listbox.items.index(listbox.value)
    mon = mon_box.value.strip()
    diem = diem_box.value.strip()

    if mon == "" or diem == "":
        return

    if not diem.replace(".", "", 1).isdigit():
        return

    ds_diem[index] = (mon, diem)
    cap_nhat_listbox()
    mon_box.value = ""
    diem_box.value = ""

def chon_mon():
    if listbox.value == "":
        return

    index = listbox.items.index(listbox.value)
    mon_box.value = ds_diem[index][0]
    diem_box.value = ds_diem[index][1]

def xuat_file():
    with open("ket_qua.txt", "w", encoding="utf-8") as f:
        f.write("DANH SÁCH MÔN HỌC\n")
        for mon, diem in ds_diem:
            f.write(f"{mon}: {diem}\n")

# ====== BUTTON ======
button_box = Box(app)

PushButton(button_box, text="Thêm", command=them_mon)
PushButton(button_box, text="Sửa", command=sua_mon)
PushButton(button_box, text="Xóa", command=xoa_mon)

PushButton(app, text="Xuất ra file", command=xuat_file)

listbox.when_selected = chon_mon

Text(app, text="File xuất ra: ket_qua.txt")

app.display()
