# https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_iris.html
import pandas as pd
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import logging
import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from time import time

logging.basicConfig(level=logging.DEBUG)

class ImageObject:
    def __init__(self, cv_img) -> None:
        '''Create an instance that store all required image data'''
        self.cv_img = cv_img
        self.tk_img = ImageMatching.cv2tkimg(cv_img)
        self.tk_img_id = None
        self.rank = 0

    def get_resized_tk_img(h:int, w:int):
        pass

    def __del__(self):
        self.cv_img = None
        self.tk_img = None
        self.tk_img_id = None


class ImageMatching:
    COLORS_CSV_FILE = r'src/colors.csv'
    COLOR_2_RGB_DICT = {}
    RGB_2_COLOR_DICT = {}

    def __init__(self) -> None:
        '''Initialize instance with empty variables'''
        if len(self.__class__.COLOR_2_RGB_DICT) == 0 or len(self.__class__.RGB_2_COLOR_DICT) == 0:
            self.__class__.read_colors_csv()

        self._source_image = None
        self._target_images = []
        self._n_highlight_color = 3

    def set_source_image(self, filename: str, can_image: tk.Canvas):
        '''Set source matching image'''
        # Remove the image from canvas and memory
        if can_image:
            if self._source_image is not None:
                can_image.delete(self._source_image.tk_img_id)
                del self._source_image
                logging.info('Removed image from canvas')

        self._source_image = ImageObject(cv2.imread(filename))

        if can_image:
            self._source_image.tk_img_id = can_image.create_image(0, 0, image=self._source_image.tk_img, anchor=tk.NW)
            logging.info('Added new image to canvas')

    def set_target_images(self, filenames: list, can_image: tk.Canvas, scroll_frame: tk.Frame):
        '''Set target matching images'''

        if can_image:
            can_image.delete("all")
            logging.info('Removed images from canvas')

        if scroll_frame:
            
            for i, widget in enumerate(scroll_frame.winfo_children()):
                scroll_frame.grid_rowconfigure(i, weight=0, minsize=0)
                widget.destroy()
            self._target_images.clear()
            self._target_images = []
            logging.info('Removed images from scroll frame')

        for file in filenames:
            self._target_images.append(ImageObject(cv2.imread(file)))

        scroll_frame.grid_columnconfigure(0, weight=0, minsize=100)
        for i in range(len(filenames)):
            scroll_frame.grid_rowconfigure(i, weight=0, minsize=100)
            tk.Label(master=scroll_frame, image=self._target_images[i].tk_img).grid(column=0, row=i, padx=2, pady=2, sticky="nsew")

        logging.info('Added new images to scroll frame')


    @classmethod
    def cv2tkimg(cls, cvImage):
        _image = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        _image = Image.fromarray(_image)
        return ImageTk.PhotoImage(_image)

    @classmethod
    def rgb2hex(cls, r: int, g: int, b: int) -> str:
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    @classmethod
    def hex2rgb(cls, hexcode: str) -> tuple:
        return tuple(map(ord, hexcode[1:].decode('hex')))

    @classmethod
    def read_colors_csv(cls):
        '''Read predefined colors data into dictionaries'''
        index = ["color", "color_name", "hex", "R", "G", "B"]
        colors_pd = pd.read_csv(cls.COLORS_CSV_FILE, names=index, header=None)
        colors = colors_pd[index[1]].to_list()
        rgbs = zip(colors_pd[index[3]].to_list(), colors_pd[index[4]].to_list(), colors_pd[index[5]].to_list())
        cls.COLOR_2_RGB_DICT = dict(zip(colors, rgbs))
        cls.RGB_2_COLOR_DICT = dict(zip(rgbs, colors))
