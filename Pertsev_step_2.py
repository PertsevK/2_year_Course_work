# підключення необхідних бібліотек
import cv2
sources = {'video1': "video1.mp4", 'video2': "video2.mp4", "web": 0} # Словник із джерелами відео

def main():
    cap = cv2.VideoCapture(sources.get('web')) # Відкриття відеофайлу для читання
    # Перевірка готовності веб-камери
    while cap.isOpened():
        # Запис фреймів
        ret, frame = cap.read() # Зчитування кадру з відеопотоку
        # При виникненні помилці запису
        if not ret:
            print("Frame recording error!") # Виведення повідомлення про помилку запису
            break
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL) # Створення та налаштування вікна відображення
        cv2.resizeWindow('frame', 800, 700)
        # Відображення результату
        cv2.imshow('frame', frame) # Відображення кадру
        if cv2.waitKey(25) == ord('q'): # Очікування натискання клавіші 'q' для виходу
            break
    # Завершуємо запис у кінці роботи
    cap.release() # Закриття відеопотоку
    cv2.destroyAllWindows() # Закриття всіх вікон OpenCV


# при запуску як головного файлу
if __name__ == '__main__':
    main()
