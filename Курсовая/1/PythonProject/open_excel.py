# -*- coding: utf-8 -*-
from tkinter import messagebox, filedialog
from resources import loading_window
import sqlite3
import pandas as pd
import numpy as np
def get_cell_str(df, i, j):
    j-=1
    i-=1
    if df.iloc[i, j] is None or pd.isna(df.iloc[i, j]):
        return ""
    return str(df.iloc[i, j])

def empty_cell_number(df, i, j):
    j-=1
    i-=1
    try:
        A = float(str(df.iloc[i, j]).replace(' ','').replace(',','.'))
    except Exception:
        return 0

    if df.iloc[i, j] is None or pd.isna(df.iloc[i, j]) or str(df.iloc[i, j]) == str(np.nan):
        return 0.00
    return round(float(str(df.iloc[i, j]).replace(' ',"").replace(',','.')),3)

def empty_cell(df, i, j):
    j-=1
    i-=1
    if df.iloc[i, j] is None or pd.isna(df.iloc[i, j]):
        return True
    return False

def get_numbers(df,i):
    return [empty_cell_number(df, i, j) for j in range(9, 28)]

def empty_file(df,i):
    for j in range(i,1048576):
        if empty_cell(df, j, 1):
            continue
        else:
            return False
    return True

def bid_and_sign_of_madness(df, i):
    number = 0.00
    string = ""
    helper = get_cell_str(df, i, 4).lower().replace(' ',"").replace(',','.')

    index = 0
    while index < len(helper) and (helper[index]=='.' or helper[index]=='0' or helper[index]=='1' or helper[index]=='2' or helper[index]=='3' or helper[index]=='4' or helper[index]=='5' or helper[index]=='6' or helper[index]=='7' or helper[index]=='8' or helper[index]=='9'):
        index += 1

    if index == 0:
        return 0.00, ""

    number = round(float(helper[:index]),3)
    string = helper[index:]

    if len(string) > 0:
        string = "сум."


    return number, string

