# -*- coding: utf-8 -*-
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

sources = {'video1': "video1.mp4", 'video2': "video2.mp4", "web": 0}
colorspaces = {'Gray': cv2.COLOR_BGR2GRAY, 'XYZ': cv2.COLOR_BGR2XYZ, 'LAB': cv2.COLOR_BGR2LAB,
               'YUV': cv2.COLOR_BGR2YUV, 'HSV': cv2.COLOR_BGR2HSV, 'RGB': cv2.COLOR_BGR2RGB}

class VideoProcessing:
    """Video processing class"""

    def __init__(self, filename):
        self.__filename = filename
        self.__mode = 0
        self.__mode_to_func = {1: VideoProcessing.colorspace_change, 2: VideoProcessing.bevel,
                               3: VideoProcessing.canny_edge_detection, 4: VideoProcessing.bilateral_filtration}
        self.__mode_to_step = {0: "Basic", 1: "Colorspace", 2: "Geometric", 3: "Operation", 4: "Filtration"}
        self.__stop_flag = False
        self.colorspace_index = 'RGB'
        self.coef_1 = 1.5
        self.coef_2 = 0.3
        self.t_lower = 100
        self.t_upper = 200
        self.filter_size = 9
        self.sigmaValues = 75
        

    def change_input(self, new_filename):
        self.__filename = new_filename

    def set_mode(self, mode_key):
        self.__mode = mode_key

    def get_current_mode_name(self):
        return self.__mode_to_step.get(self.__mode)

    @staticmethod
    def colorspace_change(self, image):
        return cv2.cvtColor(image, colorspaces.get(self.colorspace_index))

    @staticmethod
    def bevel(self, image):
        rows, cols = image.shape[:2]
        src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
        dst_points = np.float32([[0, 0], [int(self.coef_1 * (cols - 1)), 0],
                                [int(self.coef_2 * (cols - 1)), rows - 1]])
        affine_matrix = cv2.getAffineTransform(src_points, dst_points)
        img_output = cv2.warpAffine(image, affine_matrix, (cols, rows))
        return img_output

    @staticmethod
    def canny_edge_detection(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray_image, self.t_lower, self.t_upper)
        return edge

    @staticmethod
    def bilateral_filtration(self, image):
        return cv2.bilateralFilter(image, self.filter_size, self.sigmaValues, self.sigmaValues)

    def start_processing(self):
        cap = cv2.VideoCapture(self.__filename)
        self.__stop_flag = False
        while cap.isOpened() and not self.__stop_flag:
            ret, frame = cap.read()
            if not ret:
                print("Frame recording error!")
                break

            frame_changed = self.__modify_frame(frame)

            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame', 400, 350)
            cv2.namedWindow('frame_changed', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame_changed', 400, 350)
            cv2.imshow('frame', frame)
            cv2.imshow('frame_changed', frame_changed)
            self.__state_check()
        cap.release()
        cv2.destroyAllWindows()

    def __state_check(self):
        key_code = cv2.waitKey(25)
        if key_code == ord('q'):
            self.__stop_flag = True
        print(self.get_current_mode_name())
    
    def __modify_frame(self, input_frame):
        if self.__mode == 0:
            return input_frame
        elif self.__mode in self.__mode_to_func.keys():
            return self.__mode_to_func.get(self.__mode)(self, input_frame)

class VideoProcessingGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Processing")
        self.geometry("500x300")
        
        self.video_processing = VideoProcessing(sources['video1'])
        
        self.create_widgets()

    def create_widgets(self):
        self.source_frame = tk.Frame(self)
        self.source_frame.pack(pady=5)

        self.source_label = tk.Label(self.source_frame, text="Select Video Source:")
        self.source_label.pack(side="left")

        self.source_combo = ttk.Combobox(self.source_frame, values=list(sources.keys()))
        self.source_combo.current(0)
        self.source_combo.pack(side="left")

        self.mode_frame = tk.Frame(self)
        self.mode_frame.pack(pady=5)

        self.mode_label = tk.Label(self.mode_frame, text="Select Processing Mode:")
        self.mode_label.pack(side="left")

        self.mode_combo = ttk.Combobox(self.mode_frame, values=list(self.video_processing._VideoProcessing__mode_to_step.values()))
        self.mode_combo.current(0)
        self.mode_combo.pack(side="left")

        self.color_change_frame = tk.Frame(self)
        self.color_change_frame.pack(pady=5)

        self.color_change_label = tk.Label(self.color_change_frame, text="Select Color Change Mode:")
        self.color_change_label.pack(side="left")

        self.color_change = ttk.Entry(self.color_change_frame)
        self.color_change.insert(0, "RGB")
        self.color_change.pack(side="left")

        self.geometric_change_frame = tk.Frame(self)
        self.geometric_change_frame.pack(pady=5)

        self.geometric_change_label1 = tk.Label(self.geometric_change_frame, text="Enter coef_1:")
        self.geometric_change_label1.pack(side="left")

        self.geometric_change1 = ttk.Entry(self.geometric_change_frame)
        self.geometric_change1.insert(0, "1.5")
        self.geometric_change1.pack(side="left")

        self.geometric_change_label2 = tk.Label(self.geometric_change_frame, text="Enter coef_2:")
        self.geometric_change_label2.pack(side="left")

        self.geometric_change2 = ttk.Entry(self.geometric_change_frame)
        self.geometric_change2.insert(0, "0.3")
        self.geometric_change2.pack(side="left")

        self.canny_change_frame = tk.Frame(self)
        self.canny_change_frame.pack(pady=5)

        self.canny_change_label1 = tk.Label(self.canny_change_frame, text="Enter t_lower:")
        self.canny_change_label1.pack(side="left")

        self.canny_change1 = ttk.Entry(self.canny_change_frame)
        self.canny_change1.insert(0, "100")
        self.canny_change1.pack(side="left")

        self.canny_change_label2 = tk.Label(self.canny_change_frame, text="Enter t_upper:")
        self.canny_change_label2.pack(side="left")

        self.canny_change2 = ttk.Entry(self.canny_change_frame)
        self.canny_change2.insert(0, "200")
        self.canny_change2.pack(side="left")

        self.bilatheral_change_frame = tk.Frame(self)
        self.bilatheral_change_frame.pack(pady=5)

        self.bilatheral_change_label1 = tk.Label(self.bilatheral_change_frame, text="Enter filter_size:")
        self.bilatheral_change_label1.pack(side="left")

        self.bilatheral_change1 = ttk.Entry(self.bilatheral_change_frame)
        self.bilatheral_change1.insert(0, "9")
        self.bilatheral_change1.pack(side="left")

        self.bilatheral_change_label2 = tk.Label(self.bilatheral_change_frame, text="Enter sigmaValues:")
        self.bilatheral_change_label2.pack(side="left")

        self.bilatheral_change2 = ttk.Entry(self.bilatheral_change_frame)
        self.bilatheral_change2.insert(0, "75")
        self.bilatheral_change2.pack(side="left")

        self.start_button = tk.Button(self, text="Start Processing", command=self.start_processing)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self, text="Stop Processing", command=self.stop_processing)
        self.stop_button.pack(pady=5)

    def start_processing(self):
        source = self.source_combo.get()
        mode_name = self.mode_combo.get()
        mode = list(self.video_processing._VideoProcessing__mode_to_step.values()).index(mode_name)
        
        self.video_processing.change_input(sources[source])
        self.video_processing.set_mode(mode)
        
        self.video_processing.colorspace_index = str(self.color_change.get())
        self.video_processing.coef_1 = float(self.geometric_change1.get())
        self.video_processing.coef_2 = float(self.geometric_change2.get())
        self.video_processing.t_lower = float(self.canny_change1.get())
        self.video_processing.t_upper = float(self.canny_change2.get())
        self.video_processing.filter_size = int(self.bilatheral_change1.get())
        self.video_processing.sigmaValues = int(self.bilatheral_change2.get())

        self.video_processing.start_processing()

    def stop_processing(self):
        self.video_processing._VideoProcessing__stop_flag = True

def main():
    app = VideoProcessingGUI()
    app.mainloop()

if __name__ == '__main__':
    main()
