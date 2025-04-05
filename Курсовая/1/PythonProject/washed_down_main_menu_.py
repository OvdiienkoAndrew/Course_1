# -*- coding: utf-8 -*-
import sqlite3
import tkinter as tk
import os


from resources import loading_window

class Totals:
    def __init__(self):
        self.total_first_semester = 0
        self.total_second_semester = 0
        self.total_academic_year = 0
        self.counter = 0



def on_button_click(root, name_db):
    root.withdraw()
    loading = loading_window(root)

    conn = sqlite3.connect(name_db)
    cursor = conn.cursor()
    job_info = cursor.execute("SELECT * FROM РОБОЧА_ІНФОРМАЦІЯ").fetchall()
    person_info = cursor.execute("SELECT * FROM ЛЮДСЬКА_ІНФОРМАЦІЯ").fetchall()
    vacancy_info = cursor.execute("SELECT * FROM ІНФОРМАЦІЯ_ВАКАНСІЯ").fetchall()
    first_semester_info = cursor.execute("SELECT * FROM ПЕРШИЙ_СЕМЕСТР").fetchall()
    second_semester_info = cursor.execute("SELECT * FROM ДРУГИЙ_СЕМЕСТР").fetchall()
    academic_year_info = cursor.execute("SELECT * FROM АКАДЕМІЧНИЙ_РІК").fetchall()
    code_and_year_info = cursor.execute("SELECT * FROM КОД_РІК").fetchall()
    conn.close()

    path_to_file_txt = "resources/середнє навантаження на посаду/result.txt"

    if os.path.exists(path_to_file_txt):
        os.remove(path_to_file_txt)


    people = (Totals(),Totals(),Totals(),Totals(),Totals(),Totals(),Totals())
    i=-1
    for helper in job_info:
        i+=1

        if str(helper[1]) == "заф. кафедри":
            people[0].counter+=1
            people[0].total_first_semester+=float(first_semester_info[i][22])
            people[0].total_second_semester+=float(second_semester_info[i][22])
            people[0].total_academic_year+=float(academic_year_info[i][22])
            position = "заф. кафедри"
        elif  str(helper[1]) == "професор":
            people[1].counter += 1
            people[1].total_first_semester += float(first_semester_info[i][22])
            people[1].total_second_semester += float(second_semester_info[i][22])
            people[1].total_academic_year += float(academic_year_info[i][22])
            position = "професор"
        elif str(helper[1]) == "доцент":
            people[2].counter += 1
            people[2].total_first_semester += float(first_semester_info[i][22])
            people[2].total_second_semester += float(second_semester_info[i][22])
            people[2].total_academic_year += float(academic_year_info[i][22])
            position = "доцент"
        elif str(helper[1]) == "ст. викладач":
            people[3].counter += 1
            people[3].total_first_semester += float(first_semester_info[i][22])
            people[3].total_second_semester += float(second_semester_info[i][22])
            people[3].total_academic_year += float(academic_year_info[i][22])
            position = "ст. викладач"
        elif str(helper[1]) == "асистент":
            people[4].counter += 1
            people[4].total_first_semester += float(first_semester_info[i][22])
            people[4].total_second_semester += float(second_semester_info[i][22])
            people[4].total_academic_year += float(academic_year_info[i][22])
            position = "асистент"
        elif str(helper[1]) == "в.о. заф. кафедри":
                people[5].counter += 1
                people[5].total_first_semester += float(first_semester_info[i][22])
                people[5].total_second_semester += float(second_semester_info[i][22])
                people[5].total_academic_year += float(academic_year_info[i][22])
                position = "в.о. заф. кафедри"
        elif str(helper[1]) == "викладач":
                people[6].counter += 1
                people[6].total_first_semester += float(first_semester_info[i][22])
                people[6].total_second_semester += float(second_semester_info[i][22])
                people[6].total_academic_year += float(academic_year_info[i][22])
                position = "викладач"

    for person in people:
        if float(person.counter) == 0:
            person.total_first_semester = 0
            person.total_second_semester =0
            person.total_academic_year =0
            continue

        person.total_first_semester = round(float(person.total_first_semester)/float(person.counter),2)
        person.total_second_semester = round(float(person.total_second_semester) / float(person.counter),2)
        person.total_academic_year = round(float(person.total_academic_year) / float(person.counter),2)

    with open(path_to_file_txt, "a") as file:
        file.write(f"Середнє значення у годинах (заф. кафедри):\n\tперший семестр: {people[0].total_first_semester}\n\tдругий семестр: {people[0].total_second_semester}\n\tрік {people[0].total_academic_year}\n\n")
        file.write(f"Середнє значення у годинах (професор):\n\tперший семестр: {people[1].total_first_semester}\n\tдругий семестр: {people[1].total_second_semester}\n\tрік {people[1].total_academic_year}\n\n")
        file.write(f"Середнє значення у годинах (доцент):\n\tперший семестр: {people[2].total_first_semester}\n\tдругий семестр: {people[2].total_second_semester}\n\tрік {people[2].total_academic_year}\n\n")
        file.write(f"Середнє значення у годинах (ст. викладач):\n\tперший семестр: {people[3].total_first_semester}\n\tдругий семестр: {people[3].total_second_semester}\n\tрік {people[3].total_academic_year}\n\n")
        file.write(f"Середнє значення у годинах (асистент):\n\tперший семестр: {people[4].total_first_semester}\n\tдругий семестр: {people[4].total_second_semester}\n\tрік {people[4].total_academic_year}\n\n")
        file.write(f"Середнє значення у годинах (в.о. заф. кафедри):\n\tперший семестр: {people[5].total_first_semester}\n\tдругий семестр: {people[5].total_second_semester}\n\tрік {people[5].total_academic_year}\n\n")
        file.write(f"Середнє значення у годинах (викладач):\n\tперший семестр: {people[6].total_first_semester}\n\tдругий семестр: {people[6].total_second_semester}\n\tрік {people[6].total_academic_year}\n\n")

    loading.destroy()
    root.deiconify()
    washed_down_main_menu(root, name_db)

def washed_down_main_menu(root,name_db):
    from error_menu_ import error_menu
    from change_main_menu_button_click_ import change_main_menu_button_click
    from main_menu_ import main_menu
    from washed_down_main_menu_ import washed_down_main_menu

    root.title("Запити")
    for widget in root.winfo_children():
        widget.destroy()

    change_settings = tk.Button(root, text="Відкрити налаштування", command=lambda: change_main_menu_button_click(root,name_db))
    error_window = tk.Button(root, text="Вікно помилок", command=lambda: error_menu(root,name_db), fg="red")
    main_menu_window = tk.Button(root, text="Головне меню", command=lambda: main_menu(root,name_db))
    washed_down_window = tk.Button(root, text="Запити", command=lambda: washed_down_main_menu(root,name_db))

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

    button = tk.Button(root, text="Створити файл середнього навчального навантаження на посаду", command=lambda: on_button_click(root,name_db))
    button.pack(expand=True)

