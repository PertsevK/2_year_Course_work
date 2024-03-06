# підключення необхідних бібліотек
import cv2

sources = {'video1': "video1.mp4", 'video2': "video2.mp4", "web": 0} # Словник із джерелами
colorspaces = {'Gray': cv2.COLOR_BGR2GRAY, 'XYZ': cv2.COLOR_BGR2XYZ, 'LAB': cv2.COLOR_BGR2LAB,
               'YUV': cv2.COLOR_BGR2YUV, 'HSV': cv2.COLOR_BGR2HSV} # Визначення колірних просторів для зміни

# Функція для зміни колірного простору зображення
def colorspace_change(input_frame, colorspace_index):
    return cv2.cvtColor(input_frame, colorspaces.get(colorspace_index))

def main():
    cap = cv2.VideoCapture(sources.get('video2')) # Ініціалізація об'єкту для відеозахоплення з веб-камери
    # Перевірка готовності веб-камери
    while cap.isOpened():
        # Запис фреймів
        ret, frame = cap.read()
        # При виникненні помилці запису
        if not ret:
            print("Frame recording error!")
            break
        # Зміна колірного простору зображення (фрейму)
        frame_gray = colorspace_change(frame, 'Gray')
        frame_XYZ = colorspace_change(frame, 'XYZ')
        frame_LAB = colorspace_change(frame, 'LAB')
        frame_HSV = colorspace_change(frame, 'HSV')
        # Створення та налаштування вікон відображення
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 400, 350)
        cv2.namedWindow('frame Grayscale', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame Grayscale', 400, 350)
        cv2.namedWindow('frame XYZ', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame XYZ', 400, 350)
        cv2.namedWindow('frame LAB', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame LAB', 400, 350)
        cv2.namedWindow('frame HSV', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame HSV', 400, 350)
        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame Grayscale', frame_gray)
        cv2.imshow('frame XYZ', frame_XYZ)
        cv2.imshow('frame LAB', frame_LAB)
        cv2.imshow('frame HSV', frame_HSV)
        if cv2.waitKey(25) == ord('q'): # Очікування натискання клавіші 'q' для виходу
            break
    # Завершуємо запис у кінці роботи
    cap.release() # Закриття відеопотоку
    cv2.destroyAllWindows() # Закриття всіх вікон OpenCV


# при запуску як головного файлу
if __name__ == '__main__':
    main()
