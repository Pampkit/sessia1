import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk


def product(login_window, name, surname, role):
    def go_to_login():
        product_window.destroy()
        login_window.deiconify()

    def add_product_at_db(article, name, category, quantity_in_stock, manufacturer, cost, photo, description,
                          window):
        connection = mysql.connector.connect(
            host="localhost",
            user="alisa",
            password="alisa24462",
            database="demo"
        )
        print("Connection to MySQL DB successful")
        cursor = connection.cursor()
        val = (article, name, description, category, photo, manufacturer, cost, 0, quantity_in_stock, 0)
        sql = ("INSERT INTO Product(ProductArticleNumber, ProductName, ProductDescription, ProductCategory, "
               "ProductPhoto, ProductManufacturer, ProductCost, ProductDiscountAmount, ProductQuantityInStock, "
               "ProductStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        cursor.execute(sql, val)
        connection.commit()
        connection.close()
        window.destroy()

    def add_product_window():
        add_window = tk.Toplevel(product_window)
        add_window.geometry('500x500')

        article_label = tk.Label(add_window, text='Артикул')
        article_label.pack()
        article_entry = tk.Entry(add_window)
        article_entry.pack()

        name_label = tk.Label(add_window, text='Наименование')
        name_label.pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        category_label = tk.Label(add_window, text='Категория')
        category_label.pack()
        category_entry = tk.Entry(add_window)
        category_entry.pack()

        quantity_in_stock_label = tk.Label(add_window, text='Количество на складе')
        quantity_in_stock_label.pack()
        quantity_in_stock_entry = tk.Entry(add_window)
        quantity_in_stock_entry.pack()

        manufacturer_label = tk.Label(add_window, text='Производитель')
        manufacturer_label.pack()
        manufacturer_entry = tk.Entry(add_window)
        manufacturer_entry.pack()

        cost_label = tk.Label(add_window, text='Стоимость')
        cost_label.pack()
        cost_entry = tk.Entry(add_window)
        cost_entry.pack()

        photo_label = tk.Label(add_window, text='Изображение')
        photo_label.pack()
        photo_entry = tk.Entry(add_window)
        photo_entry.pack()

        description_label = tk.Label(add_window, text='Описание')
        description_label.pack()
        description_entry = tk.Entry(add_window)
        description_entry.pack()

        add_button = tk.Button(add_window, text='Добавить',
                               command=lambda: add_product_at_db(article_entry.get(), name_entry.get(),
                                                                 category_entry.get(),
                                                                 quantity_in_stock_entry.get(),
                                                                 manufacturer_entry.get(),
                                                                 cost_entry.get(), photo_entry.get(),
                                                                 description_entry.get(), add_window))

        add_button.pack()
        add_window.transient(product_window)
        add_window.grab_set()
        add_window.focus_set()
        add_window.wait_window()

    def sorted_items(val, data):
        if val == 'up':  # сортировка элементов по возрастанию
            data = sorted(data, key=lambda x: x[3])
        else:  # сортировка элементов по убыванию
            data = sorted(data, key=lambda x: x[3], reverse=True)
        return data

    def search_items(search_name,data):
        filter_data = []
        for item in data:
            if search_name.lower() in item[1].lower():
                filter_data.append(item)
        return filter_data

    def load_products(val=None, search_entry=None):

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
        cursor.execute("SELECT ProductPhoto, ProductName, ProductDescription, ProductCost, ProductQuantityInStock "
                       "FROM Product")

        # Получаем все строки с товарами
        products = cursor.fetchall()
        products = sorted(products, key=lambda x: x[1])
        if val is not None:
            products = sorted_items(val, products)

        if search_entry is not None:
            print(search_entry.get())
            search_name = search_entry.get()
            products = search_items(search_name, products)

        scrollbar.pack(side='right', fill='y', pady=40)
        canvas.delete(tk.ALL)
        canvas.config(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True, pady=40)
        scrollbar.config(command=canvas.yview)

        frame_container = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_container, anchor='nw')
        for product in products:
            frame = tk.Frame(frame_container, relief='solid')
            frame.pack(anchor='w', fill='both')
            fi = product[0].decode('utf-8')
            if fi == 'xxxxx':
                fi = 'B538G6.jpg'
            image = Image.open('Товар_import/' + fi)
            image = image.resize((50, 50))
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(frame, image=image)
            image_label.image = image

            image_label.grid(row=0, column=0, rowspan=4)

            name = tk.Label(frame, text=f'{product[1]}')
            name.grid(row=0, column=1, sticky="w")

            info = tk.Label(frame, text=f'{product[2]}')
            info.grid(row=1, column=1, sticky="w")

            cost = tk.Label(frame, text=f'{product[3]}')
            cost.grid(row=2, column=1, sticky="w")

            amount = tk.Label(frame, text=f'{product[4]}')
            amount.grid(row=1, column=2, sticky="e")

            frame_container.update_idletasks()
            canvas.config(scrollregion=canvas.bbox('all'))

        connection.close()

    product_window = tk.Toplevel()
    product_window.title('Список товаров')
    product_window.geometry('780x900')
    # если на линухе, то
    # product_window.geometry('1500x900')

    canvas = tk.Canvas(product_window, width=800, height=400)
    scrollbar = tk.Scrollbar(product_window, orient='vertical')

    # Создаем кнопку назад
    back_button = tk.Button(product_window, text="Назад", command=go_to_login)
    back_button.pack(anchor="nw", pady=10, padx=10, side='left')

    name_lab = tk.Label(product_window, text=f'{name} {surname} ({role})')
    name_lab.pack(anchor='ne', pady=10, padx=10, side='right')
    if role == 'Администратор':
        add_prod_button = tk.Button(product_window, text='Добавить товар', command=add_product_window)
        add_prod_button.pack(anchor='n', pady=10)

    update_button = tk.Button(product_window, text='Обновить данные', command=load_products)
    update_button.pack(anchor='nw', padx=10, pady=10)

    frame = tk.Frame(product_window, borderwidth=1)

    # ----------------------------SEARCH-----------------------------------
    search_label = tk.Label(frame, text='Поиск')
    search_label.pack(anchor='nw')
    search_entry = tk.Entry(frame)
    search_entry.pack(anchor='nw', side='left')


    search_button = tk.Button(frame, text="Найти",command=lambda: load_products(search_entry=search_entry))
    search_button.pack(anchor='nw', padx=4, side='left')



    # ----------------------------SORT-----------------------------------
    up = 'up'
    down = 'down'
    lang = tk.StringVar(value=up)
    choice = ''

    def sel():
        nonlocal choice
        choice = lang.get()
        print(choice)

    up_btn = tk.Radiobutton(frame, text=up, value=up, variable=lang, command=sel)
    up_btn.pack(anchor='ne', side='right')

    down_btn = tk.Radiobutton(frame, text=down, value=down, variable=lang, command=sel)
    down_btn.pack(anchor='ne', side='right')

    sort_button = tk.Button(frame, text='Сортировка по цене', command=lambda: load_products(choice))
    sort_button.pack(anchor='ne', side='right')

    frame.pack(anchor='nw', fill='x')

    load_products()
    product_window.mainloop()
