import tkinter as tk
import tkinter.messagebox
import mysql.connector
import win_product


def login():
    def go_to_list_product():
        login_str = login_entry.get()
        password_str = password_entry.get()

        connection = mysql.connector.connect(
            host="localhost",
            user="alisa",
            password="alisa24462",
            database="demo"
        )
        print("Connection to MySQL DB successful")
        cursor = connection.cursor()
        sql = ("SELECT UserRole, UserSurname, UserName FROM User WHERE UserLogin = %s and UserPassword = %s")
        val = (login_str, password_str)
        cursor.execute(sql, val)
        data = cursor.fetchall()
        if data == []:
            tk.messagebox.showinfo(message='Такого пользователя нет в базе')
        else:
            login_window.withdraw()
            print(data)
            role, surname, name = data[0]
            sql_r = ("SELECT RoleName FROM Role WHERE RoleID = %s")
            val_r = (role,)
            cursor.execute(sql_r, val_r)
            role = cursor.fetchall()[0][0]
            win_product.product(login_window, name, surname, role)
        connection.close()

    def go_to_like_guest():
        login_window.withdraw()
        win_product.product(login_window, 'Гость', '', 'Клиент')

    login_window = tk.Tk()
    login_window.geometry('500x500')
    login_window.title("Авторизация")

    # Создаем виджеты для ввода имени пользователя и пароля
    login_label = tk.Label(login_window, text="Логин:")
    login_label.pack()
    login_entry = tk.Entry(login_window)
    login_entry.pack()

    password_label = tk.Label(login_window, text="Пароль:")
    password_label.pack()
    password_entry = tk.Entry(login_window)
    password_entry.pack()

    # Создаем кнопку для входа
    login_button = tk.Button(login_window, text="Войти", command=go_to_list_product)
    login_button.pack(pady=15)

    # Создаем кнопку для входа
    skip_button = tk.Button(login_window, text="Продолжить как гость", command=go_to_like_guest)
    skip_button.pack()

    login_window.mainloop()

