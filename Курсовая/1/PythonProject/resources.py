from tkinter import Toplevel, Label

def loading_window(root):
    window = Toplevel(root)
    window.title("Завантаження")
    window.geometry("200x100")
    window.grab_set()
    Label(window, text="Завантаження...").pack(expand=True)
    root.update()
    return window


#  із строки виймаємо число та строку
def number_and_string_before_and_after(string):

    string = str(string).replace(' ', "")

    if len(string) <= 0 or string == "none":
        return 0, ""

    index = 0
    while index < len(string) and (string[index] == '0' or string[index] == '1' or string[index] == '2' or string[index] == '3' or string[index] == '4' or string[index] == '5' or string[index] == '6'or string[index] == '7' or string[index] == '8' or string[index] == '9' or string[index] == '.' or string[index] == ',' ):
        index += 1

    upload_number = string[:index].replace(' ', "").lower().replace(',', '.')
    upload_string = string[index:].replace(' ', "").lower()

    if upload_number == "none" or len(upload_number)<=0:
        return 0, ""

    if upload_string == "none" or len(upload_string)<=0:
        return round(float(upload_number),3), ""

    return round(float(upload_number),3), "сум"
