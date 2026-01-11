from guizero import App, Text, TextBox, PushButton, ListBox

app = App(title="Ứng dụng quản lý điểm", width=400, height=400)

Text(app, text="Tên môn:")
mon_box = TextBox(app)

Text(app, text="Điểm:")
diem_box = TextBox(app)

ds_diem = []

def them_mon():
    mon = mon_box.value
    diem = diem_box.value
    if mon != "" and diem != "":
        ds_diem.append(f"{mon}: {diem}")
        listbox.append(f"{mon}: {diem}")
        mon_box.value = ""
        diem_box.value = ""

def xuat_file():
    with open("ket_qua.txt", "w", encoding="utf-8") as f:
        f.write("DANH SÁCH MÔN HỌC\n")
        for item in ds_diem:
            f.write(item + "\n")

PushButton(app, text="Thêm môn", command=them_mon)

Text(app, text="Danh sách môn:")
listbox = ListBox(app, items=[])

PushButton(app, text="Xuất ra file", command=xuat_file)

app.display()