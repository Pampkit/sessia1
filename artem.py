import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas
from PIL import Image, ImageTk
import os
import sqlite3

# Подключение к базе данных и создание таблиц
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(100),
        password VARCHAR(100)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100),
        photo VARCHAR
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

cursor.execute('''INSERT INTO users(username, password) VALUES ("1","1")''')
conn.commit()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Catalog")
        self.logged_in = False
        self.create_login_window()

    def create_login_window(self):
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Проверка логина и пароля в базе данных
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            self.logged_in = True
            self.clear_login_window()
            self.show_product_list()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def clear_login_window(self):
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.login_button.pack_forget()

    def show_product_list(self):
        img_directory = r'D:\SHA RA GA\Guti\LABRAB4\img'
        canvas = tk.Canvas(self.root)  # Используйте tk.Canvas
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        row_counter = 0  # Используйте счетчик строк для размещения виджетов в разных строках

        for filename in os.listdir(img_directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                img_path = os.path.join(img_directory, filename)
                cursor.execute('''INSERT INTO products(title, photo) VALUES (?,?)''', (filename, img_path))
                img = Image.open(img_path)
                img = img.resize((100, 100), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)

                # Создайте отдельные виджеты Label для текста и изображения
                text_label = tk.Label(frame, text=filename)
                image_label = tk.Label(frame, image=photo)

                # to prevent image from being garbage collected
                image_label.image = photo

                # Упакуйте виджеты Label внутри Frame с увеличением значения row
                text_label.grid(row=row_counter, column=1, sticky='w')  # Выравнивание текста слева
                image_label.grid(row=row_counter, column=0, sticky='e')  # Выравнивание изображения справа

                row_counter += 1  # Увеличьте значение row для следующей пары "текст + изображение"

                # Привязка контекстного меню
                context_menu = tk.Menu(image_label, tearoff=0)
                context_menu.add_command(label="Add to Cart",
                                         command=lambda filename=filename: self.add_to_cart(filename))
                image_label.bind("<Button-3>",
                                 lambda event, context_menu=context_menu: context_menu.post(event.x_root, event.y_root))
        conn.commit()

        frame.update_idletasks()  # Обновите размеры канвы после добавления всех изображений
        canvas.config(scrollregion=canvas.bbox("all"))  # Подстройте размеры канвы под изображения

    def add_to_cart(self, product_name):
        if self.logged_in:
            # Получить ID товара по имени
            cursor.execute("SELECT id FROM products WHERE title=?", (product_name,))
            product_id = cursor.fetchone()[0]

            # Добавить заказ в базу данных
            cursor.execute("INSERT INTO orders (product_id, user_id) VALUES (?, ?)", (
            product_id, 1))  # Здесь 1 - это ID пользователя, который вошел в систему (ваша логика входа пользователя)

            conn.commit()
            messagebox.showinfo("Success", "Product added to cart!")
        else:
            messagebox.showerror("Error", "Please login first.")


# (ваш существующий код создания таблиц)

root = tk.Tk()
app = App(root)
root.mainloop()

conn.close()

# Удаление файла базы данных после закрытия приложения
os.remove('shop.db')