import tkinter as tk
import sqlite3
from tkinter import messagebox


def login():
    username = username_entry.get().strip()

    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id_buyer FROM buyer WHERE name = ?", (username,))
    id_buyer = cursor.fetchall()[0][0]
    print(id_buyer,type(id_buyer))
    login_window.destroy()
    show_product_window(id_buyer)


def show_order_window(cart_items, id_buyer):
    order_window = tk.Tk()
    order_window.geometry('300x300')
    order_window.title("Оформление заказа")

    # Создайте и настройте виджеты для отображения выбранных товаров
    label = tk.Label(order_window, text="Выбранные товары:")
    label.pack()
    selected_items = []  # Список для хранения выбранных товаров
    arr_id = []

    for item in cart_items:
        item_label = tk.Label(order_window, text=item)
        item_label.pack()
        selected_items.append(item)  # Добавляем выбранный товар в список
    # Добавьте кнопку "Оформить заказ" (и другие элементы, если необходимо)
    order_button = tk.Button(order_window, text="Оформить заказ", command=lambda: complete_order(selected_items, id_buyer))
    order_button.pack()
    order_window.mainloop()




def complete_order(selected_items, id_buyer):
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()
    # Преобразуем массив cart_items в строку с разделителем (например, запятая)
    items_string = ",".join([str(item[0]) for item in selected_items])
    cursor.execute("INSERT INTO orders (id_buyer, id_product,sum) VALUES (?, ?, ?)", (id_buyer, items_string, 100))
    conn.commit()
    messagebox.showinfo("Сформирован заказ", "Заказ успешно сформирован.")
    conn.close()


# Функция для добавления выбранного элемента в корзину
def add_to_cart(item, button, cart_items):
    cart_items.append(item)
    messagebox.showinfo("Добавить в корзину", f"Добавлено в корзину: {item}")
    button.config(state=tk.NORMAL)


# Функция для открытия контекстного меню
def show_context_menu(event, listbox, context_menu, button, cart_items):
    selected_item = listbox.curselection()
    if selected_item:
        item_index = selected_item[0]  # Получаем индекс выбранного элемента
        item_text = listbox.get(item_index)  # Получаем текст выбранного элемента
        context_menu.delete(0, "end")  # Очищаем контекстное меню
        context_menu.add_command(label="Добавить в корзину", command=lambda: add_to_cart(item_text, button, cart_items))
        context_menu.post(event.x_root, event.y_root)


def show_product_window(id_buyer):
    product_window = tk.Tk()
    product_window.title('Список товаров')
    product_window.geometry('500x500')
    cart_items = []
    # Создаем кнопку
    button = tk.Button(product_window, text="Корзина", state=tk.DISABLED,
                       command=lambda: show_order_window(cart_items, id_buyer))
    button.pack(anchor='ne', pady=15, padx=15)

    # Создаем виджет списка для отображения товаров
    listbox = tk.Listbox(product_window, width=20, height=10)
    listbox.pack()
    listbox.config(font=("Arial", 12))

    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect("db.db")
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения списка товаров из базы данных
    cursor.execute("SELECT name, info, manufacturer, price FROM product")
    products = cursor.fetchall()

    # Добавляем товары в виджет списка
    for product in products:
        listbox.insert(tk.END, product)  # product[0] содержит название товара

    # Закрываем соединение с базой данных
    conn.close()
    # Создаем контекстное меню
    context_menu = tk.Menu(listbox, tearoff=0)
    listbox.bind("<Button-3>", lambda event: show_context_menu(event, listbox, context_menu, button, cart_items))

    product_window.mainloop()


# Создаем окно авторизации
login_window = tk.Tk()
login_window.geometry('500x500')
login_window.title("Авторизация")

# Создаем виджеты для ввода имени пользователя и пароля
username_label = tk.Label(login_window, text="Имя пользователя:")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

# Создаем кнопку для входа
login_button = tk.Button(login_window, text="Войти", command=login)
login_button.pack()

login_window.mainloop()
