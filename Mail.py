from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import os

# Глобальные переменные для хранения изображений
original_image = None
current_image = None


def open_image():
    global current_image
    # Открытие диалогового окна для выбора изображения
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])

    # Загрузка и отображение изображения в окне Tkinter
    global original_image, current_image
    original_image = Image.open(file_path)
    current_image = original_image.copy()  # Создание копии изображения
    photo = ImageTk.PhotoImage(original_image)
    image_label.config(image=photo)
    image_label.image = photo


def save_image():
    global current_image
    # Проверка наличия выбранного изображения
    if current_image:
        # Открытие диалогового окна для выбора каталога сохранения
        save_directory = filedialog.askdirectory()

        # Генерация уникального имени файла
        file_name = "edited_image.jpg"

        # Полный путь к файлу
        save_path = os.path.join(save_directory, file_name)

        # Сохранение изображения
        current_image.save(save_path)


def restore_image():
    global current_image, original_image
    # Проверка наличия выбранного изображения
    if original_image:
        # Восстановление изображения до первоначального состояния
        current_image = original_image.copy()
        photo = ImageTk.PhotoImage(original_image)
        image_label.config(image=photo)
        image_label.image = photo


def apply_blur_filter():
    global current_image
    # Проверка наличия выбранного изображения
    if current_image:
        # Применение фильтра размытия (Blur) к текущему изображению
        blurred_image = current_image.filter(ImageFilter.BLUR)
        photo = ImageTk.PhotoImage(blurred_image)
        image_label.config(image=photo)
        image_label.image = photo
        # Обновление текущего изображения
        current_image = blurred_image


def apply_lighting_filter():
    global current_image
    # Проверка наличия выбранного изображения
    if current_image:
        # Применение фильтра реалистичности и эффекта лучей света к текущему изображению
        cv_image = cv2.cvtColor(np.array(current_image), cv2.COLOR_RGB2BGR)

        # Добавление реалистичности и эффекта лучей света
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        hsv_image[..., 1] = hsv_image[..., 1] * 0.8  # Уменьшение насыщенности
        hsv_image[..., 2] = hsv_image[..., 2] * 1.2  # Увеличение яркости
        cv_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        filtered_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

        photo = ImageTk.PhotoImage(filtered_image)
        image_label.config(image=photo)
        image_label.image = photo
        # Обновление текущего изображения
        current_image = filtered_image


def crop_image():
    global current_image
    # Проверка наличия выбранного изображения
    if original_image:
        # Открытие диалогового окна для ввода координат кадрирования
        crop_dialog = tk.Toplevel(window)
        crop_dialog.title("Кадрирование")

        x_label = tk.Label(crop_dialog, text="X:")
        x_label.grid(row=0, column=0)
        x_entry = tk.Entry(crop_dialog)
        x_entry.grid(row=0, column=1)

        y_label = tk.Label(crop_dialog, text="Y:")
        y_label.grid(row=1, column=0)
        y_entry = tk.Entry(crop_dialog)
        y_entry.grid(row=1, column=1)

        width_label = tk.Label(crop_dialog, text="Ширина:")
        width_label.grid(row=2, column=0)
        width_entry = tk.Entry(crop_dialog)
        width_entry.grid(row=2, column=1)

        height_label = tk.Label(crop_dialog, text="Высота:")
        height_label.grid(row=3, column=0)
        height_entry = tk.Entry(crop_dialog)
        height_entry.grid(row=3, column=1)

        def confirm_crop():
            # Получение введенных пользователем значений
            x = int(x_entry.get())
            y = int(y_entry.get())
            width = int(width_entry.get())
            height = int(height_entry.get())

            # Кадрирование изображения
            global current_image
            cropped_image = current_image.crop((x, y, x + width, y + height))
            photo = ImageTk.PhotoImage(cropped_image)
            image_label.config(image=photo)
            image_label.image = photo
            # Обновление текущего изображения
            current_image = cropped_image

            # Закрытие диалогового окна
            crop_dialog.destroy()

        confirm_button = tk.Button(crop_dialog, text="Подтвердить", command=confirm_crop)
        confirm_button.grid(row=4, columnspan=2)


def rotate_image():
    global current_image
    # Проверка наличия выбранного изображения
    if current_image:
        # Поворот изображения на 90 градусов по часовой стрелке
        current_image = current_image.rotate(-90)  # Используется отрицательный угол для поворота по часовой стрелке
        photo = ImageTk.PhotoImage(current_image)
        image_label.config(image=photo)
        image_label.image = photo


# Создание главного окна Tkinter
window = tk.Tk()
window.title("Фотошоп")

# Создание кнопки "Открыть изображение"
open_button = tk.Button(window, text="Открыть изображение", command=open_image)
open_button.pack()

# Создание кнопки "Применить размытие"
blur_button = tk.Button(window, text="Применить размытие", command=apply_blur_filter)
blur_button.pack()

# Создание кнопки "Применить реалистичность и лучи света"
lighting_button = tk.Button(window, text="Применить реалистичность и лучи света", command=apply_lighting_filter)
lighting_button.pack()

# Создание кнопки "Повернуть"
rotate_button = tk.Button(window, text="Повернуть", command=rotate_image)
rotate_button.pack()

# Создание кнопки "Кадрировать"
crop_button = tk.Button(window, text="Кадрировать", command=crop_image)
crop_button.pack()

# Создание кнопки "Восстановить"
restore_button = tk.Button(window, text="Восстановить", command=restore_image)
restore_button.pack()

# Создание кнопки "Сохранить"
save_button = tk.Button(window, text="Сохранить", command=save_image)
save_button.pack()

# Создание метки для отображения изображения
image_label = tk.Label(window)
image_label.pack()

# Запуск главного цикла обработки событий Tkinter
window.mainloop()
