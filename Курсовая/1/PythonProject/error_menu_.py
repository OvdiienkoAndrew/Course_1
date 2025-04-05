# -*- coding: utf-8 -*-

import sqlite3
import tkinter as tk
from tkinter import ttk



def error_menu(root,name_db):
    from change_main_menu_button_click_ import change_main_menu_button_click
    from main_menu_ import main_menu
    from washed_down_main_menu_ import washed_down_main_menu

    root.title("Помилки")
    for widget in root.winfo_children():
        widget.destroy()


    root.title("Помилки")

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

    check_info = ""
    check_info_as_st = ""
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



    canvas = tk.Canvas(root)
    scrollbar_vertical = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar_horizontal = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)


    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=50)
    scrollbar_vertical.pack(side="right", fill="y", padx=10, pady=50)
    scrollbar_horizontal.pack(side="bottom", fill="x", padx=10, pady=50)



    k=0
    if str(check_info):
        for i in range(0, len((check_info))):
            temp = ""
            for j in range(1, len((check_info[i]))):
                if j==4:
                    temp += "cтавка: "
                if len(str(check_info[i][j]))<=0:
                    continue
                if j == 6:
                    temp += "загальна кількость годин: "
                if j == 7:
                    temp += "мінімум: "
                if j == 8:
                    temp += "максимум: "
                if j == 9:
                    temp += "загальний мінімум: "
                if j == 10:
                    temp += "загальний максимум: "
                temp += str(check_info[i][j]) + " "

            label = tk.Label(scrollable_frame, text=temp)
            label.grid(row=i + 1, column=0, pady=5)
            k=i+1

    root.update()
    if str(check_info_as_st):
        for i in range(0, len((check_info_as_st))):
            temp = ""
            for j in range(1, len((check_info_as_st[i]))):
                if j==6:
                    temp+="помилка: "
                temp += str(check_info_as_st[i][j]) + " "

            label = tk.Label(scrollable_frame, text=temp)
            label.grid(row=k + 1, column=0, pady=5)
            k+=1
    root.update()
