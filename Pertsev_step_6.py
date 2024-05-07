# підключення необхідних бібліотек
import cv2
import numpy as np

sources = {'video1': "video1.mp4", 'video2': "video2.mp4", "web": 0} # Словник із джерелами відео


# Білатеральний фільтр
def bilateral_filtration(image, filter_size=9, sigmaValues=75):
    return cv2.bilateralFilter(image, filter_size, sigmaValues, sigmaValues)


def main():
    cap = cv2.VideoCapture(sources.get('web')) # Відкриття відеофайлу для читання
    # Перевірка готовності веб-камери
    while cap.isOpened():
        # Запис фреймів
        ret, frame = cap.read()
        # При виникненні помилці запису
        if not ret:
            print("Frame recording error!") # Виведення повідомлення про помилку запису
            break

        # Виконання операції за варіантом
        frame_changed1 = bilateral_filtration(frame, filter_size=9, sigmaValues=75)
        frame_changed2 = bilateral_filtration(frame, filter_size=10, sigmaValues=150)
        frame_changed3 = bilateral_filtration(frame, filter_size=2, sigmaValues=1)
        # Створення та налаштування вікон відображення
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 400, 350)
        cv2.namedWindow('frame_changed1', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_changed1', 400, 350)
        cv2.namedWindow('frame_changed2', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_changed2', 400, 350)
        cv2.namedWindow('frame_changed3', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_changed3', 400, 350)
        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame_changed1', frame_changed1)
        cv2.imshow('frame_changed2', frame_changed2)
        cv2.imshow('frame_changed3', frame_changed3)
        if cv2.waitKey(25) == ord('q'):  # Перевірка натискання клавіші 'q' для виходу з циклу
            break
    # Завершуємо запис у кінці роботи
    cap.release()
    cv2.destroyAllWindows()


# при запуску як головного файлу
if __name__ == '__main__':
    main()