def open_button_click(root,name_db):

    files = filedialog.askopenfilenames(
        title="Оберіть Excel файл",
        filetypes=[("Excel Files", "*.xlsx")]
    )

    if files == "":
        messagebox.showinfo("Помилка", "Файл не обрано або має валідну помилку в назві!")
        return

    loading = loading_window(root)

    for file in files:

        try:
            df = pd.read_excel(file, sheet_name="Загальна", engine="openpyxl", header=None)
        except Exception:
            loading.destroy()
            messagebox.showinfo("Помилка", f"Лист: \"Загальна\" - не знайдено!\nФайл: {file}")
            continue

        name_of_the_department = ""  # назва кафедри
        year = ""  # роки
        helper = get_cell_str(df, 3, 1).replace(' ', "")
        i = 0
        try:
            while helper[i] != '(':
                i += 1
        except Exception:
            loading.destroy()
            messagebox.showinfo("Помилка", f"У комірці А3 не знайдено назву кафедри, яка має бути у круглих дужках\nФайл: {file}")
            return
        i += 1
        try:
            while helper[i] != ')':
                name_of_the_department += helper[i]
                i+=1
        except Exception:
            loading.destroy()
            messagebox.showinfo("Помилка", f"У комірці А3 не знайдено назву кафедри, яка має бути у круглих дужках.\nФайл: {file}")
            return
        i = 0
        while i < len(helper) and helper[i] != '1' and helper[i] != '2' and helper[i] != '3' and helper[i] != '4' and helper[i] != '5' and helper[i] != '6' and helper[i] != '7' and helper[i] != '8' and helper[i] != '9' and helper[i] != '0':
            i += 1
        while i < len(helper) and (helper[i] == '1' or helper[i] == '2' or helper[i] == '3' or helper[i] == '4' or helper[i] == '5' or helper[i] == '6' or helper[i] == '7' or helper[i] == '8' or helper[i] == '9' or helper[i] == '-' or helper[i] == '0'):
            year += helper[i]
            i += 1

        conn = sqlite3.connect(name_db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM КОД_РІК WHERE назва_кафедри = ? AND роки = ? LIMIT 1",
            (name_of_the_department, year)
        )

        exists = cursor.fetchone() is not None

        if exists:
            loading.destroy()

            result = messagebox.askyesno("Попередження", "Перезаписати дані для кафедри "+name_of_the_department+" "+year+" років?")
            loading = loading_window(root)

            if result:

                with sqlite3.connect(name_db) as db:
                    cursor = db.cursor()
                    cursor.execute("PRAGMA foreign_keys = ON")


                    try:
                        while True:
                            cursor.execute("""
                                                SELECT "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" 
                                                FROM КОД_РІК 
                                                WHERE "назва_кафедри"=? AND "роки"=?
                                            """, (name_of_the_department, year))

                            result = cursor.fetchone()

                            if result:
                                work_info_id = result[0]
                                cursor.execute("DELETE FROM РОБОЧА_ІНФОРМАЦІЯ WHERE id=?", (work_info_id,))
                                db.commit()
                            else:
                                break
                    except Exception:
                        cursor.close()
                        db.close()
            else:
                cursor.close()
                loading.destroy()
                return



        with sqlite3.connect(name_db) as db:
            cursor = db.cursor()
            job_info = """
                                    INSERT INTO РОБОЧА_ІНФОРМАЦІЯ (посада, вчене_звання_вчена_ступінь)
                                    VALUES (?, ?)
                                    """
            person_info = """
                                    INSERT INTO ЛЮДСЬКА_ІНФОРМАЦІЯ ("ім'я", "прізвище","по-батькові", "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ")
                                    VALUES (?, ?, ?, ?)
                                    """
            vacancy_info = """
                                    INSERT INTO ІНФОРМАЦІЯ_ВАКАНСІЯ ("назва", "номер", "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ")
                                    VALUES (?, ?,?)
                                    """
            first_semester_info = """
                                    INSERT INTO ПЕРШИЙ_СЕМЕСТР  ("ставка", "знак_сумісності", "лекції", "практичні_(семінарські)_заняття", "лабораторні_роботи", "екзамени", "консультації_перед_екзаменами", "заліки", "кваліфікаційна_робота", "атестаційний_екзамен", "виробнича_практика", "навчальна_практика", "поточні_консультації", "індивідуальні", "курсові_роботи", "аспірантські_екзамени", "керівництво_аспірантами", "консультування_докторантів_здобувачів", "керівництво_ФПК", "робота_приймальної_комісії", "інше", "всього", "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ")
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                    """
            second_semester_info = """
                                    INSERT INTO ДРУГИЙ_СЕМЕСТР ("ставка", "знак_сумісності", "лекції", "практичні_(семінарські)_заняття", "лабораторні_роботи", "екзамени", "консультації_перед_екзаменами", "заліки", "кваліфікаційна_робота", "атестаційний_екзамен", "виробнича_практика", "навчальна_практика", "поточні_консультації", "індивідуальні", "курсові_роботи", "аспірантські_екзамени", "керівництво_аспірантами", "консультування_докторантів_здобувачів", "керівництво_ФПК", "робота_приймальної_комісії", "інше", "всього", "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ")
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                    """
            academic_year_info = """
                                    INSERT INTO АКАДЕМІЧНИЙ_РІК ("ставка", "знак_сумісності", "лекції", "практичні_(семінарські)_заняття", "лабораторні_роботи", "екзамени", "консультації_перед_екзаменами", "заліки", "кваліфікаційна_робота", "атестаційний_екзамен", "виробнича_практика", "навчальна_практика", "поточні_консультації", "індивідуальні", "курсові_роботи", "аспірантські_екзамени", "керівництво_аспірантами", "консультування_докторантів_здобувачів", "керівництво_ФПК", "робота_приймальної_комісії", "інше", "всього", "розподіл_ставок_навчального_навантаження" ,"посилання_на_РОБОЧУ_ІНФОРМАЦІЮ")
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                    """
            code_year_info = """
                                    INSERT INTO КОД_РІК("назва_кафедри", "роки", "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ")
                                    VALUES (?, ?, ?)
                                    """

            try:
                for i in range(7,1048576):
                    print(i)
                    if empty_file(df, i):
                       break
                    if empty_cell(df, i, 1):
                        continue

                    helper = str(get_cell_str(df, i, 1)).lower().replace(' ', '')

                    was =True
                    try:
                        helper = int(helper)

                    except Exception:
                        was =False

                    if was is False:
                        continue


                    helper = get_cell_str(df,i,2)
                    name = ""  # ім'я
                    surname = ""  # прізвище
                    patronymic= ""  # по батькові
                    parts = helper.split()
                    if len(parts) >= 1:
                        surname = parts[0]
                        if len(parts) >= 2:
                            name = parts[1]
                        if len(parts) >= 3:
                            patronymic = parts[2]
                    vacancy = ""  # вакансія
                    vacancy_number = ""  # номер вакансії
                    helper = helper.replace(' ', "").lower()
                    if len(helper) <= 8:
                        continue

                    if helper[0] == 'в' and helper[1] == 'а' and helper[2] == 'к' and helper[3] == 'а' and helper[
                        4] == 'н' and helper[5] == 'с' and helper[6] == 'і' and helper[7] == 'я' and (
                            helper[8] == ' ' or helper[8] == '1' or helper[8] == '2' or helper[8] == '3' or helper[
                        8] == '4' or helper[8] == '5' or helper[8] == '6' or helper[8] == '7' or helper[8] == '8' or helper[
                                8] == '9'):
                        vacancy = "Вакансія"
                        name = ""
                        surname = ""
                        patronymic = ""
                        temp = helper[8:]
                        vacancy_number = int(temp)
                    else:
                        vacancy = ""
                        vacancy_number = ""
                        if patronymic == "":
                            continue

                    position = ""  # посада
                    academic_title_academic_degree = ""  # вчене звання, вчена ступінь
                    helper = get_cell_str(df,i,3)
                    helper2 = helper.lower().replace(' ', "")
                    if helper2[0] == 'з':
                        position = "заф. кафедри"
                    elif helper2[0] == 'п':
                        position = "професор"
                    elif helper2[0] == 'д':
                        position = "доцент"
                    elif helper2[0] == 'с':
                        position = "ст. викладач"
                    elif helper2[0] == 'а':
                        position = "асистент"
                    elif helper2[0] == 'в':
                        if helper2[1] == '.':
                            position = "в.о. заф. кафедри"
                        else:
                            position = "викладач"

                    if position == "":
                        academic_title_academic_degree = helper

                    else:
                        j = helper.find(',')
                        j += 1
                        if j == 0:
                            j = len(helper)
                        while j < len(helper):
                            academic_title_academic_degree += helper[j]
                            j += 1


                    distribution_of_teaching_workload_rates_helper =  get_cell_str(df,i+2,29)
                    if distribution_of_teaching_workload_rates_helper == "" or distribution_of_teaching_workload_rates_helper is None or distribution_of_teaching_workload_rates_helper == "None":
                        distribution_of_teaching_workload_rates_helper = ""


                    first_semester_numbers = get_numbers(df,i)
                    first_semester_total = 0
                    for j in first_semester_numbers:
                        first_semester_total += j


                    second_semester_numbers = get_numbers(df,i+1)
                    second_semester_total = 0
                    for j in second_semester_numbers:
                        second_semester_total += j

                    academic_year_numbers =  [first_semester_numbers[j]+second_semester_numbers[j] for j in range(len(first_semester_numbers))]
                    academic_year_total = 0
                    for j in academic_year_numbers:
                        academic_year_total += j

                    first_semester_bid ,first_semester_sign_of_madness = bid_and_sign_of_madness(df, i)     # ставка і ознака сумісності
                    second_semester_bid, second_semester_sign_of_madness = bid_and_sign_of_madness(df, i+1) # ставка і ознака сумісності
                    academic_year_bid, academic_year_sign_of_madness = bid_and_sign_of_madness(df, i+2)     # ставка і ознака сумісності

                    was = False
                    try:
                        cursor.execute("""
                            SELECT 1 
                            FROM ЛЮДСЬКА_ІНФОРМАЦІЯ 
                            WHERE "ім'я" = ? AND "прізвище" = ? AND "по-батькові" = ?
                        """, (name, surname, patronymic))


                        if cursor.fetchone():

                            cursor.execute("""
                                SELECT 1
                                FROM ІНФОРМАЦІЯ_ВАКАНСІЯ iv
                                JOIN ЛЮДСЬКА_ІНФОРМАЦІЯ li ON li."посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" = iv."посилання_на_РОБОЧУ_ІНФОРМАЦІЮ"
                                WHERE li."ім'я" = ? AND li."прізвище" = ? AND li."по-батькові" = ?
                                  AND iv."назва" = ? AND iv."номер" = ?
                            """, (name, surname, patronymic, vacancy, vacancy_number))

                            if cursor.fetchone():

                                cursor.execute("""
                                    SELECT 1
                                    FROM РОБОЧА_ІНФОРМАЦІЯ iv
                                    JOIN ЛЮДСЬКА_ІНФОРМАЦІЯ li ON li."посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" = iv."id"
                                     WHERE li."ім'я" = ? AND li."прізвище" = ? AND li."по-батькові" = ?
                                     AND iv."посада" = ? AND iv."вчене_звання_вчена_ступінь" = ?
                                """, (name, surname, patronymic, position,academic_title_academic_degree ))

                                if cursor.fetchone():

                                        cursor.execute("""
                                            SELECT 1
                                            FROM КОД_РІК iv
                                            JOIN ЛЮДСЬКА_ІНФОРМАЦІЯ li ON li."посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" = iv."посилання_на_РОБОЧУ_ІНФОРМАЦІЮ"
                                            WHERE li."ім'я" = ? AND li."прізвище" = ? AND li."по-батькові" = ?
                                            AND iv."назва_кафедри" = ? AND iv."роки" = ?
                                            """,(name, surname, patronymic, name_of_the_department, year ))

                                        if cursor.fetchone():
                                            cursor.execute("""
                                                SELECT 1
                                                FROM АКАДЕМІЧНИЙ_РІК iv
                                                JOIN ЛЮДСЬКА_ІНФОРМАЦІЯ li ON li."посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" = iv."посилання_на_РОБОЧУ_ІНФОРМАЦІЮ"
                                                WHERE li."ім'я" = ? AND li."прізвище" = ? AND li."по-батькові" = ?
                                                AND iv."знак_сумісності" = ? 
                                                """, (name, surname, patronymic, academic_year_sign_of_madness))

                                            if cursor.fetchone():
                                                was=True


                    except Exception:
                        was = False

                    if was == True:

                        messagebox.showwarning("Попередження", f"{surname} {name} {patronymic}\n{vacancy} {vacancy_number}\n{position} {academic_year_sign_of_madness} {name_of_the_department} {year}\nЯ вже бачив цю людину і не заношу її до бд!\nЯкби ця людина була в одному випадку сумісником, а в іншому ні - то це повідомлення не висвітилося.\n")
                        continue

                    cursor.execute(job_info, (position, academic_title_academic_degree))
                    job_info_id = cursor.lastrowid
                    cursor.execute(person_info, (name, surname, patronymic, job_info_id))
                    cursor.execute(vacancy_info, (vacancy, vacancy_number, job_info_id))
                    cursor.execute(first_semester_info, (first_semester_bid, first_semester_sign_of_madness,first_semester_numbers[0],first_semester_numbers[1],first_semester_numbers[2],first_semester_numbers[3],first_semester_numbers[4],first_semester_numbers[5],first_semester_numbers[6],first_semester_numbers[7],first_semester_numbers[8],first_semester_numbers[9],first_semester_numbers[10],first_semester_numbers[11],first_semester_numbers[12],first_semester_numbers[13],first_semester_numbers[14],first_semester_numbers[15],first_semester_numbers[16],first_semester_numbers[17],first_semester_numbers[18],first_semester_total, job_info_id))
                    cursor.execute(second_semester_info, (second_semester_bid, second_semester_sign_of_madness,second_semester_numbers[0],second_semester_numbers[1],second_semester_numbers[2],second_semester_numbers[3],second_semester_numbers[4],second_semester_numbers[5],second_semester_numbers[6],second_semester_numbers[7],second_semester_numbers[8],second_semester_numbers[9],second_semester_numbers[10],second_semester_numbers[11],second_semester_numbers[12],second_semester_numbers[13],second_semester_numbers[14],second_semester_numbers[15],second_semester_numbers[16],second_semester_numbers[17],second_semester_numbers[18],second_semester_total, job_info_id))
                    cursor.execute(academic_year_info, (academic_year_bid, academic_year_sign_of_madness,academic_year_numbers[0],academic_year_numbers[1],academic_year_numbers[2],academic_year_numbers[3],academic_year_numbers[4],academic_year_numbers[5],academic_year_numbers[6],academic_year_numbers[7],academic_year_numbers[8],academic_year_numbers[9],academic_year_numbers[10],academic_year_numbers[11],academic_year_numbers[12],academic_year_numbers[13],academic_year_numbers[14],academic_year_numbers[15],academic_year_numbers[16],academic_year_numbers[17],academic_year_numbers[18], academic_year_total, distribution_of_teaching_workload_rates_helper,job_info_id))
                    cursor.execute(code_year_info, (name_of_the_department, year, job_info_id))
                    db.commit()

            except Exception:

                continue


    loading.destroy()