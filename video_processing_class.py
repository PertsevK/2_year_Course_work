import cv2
import numpy as np

sources = {'video1': "video1.mp4", 'video2': "video2.mp4", "web": 0}
colorspaces = {'Gray': cv2.COLOR_BGR2GRAY, 'XYZ': cv2.COLOR_BGR2XYZ, 'LAB': cv2.COLOR_BGR2LAB,
               'YUV': cv2.COLOR_BGR2YUV, 'HSV': cv2.COLOR_BGR2HSV, 'RGB': cv2.COLOR_BGR2RGB} # Визначення колірних просторів для зміни

class VideoProcessing:
    """Video processing class"""

    # конструктор
    def __init__(self, filename):
        self.__filename = filename
        self.__mode = 0
        # Словник, що містить методи обробки відео для кожного режиму
        self.__mode_to_func = {1: VideoProcessing.colorspace_change, 2: VideoProcessing.bevel,
                               3: VideoProcessing.canny_edge_detection, 4: VideoProcessing.bilateral_filtration}
        # Словник, що відображає режими на їх назви
        self.__mode_to_step = {0: "Basic", 1: "Colorspace", 2: "Geometric", 3: "Operation", 4: "Filtration"}
        self.__stop_flag = False

    # Зміна джерела відео
    def change_input(self, new_filename):
        self.__filename = new_filename

    # Встановлення поточного режиму обробки відео
    def set_mode(self, mode_key):
        self.__mode = mode_key

    # Отримання назви поточного режиму
    def get_current_mode_name(self):
        return self.__mode_to_step.get(self.__mode)

    # Метод для зміни колірного простору
    @staticmethod
    def colorspace_change(image, colorspace_index='RGB'):
        return cv2.cvtColor(image, colorspaces.get(colorspace_index))

    # Метод для створення нахилу на зображенні
    @staticmethod
    def bevel(image, coef_1=1.5, coef_2=0.3):
        rows, cols = image.shape[:2]
        # Визначаємо початкові і кінцеві точки для створення скосу
        src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
        dst_points = np.float32([[0, 0], [int(coef_1 * (cols - 1)), 0],
                                [int(coef_2 * (cols - 1)), rows - 1]])
        affine_matrix = cv2.getAffineTransform(src_points, dst_points) # Отримуємо матрицю перетворення
        img_output = cv2.warpAffine(image, affine_matrix, (cols, rows)) # Застосовуємо скіс до зображення
        return img_output

    # Метод для виявлення граней за допомогою алгоритму Canny
    @staticmethod
    def canny_edge_detection(image, t_lower=100, t_upper=200): 
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Перетворення зображення в відтінки сірого
        edge = cv2.Canny(gray_image, t_lower, t_upper) # Використання алгоритму Canny для виявлення граней
        return edge

    # Метод для білатерального фільтрування зображення
    @staticmethod
    def bilateral_filtration(image, filter_size=9, sigmaValues=75):
        return cv2.bilateralFilter(image, filter_size, sigmaValues, sigmaValues)

    # методи класу
    def start_processing(self):
        cap = cv2.VideoCapture(self.__filename)
        self.__stop_flag = False
        # Перевірка готовності веб-камери
        while cap.isOpened() and not self.__stop_flag:
            # Запис фреймів
            ret, frame = cap.read()
            # При виникненні помилці запису
            if not ret:
                print("Frame recording error!")
                break

            frame_changed = self.__modify_frame(frame)

            # Відображення результату
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame', 400, 350)
            cv2.namedWindow('frame_changed', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame_changed', 400, 350)
            cv2.imshow('frame', frame)
            cv2.imshow('frame_changed', frame_changed)
            self.__state_check()
        # Завершуємо запис у кінці роботи
        cap.release()
        cv2.destroyAllWindows()

    # Перевірка стану клавіатури
    def __state_check(self):
        key_code = cv2.waitKey(25)
        if key_code == ord('0'):
            self.set_mode(0)
        elif key_code == ord('1'):
            self.set_mode(1)
        elif key_code == ord('2'):
            self.set_mode(2)
        elif key_code == ord('3'):
            self.set_mode(3)
        elif key_code == ord('4'):
            self.set_mode(4)
        elif key_code == ord('q'):
            self.__stop_flag = True
        print(self.get_current_mode_name())
    
    # Модифікація кадру відео залежно від поточного режиму
    def __modify_frame(self, input_frame):
        if self.__mode == 0:
            return input_frame
        elif self.__mode in self.__mode_to_func.keys():
            return self.__mode_to_func.get(self.__mode)(input_frame)


def main():
    # Створення екземпляру класу та обробка відео
    video_processing = VideoProcessing(sources.get('video1'))
    video_processing.start_processing()
    # Зміна режиму та джерела відео
    video_processing.set_mode(3)
    video_processing.change_input(sources.get('video2'))
    video_processing.start_processing()


if __name__ == '__main__':
    main()
