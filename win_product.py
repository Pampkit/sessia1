import io
import os
import tkinter as tk
import sqlite3

import mysql.connector
from PIL import Image, ImageTk


def product(login_window, name, surname, role):
    def go_to_login():
        product_window.destroy()
        login_window.deiconify()

    product_window = tk.Toplevel()
    product_window.title('Список товаров')
    product_window.geometry('500x500')

    # Создаем кнопку назад
    back_button = tk.Button(product_window, text="Назад", command=go_to_login)
    # back_button.grid(row=0, column=0, padx=10)
    back_button.pack(anchor="nw", pady=10, padx=10, side='left')

    name = tk.Label(product_window, text=f'{name} {surname} ({role})')
    # name.grid(row=0, column=1, padx=10, sticky='e')
    name.pack(anchor='ne', pady=10, padx=10, side='right')

    # listbox = tk.Listbox(product_window, width=50)
    # listbox.pack(pady=50)

    def load_products():
        # подключение к базе данных
        connection = mysql.connector.connect(
            host="localhost",
            user="alisa",
            password="alisa24462",
            database="demo"
        )
        print("Connection to MySQL DB successful")
        cursor = connection.cursor()

        # Запрос на выборку всех товаров из базы данных
        cursor.execute("SELECT ProductPhoto, ProductName, ProductCost FROM Product")

        # Получаем все строки с товарами
        products = cursor.fetchall()

        img_directory = r'C:\Users\alisa\PycharmProjects\sessia1\Товар_import'

        scrollbar = tk.Scrollbar(product_window, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(product_window, yscrollcommand=scrollbar.set)
        canvas.pack(expand=True, fill="both")
        scrollbar.config(command=canvas.yview)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        row_counter = 0  # Используйте счетчик строк для размещения виджетов в разных строках
        photo_list = []

        for filename in os.listdir(img_directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                img_path = os.path.join(img_directory, filename)
                img = Image.open(img_path)
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)

                photo_list.append(photo)

                # Создайте отдельные виджеты Label для текста и изображения
                text_label = tk.Label(frame, text=filename)
                image_label = tk.Label(frame, image=photo)

                # to prevent image from being garbage collected
                image_label.image = photo

                # Упакуйте виджеты Label внутри Frame с увеличением значения row
                text_label.grid(row=row_counter, column=1, sticky='w')  # Выравнивание текста слева
                image_label.grid(row=row_counter, column=0, sticky='e')  # Выравнивание изображения справа

                row_counter += 1  # Увеличьте значение row для следующей пары "текст + изображение"
        frame.update_idletasks()  # Обновите размеры канвы после добавления всех изображений
        canvas.config(scrollregion=canvas.bbox("all"))  # Подстройте размеры канвы под изображения

        canvas.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # for product in products:
        #     listbox.insert(tk.END,product[1])

        connection.close()

    load_products()

    product_window.mainloop()
