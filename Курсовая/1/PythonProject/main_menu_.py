# -*- coding: utf-8 -*-
import sqlite3
import tkinter as tk

from database import creat_database
from show_data_base import show_button_click
from check_data_base import check_button_click
from open_excel import open_button_click
from tkinter import messagebox, ttk


def main_menu(root,name_db):
    from error_menu_ import error_menu
    from change_main_menu_button_click_ import change_main_menu_button_click
    from washed_down_main_menu_ import washed_down_main_menu

    root.title("Головне меню")
    for widget in root.winfo_children():
        widget.destroy()
    def download_click():
        root.withdraw()
        open_button_click(root,name_db)
        root.deiconify()


    def check_click():
        root.withdraw()
        check_button_click(root,name_db)
        root.deiconify()
        main_menu(root,name_db)


    def upload_click():
        root.withdraw()
        show_button_click(root,name_db)
        root.deiconify()

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
    washed_down_window.place(x=10 + change_settings.winfo_width() + 10 +10 +main_menu_window.winfo_width(), y=10)
    root.update()
    error_window.place \
        (x=10 + change_settings.winfo_width() + 10 + 10 + main_menu_window.winfo_width( ) +10 +washed_down_window.winfo_width(), y=10)
    root.update()


    download = tk.Button(root, text="Відкрити Excel файл", command=download_click)
    change_settings.winfo_width()
    check = tk.Button(root, text="Перевірити", command=check_click)
    upload = tk.Button(root, text="Завантажити дані з бази данних", command=upload_click)



    window_height = root.winfo_height() - 20 - main_menu_window.winfo_height()
    empty_window_height = (window_height - 3 * main_menu_window.winfo_height() ) /4
    window_brain = 20 +  main_menu_window.winfo_height()

    download.place(x=0 ,y=window_brain +empty_window_height)
    root.update()
    download.place(x=(root.winfo_width() - download.winfo_width()) / 2, y=window_brain + empty_window_height)
    root.update()

    check.place(x=0 ,y=window_brain +empty_window_height +download.winfo_height( ) +empty_window_height)
    root.update()
    check.place(x=(root.winfo_width() - check.winfo_width()) / 2, y=window_brain +empty_window_height +download.winfo_height( ) +empty_window_height)
    root.update()

    upload.place(x=0, y=window_brain +empty_window_height +download.winfo_height( ) +empty_window_height +check.winfo_height( ) +empty_window_height)
    root.update()
    upload.place(x=(root.winfo_width() - upload.winfo_width()) / 2
                 ,y=window_brain +empty_window_height +download.winfo_height( ) +empty_window_height +check.winfo_height( ) +empty_window_height)
    root.update()

    try:
        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()
        check_info = cursor.execute("SELECT * FROM ПЕРЕВІРКА").fetchall()
        check_info_as_st = cursor.execute("SELECT * FROM ПЕРЕВІРКА_АСИСТЕНТ_СТ_ВИКЛАДАЧ").fetchall()
        conn.close()
        if len(check_info ) +len(check_info_as_st) == 0:
            error_window.place(x=-100 ,y=-100)

    except Exception:
        error_window.place(x=-100, y=-100)


    root.mainloop()


