# підключення необхідних бібліотек
import cv2
import numpy as np

sources = {'video1': "video1.mp4", 'video2': "video2.mp4", "web": 0} # Словник із джерелами відео

# функція повороту зображення
def rotate_image(image, angle=0):
    num_rows, num_cols = image.shape[:2] # Отримуємо розміри зображення
    rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), angle, 1) # Генеруємо матрицю повороту
    img_rotation = cv2.warpAffine(image, rotation_matrix, (num_cols, num_rows)) # Застосовуємо поворот до зображення
    return img_rotation


# функція переносу зображення
def parallel_transfer(image, left=0, top=0):
    num_rows, num_cols = image.shape[:2] # Отримуємо розміри зображення
    translation_matrix = np.float32([[1, 0, left], [0, 1, top]]) # Генеруємо матрицю переносу
    img_translation = cv2.warpAffine(image, translation_matrix, (num_cols, num_rows)) # Застосовуємо перенос до зображення
    return img_translation


# функція скісу зображення
def bevel(image, coef_1=1.0, coef_2=0.0):
    rows, cols = image.shape[:2]
    # Визначаємо початкові і кінцеві точки для створення скосу
    src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
    dst_points = np.float32([[0, 0], [int(coef_1 * (cols - 1)), 0],
                             [int(coef_2 * (cols - 1)), rows - 1]])
    affine_matrix = cv2.getAffineTransform(src_points, dst_points) # Отримуємо матрицю перетворення
    img_output = cv2.warpAffine(image, affine_matrix, (cols, rows)) # Застосовуємо скіс до зображення
    return img_output


# функція дзеркального відображення зображення
def mirror(image):
    rows, cols = image.shape[:2]
    # Визначаємо початкові і кінцеві точки для дзеркального відображення
    src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
    dst_points = np.float32([[cols - 1, 0], [0, 0], [cols - 1, rows - 1]])
    affine_matrix = cv2.getAffineTransform(src_points, dst_points) # Отримуємо матрицю перетворення
    img_output = cv2.warpAffine(image, affine_matrix, (cols, rows)) # Застосовуємо дзеркальне відображення до зображення
    return img_output

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

        # Геометричні перетворення зображення (фрейму)
        frame_rotate = rotate_image(frame, 30)
        frame_transfer = parallel_transfer(frame, 100)
        frame_bevel = bevel(frame, 0.6, 0.4)
        frame_mirror = mirror(frame)
        # Створення та налаштування вікон відображення
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 400, 350)
        cv2.namedWindow('frame_rotated', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_rotated', 400, 350)
        cv2.namedWindow('frame_transfered', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_transfered', 400, 350)
        cv2.namedWindow('frame_bevel', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_bevel', 400, 350)
        cv2.namedWindow('frame_mirrored', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_mirrored', 400, 350)
        # Відображення результату
        cv2.imshow('frame', frame)
        cv2.imshow('frame_rotated', frame_rotate)
        cv2.imshow('frame_transfered', frame_transfer)
        cv2.imshow('frame_bevel', frame_bevel)
        cv2.imshow('frame_mirrored', frame_mirror)
        if cv2.waitKey(25) == ord('q'):
            break
    # Завершуємо запис у кінці роботи
    cap.release() # Закриття відеопотоку
    cv2.destroyAllWindows() # Закриття всіх вікон OpenCV


# при запуску як головного файлу
if __name__ == '__main__':
    main()
