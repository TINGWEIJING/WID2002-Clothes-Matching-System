# https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_iris.html
from functools import partial
from numpy.core.fromnumeric import resize
import pandas as pd
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import logging
import cv2
import numpy as np
import kmeans

logging.basicConfig(level=logging.DEBUG)


class ImageObject:
    def __init__(self, cv_img) -> None:
        '''Create an instance that store all required image data'''
        self.cv_img = cv_img
        self.tk_img = self.get_resize_tk_img(400, 400)
        self.tk_img_id = None
        self.rank = 0

    def get_resize_cv_img(self, h: int, w: int):
        resize_cv_img = self.__class__.resize(self.cv_img, h, w)
        return resize_cv_img

    def get_resize_tk_img(self, h: int, w: int):
        resize_tk_img = ImageMatching.cv2tkimg(self.__class__.resize(self.cv_img, h, w))
        return resize_tk_img

    def get_tk_thumbnail(self):
        resize_tk_img = ImageMatching.cv2tkimg(self.__class__.resize(self.cv_img))
        return resize_tk_img

    def __del__(self):
        self.cv_img = None
        self.tk_img = None
        self.tk_img_id = None

    def __eq__(self, other: 'ImageObject'):
        return self.rank == other.rank

    def __lt__(self, other: 'ImageObject'):
        return self.rank < other.rank

    def __le__(self, other: 'ImageObject'):
        return self.rank <= other.rank

    def __gt__(self, other: 'ImageObject'):
        return self.rank > other.rank

    def __ge__(self, other: 'ImageObject'):
        return self.rank >= other.rank

    @classmethod
    def resize(cls, cv_img, dst_h: int = 100, dst_w: int = 100):
        '''Using NN interpolation to resize'''

        src_H, src_W, channels = cv_img.shape
        old_size =  cv_img.shape
        row_ratio, col_ratio, _ = np.array([dst_h, dst_w,3])/np.array(old_size)
        
        print(row_ratio, col_ratio)
        # row wise interpolation 
        row_idx = (np.ceil(range(1, 1 + int(src_H*row_ratio))/row_ratio) - 1).astype(int)
        # column wise interpolation
        col_idx = (np.ceil(range(1, 1 + int(src_W*col_ratio))/col_ratio) - 1).astype(int)

        final_matrix = cv_img[:, col_idx][row_idx, :]
        print(final_matrix.shape)
        return final_matrix


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
        self._target_thumbnails = []
        self._color_checkbox_vars = {}
        self._color_pallets = []
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

        def display_tk_image(img):
            can_image.delete("all")
            can_image.create_image(0, 0, image=img, anchor=tk.NW)
            logging.info('Changed image in canvas')

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
            new_thumbnail = self._target_images[i].get_tk_thumbnail()
            new_button = tk.Button(master=scroll_frame, image=new_thumbnail, command=partial(display_tk_image, self._target_images[i].tk_img))
            new_button.grid(column=0, row=i, padx=0, pady=0, sticky="nsew")
            self._target_thumbnails.append(new_thumbnail)

        logging.info('Added new images to scroll frame')

    def generate_color_pallets(self, scroll_frame: tk.Frame):
        if self._source_image is None:
            return

        if scroll_frame:
            for i, widget in enumerate(scroll_frame.winfo_children()):
                scroll_frame.grid_columnconfigure(i, weight=0, minsize=0)
                widget.destroy()
            self._color_checkbox_vars.clear()
            self._color_checkbox_vars = {}
            self._color_pallets.clear()
            self._color_pallets = []
            logging.info('Removed color pallets from scroll frame')

        highlight_color, _ = kmeans.perform(self._source_image.get_resize_cv_img(200, 200))

        # TODO: get close color and remove duplicate color
        highlight_color = list(set([tuple(x) for x in highlight_color]))

        for x in highlight_color:
            b, g, r = x
            new_tk_img = self.generate_color_tk_img(r, g, b)
            self._color_pallets.append(new_tk_img)
            logging.info('Detected color: ' + str(x))

        scroll_frame.grid_rowconfigure(0, weight=0, minsize=50)
        for i in range(len(self._color_pallets)):
            scroll_frame.grid_columnconfigure(i, weight=0, minsize=80)
            new_var = tk.IntVar()
            new_checkbox = tk.Checkbutton(master=scroll_frame, image=self._color_pallets[i], compound='right', variable=new_var, background='black')
            new_checkbox.select()
            new_checkbox.grid(column=i, row=0, padx=2, pady=2, sticky="nsew")
            self._color_checkbox_vars[highlight_color[i]] = new_var

        logging.info('Generated color pallets to scroll frame')

    def generate_matching_results(self, can_image: tk.Canvas, scroll_frame: tk.Frame):
        '''
        1. kmeans for each image list
        2. check selected color
        3. compute matching rate
        4. sort the each image list
        5. update image list frame
        6. update display frame
        '''
        def display_tk_image(img):
            can_image.delete("all")
            can_image.create_image(0, 0, image=img, anchor=tk.NW)
            logging.info('Changed image in canvas')

        # 1

        # 2
        for rgb, var in self._color_checkbox_vars.items():
            if(var.get() == 1):
                print(rgb)

        # 3
        # 4
        for i in range(len(self._target_images)):
            self._target_images[i].rank = len(self._target_images) - i

        sorted_idx = [i[0] for i in sorted(enumerate(self._target_images), key=lambda x:x[1])]

        # 5 & 6
        for i, widget in enumerate(scroll_frame.winfo_children()):
            widget.destroy()

        for i, idx in enumerate(sorted_idx):
            new_button = tk.Button(master=scroll_frame, image=self._target_thumbnails[idx], command=partial(display_tk_image, self._target_images[idx].tk_img))
            new_button.grid(column=0, row=i, padx=0, pady=0, sticky="nsew")

        logging.info('Rearranged images in scroll frame')

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
    def generate_color_tk_img(cls, r: int, g: int, b: int):
        size = 50
        new_img = np.zeros((size, size, 3), dtype=np.uint8)
        new_img[:, :, 0].fill(b)
        new_img[:, :, 1].fill(g)
        new_img[:, :, 2].fill(r)
        tk_img = ImageMatching.cv2tkimg(new_img)
        return tk_img

    @classmethod
    def read_colors_csv(cls):
        '''Read predefined colors data into dictionaries'''
        index = ["color", "color_name", "hex", "R", "G", "B"]
        colors_pd = pd.read_csv(cls.COLORS_CSV_FILE, names=index, header=None)
        colors = colors_pd[index[1]].to_list()
        rgbs = zip(colors_pd[index[3]].to_list(), colors_pd[index[4]].to_list(), colors_pd[index[5]].to_list())
        cls.COLOR_2_RGB_DICT = dict(zip(colors, rgbs))
        cls.RGB_2_COLOR_DICT = dict(zip(rgbs, colors))
