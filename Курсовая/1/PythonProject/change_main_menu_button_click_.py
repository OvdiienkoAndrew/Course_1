import sqlite3
import tkinter as tk

from tkinter import messagebox, ttk
import tkinter.font as tkFont





def change_main_menu_button_click(root,name_db):
    from error_menu_ import error_menu
    from main_menu_ import main_menu
    from washed_down_main_menu_ import washed_down_main_menu

    def send_input():

        datas = []

        for entry in entries:
            datas.append(entry.get())

        with open("resources/settings/file.txt", 'w', encoding='utf-8') as file:
            for i in range(len(datas)):
                file.write(str(datas[i]) + " ")
        messagebox.showinfo("Повідомлення", "Налаштування змінені")


    for widget in root.winfo_children():
        widget.destroy()

    root.title("Налаштування")

    change_settings = tk.Button(root, text="Відкрити налаштування",
                                command=lambda: change_main_menu_button_click(root, name_db))
    error_window = tk.Button(root, text="Вікно помилок", command=lambda: error_menu(root, name_db), fg="red")
    main_menu_window = tk.Button(root, text="Головне меню", command=lambda: main_menu(root, name_db))
    washed_down_window = tk.Button(root, text="Запити", command=lambda: washed_down_main_menu(root, name_db))



    root.update()
    change_settings.place(x=10, y=10)
    root.update()
    main_menu_window.place(x=10 + change_settings.winfo_width() + 10, y=10)
    root.update()
    washed_down_window.place(x=10 + change_settings.winfo_width() + 10 + 10 + main_menu_window.winfo_width(), y=10)
    root.update()
    error_window.place(
        x=10 + change_settings.winfo_width() + 10 + 10 + main_menu_window.winfo_width() + 10 + washed_down_window.winfo_width(),
        y=10)
    root.update()

    with open("resources/settings/file.txt", "r", encoding="utf-8") as file:
        datas = [list(map(float, line.split())) for line in file.readlines()]


    hints = ["Середнє навантаження","Максимум перевищення у %", "Максимум", "Мінімум","Заступник декана з навчальної роботи", "Заступник декана з наукової роботи", "Заступник декана з виховної роботи", "Заступник декана з міжнародної роботи", "Гаранти ОП, які акредитуються","Гаранти ОП, які не акредитуються","Редактори журналів Скопус", "Керівники аспірантів  (на одного аспіранта)", "Рівномірність розподілу"]

    labels = []

    for i in range(0,len(hints)):
        labels.append(tk.Label(root, text=hints[i]))

    root.update()

    for label in labels:
        label.place(x=10,y=50)

    root.update()

    empty_height = root.winfo_height() - 20 - main_menu_window.winfo_height()

    for label in labels:
        empty_height -= label.winfo_height()

    empty_height /= (len(labels)+2)

    helper_height = 20 + main_menu_window.winfo_height()

    for i, label in enumerate(labels, start=1):
        label.place(x=10,y=helper_height+i*empty_height+(i-1)*label.winfo_height())

    entries = []

    for i in range(len(labels)):
        entries.append(tk.Entry(root))

    for i, entry in enumerate(entries, start=1):
        entry.place(x=root.winfo_width()/2+10, y=helper_height+i*empty_height+(i-1)*labels[i-1].winfo_height(), width=root.winfo_width()/2-20)
        entry.insert(0, str(datas[0][i-1]))

    send_button = tk.Button(root, text="Застосувати", command=send_input)
    send_button.place(x=10, y=helper_height + (len(labels)+1) * empty_height + (len(labels)) * labels[0].winfo_height())

    try:
        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()
        check_info = cursor.execute("SELECT * FROM ПЕРЕВІРКА").fetchall()
        check_info_as_st = cursor.execute("SELECT * FROM ПЕРЕВІРКА_АСИСТЕНТ_СТ_ВИКЛАДАЧ").fetchall()
        conn.close()
        if len(check_info) + len(check_info_as_st) == 0:
            error_window.place(x=-100, y=-100)

    except Exception:
        error_window.place(x=-100, y=-100)


