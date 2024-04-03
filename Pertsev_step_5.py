# підключення необхідних бібліотек
import cv2
import numpy as np

sources = {'video1': "video1.mp4", 'video2': "video2.mp4", "web": 0}# Словник із джерелами відео


# функція виділення меж canny
def canny_edge_detection(image, t_lower=100, t_upper=200): 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Перетворення зображення в відтінки сірого
    edge = cv2.Canny(gray_image, t_lower, t_upper) # Використання алгоритму Canny для виявлення граней
    return edge


def main():
    cap = cv2.VideoCapture(sources.get('video1')) # Відкриття відеофайлу для читання
    # Перевірка готовності веб-камери
    while cap.isOpened():
        # Запис фреймів
        ret, frame = cap.read() # Зчитування кадру з відеопотоку
        # При виникненні помилці запису
        if not ret:
            print("Frame recording error!") # Виведення повідомлення про помилку запису
            break

        # Виконання операції за варіантом
        frame_changed = canny_edge_detection(frame, t_lower=100, t_upper=200)
        # Створення та налаштування вікон відображення
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 400, 350)
        cv2.namedWindow('frame_changed', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_changed', 400, 350)
        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame_changed', frame_changed)
        if cv2.waitKey(25) == ord('q'): # Перевірка натискання клавіші 'q' для виходу з циклу
            break
    # Завершуємо запис у кінці роботи
    cap.release()
    cv2.destroyAllWindows()


# при запуску як головного файлу
if __name__ == '__main__':
    main()
