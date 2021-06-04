# https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_iris.html
from functools import partial
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
        self.rank = 0
        self.highlight_colors = []
        self.main_color_var = None
        self.color_palettes = []

    def get_resize_cv_img(self, h: int, w: int):
        resize_cv_img = self.__class__.resize(self.cv_img, h, w)
        return resize_cv_img

    def get_resize_tk_img(self, h: int, w: int):
        resize_tk_img = ImageMatching.cv2tkimg(self.__class__.resize(self.cv_img, h, w))
        return resize_tk_img

    def get_tk_thumbnail(self):
        resize_tk_img = ImageMatching.cv2tkimg(self.__class__.resize(self.cv_img))
        return resize_tk_img

    def get_main_rgb(self) -> tuple:
        main_rgb = self.highlight_colors[self.main_color_var.get()]
        return main_rgb

    def __del__(self):
        self.cv_img = None
        self.tk_img = None
        self.highlight_colors = None
        self.main_color_var = None
        self.color_palettes = None

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

        src_H, src_W, _ = cv_img.shape
        ratio = 0
        if(src_H > src_W):
            ratio = src_H/dst_h
            dst_w = int(src_W / ratio)
        else:
            ratio = src_W/dst_w
            dst_h = int(src_H / ratio)
        
        row_ratio, col_ratio= np.array([dst_h, dst_w])/np.array([src_H, src_W])
        
        # row wise interpolation 
        row_idx = (np.ceil(range(1, 1 + int(src_H*row_ratio))/row_ratio) - 1).astype(int)
        # column wise interpolation
        col_idx = (np.ceil(range(1, 1 + int(src_W*col_ratio))/col_ratio) - 1).astype(int)

        final_matrix = cv_img[:, col_idx][row_idx, :]
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
        self._n_highlight_color = 3

    def set_source_image(self, filename: str, can_image: tk.Canvas, scroll_frame: tk.Frame):
        '''Set source matching image'''
        # Remove the image from canvas and memory
        if can_image:
            if self._source_image is not None:
                can_image.delete("all")
                del self._source_image
                self._source_image = None
                logging.info('Removed image from canvas')

        # Remove color palettes from scroll frame
        if scroll_frame:
            for i, widget in enumerate(scroll_frame.winfo_children()):
                scroll_frame.grid_columnconfigure(i, weight=0, minsize=0)
                widget.destroy()
            if self._source_image:
                self._source_image.color_palettes.clear()
                self._source_image.color_palettes = []
            logging.info('Removed color pallets from scroll frame')

        self._source_image = ImageObject(cv2.imread(filename))

        if can_image:
            can_image.create_image(0, 0, image=self._source_image.tk_img, anchor=tk.NW)
            logging.info('Added new image to canvas')

    def set_target_images(self, filenames: list, can_image: tk.Canvas, scroll_frame: tk.Frame, palette_frame: tk.Frame):
        '''Set target matching images'''

        def display_tk_image_n_palettes(img_obj: 'ImageObject'):
            '''Button command for image list'''
            # delete widgets
            can_image.delete("all")
            for i, widget in enumerate(palette_frame.winfo_children()):
                palette_frame.grid_columnconfigure(i, weight=0, minsize=0)
                widget.destroy()
            # change image in canvas
            can_image.create_image(0, 0, image=img_obj.tk_img, anchor=tk.NW)
            # display palettes
            for i in range(len(img_obj.color_palettes)):
                palette_frame.grid_columnconfigure(i, weight=0, minsize=80)
                new_radio_bt = tk.Radiobutton(master=palette_frame,
                                              image=img_obj.color_palettes[i],
                                              compound='right',
                                              variable=img_obj.main_color_var,
                                              value=i,
                                              background='black')
                new_radio_bt.grid(column=i, row=0, padx=2, pady=2, sticky="nsew")
                if i == img_obj.main_color_var.get():
                    new_radio_bt.select()

            logging.info('Changed image in canvas')

        # remove image from canvas
        if can_image:
            can_image.delete("all")
            logging.info('Removed images from canvas')

        # remove thumbnail from scroll frame
        if scroll_frame:
            for i, widget in enumerate(scroll_frame.winfo_children()):
                scroll_frame.grid_rowconfigure(i, weight=0, minsize=0)
                widget.destroy()
            self._target_thumbnails.clear()
            self._target_thumbnails = []
            self._target_images.clear()
            self._target_images = []
            logging.info('Removed images from scroll frame')

        # remove color palettes from palettes frame
        if palette_frame:
            for i, widget in enumerate(palette_frame.winfo_children()):
                palette_frame.grid_columnconfigure(i, weight=0, minsize=0)
                widget.destroy()
            logging.info('Removed color pallets from scroll frame')

        # read list of images
        for file in filenames:
            self._target_images.append(ImageObject(cv2.imread(file)))

        # generating highlight color for each image
        for i in range(len(self._target_images)):
            # get highlight color
            highlight_colors, _ = kmeans.perform(self._target_images[i].get_resize_cv_img(200, 200))
            # TODO: get close color and remove duplicate color
            highlight_colors = list(set([tuple(x) for x in highlight_colors]))

            for x in highlight_colors:
                b, g, r = x
                new_tk_img = self.generate_color_tk_img(r, g, b)
                self._target_images[i].color_palettes.append(new_tk_img)
                self._target_images[i].highlight_colors.append((r, g, b))
                logging.info(f'{i} Detected color: {(r,g,b)}')

            # create new int var
            self._target_images[i].main_color_var = tk.IntVar()
            self._target_images[i].main_color_var.set(0)

        # setting up thumbnail in scroll frame
        scroll_frame.grid_columnconfigure(0, weight=0, minsize=100)
        for i in range(len(filenames)):
            scroll_frame.grid_rowconfigure(i, weight=0, minsize=100)
            new_thumbnail = self._target_images[i].get_tk_thumbnail()
            new_button = tk.Button(master=scroll_frame, image=new_thumbnail, command=partial(display_tk_image_n_palettes, self._target_images[i]))
            new_button.grid(column=0, row=i, padx=0, pady=0, sticky="nsew")
            self._target_thumbnails.append(new_thumbnail)

        # setting up color palettes in scroll frame

        logging.info('Added new images to scroll frame')

    def generate_source_color_pallets(self, scroll_frame: tk.Frame):
        '''Generate color pallets by highlight colors'''
        if self._source_image is None:
            return

        # remove existing color pallets
        if scroll_frame:
            for i, widget in enumerate(scroll_frame.winfo_children()):
                scroll_frame.grid_columnconfigure(i, weight=0, minsize=0)
                widget.destroy()
            self._source_image.color_palettes.clear()
            self._source_image.color_palettes = []
            self._source_image.highlight_colors.clear()
            self._source_image.highlight_colors = []
            logging.info('Removed color pallets from scroll frame')

        # get highlight color
        highlight_colors, _ = kmeans.perform(self._source_image.get_resize_cv_img(200, 200))
        # TODO: get close color and remove duplicate color
        highlight_colors = list(set([tuple(x) for x in highlight_colors]))

        for x in highlight_colors:
            b, g, r = x
            new_tk_img = self.generate_color_tk_img(r, g, b)
            self._source_image.color_palettes.append(new_tk_img)
            self._source_image.highlight_colors.append((r, g, b))
            logging.info('Detected color: ' + str((r, g, b)))

        # create new int var
        self._source_image.main_color_var = tk.IntVar()

        scroll_frame.grid_rowconfigure(0, weight=0, minsize=50)
        for i in range(len(self._source_image.color_palettes)):
            scroll_frame.grid_columnconfigure(i, weight=0, minsize=80)
            new_radio_bt = tk.Radiobutton(master=scroll_frame,
                                          image=self._source_image.color_palettes[i],
                                          compound='right',
                                          variable=self._source_image.main_color_var,
                                          value=i,
                                          background='black')
            new_radio_bt.grid(column=i, row=0, padx=2, pady=2, sticky="nsew")

        if len(self._source_image.color_palettes) > 0:
            new_radio_bt.select()
            self._source_image.main_color_var.set(len(self._source_image.color_palettes) - 1)

        logging.info('Generated color pallets to scroll frame')

    def generate_matching_results(self, can_image: tk.Canvas, scroll_frame: tk.Frame, palette_frame: tk.Frame):
        '''
        1. kmeans for each image list
        2. check selected color
        3. compute matching rate
        4. sort the each image list
        5. update image list frame
        6. update display frame
        '''
        def display_tk_image_n_palettes(img_obj: 'ImageObject'):
            '''Button command for image list'''
            # delete widgets
            can_image.delete("all")
            for i, widget in enumerate(palette_frame.winfo_children()):
                palette_frame.grid_columnconfigure(i, weight=0, minsize=0)
                widget.destroy()
            # change image in canvas
            can_image.create_image(0, 0, image=img_obj.tk_img, anchor=tk.NW)
            # display palettes
            for i in range(len(img_obj.color_palettes)):
                palette_frame.grid_columnconfigure(i, weight=0, minsize=80)
                new_radio_bt = tk.Radiobutton(master=palette_frame,
                                              image=img_obj.color_palettes[i],
                                              compound='right',
                                              variable=img_obj.main_color_var,
                                              value=i,
                                              background='black')
                new_radio_bt.grid(column=i, row=0, padx=2, pady=2, sticky="nsew")
                if i == img_obj.main_color_var.get():
                    new_radio_bt.select()

        # check can perform match
        if self._source_image is None or self._source_image.main_color_var is None or len(self._target_images) < 1:
            logging.info('Images not imported')
            return

        # 2
        source_rgb = self._source_image.get_main_rgb()

        target_rgbs = []
        for i in range(len(self._target_images)):
            r, g, b = self._target_images[i].get_main_rgb()
            target_rgbs.append([r, g, b])

        # 3
        ranks = self.__class__.getClosestMatch(source_rgb, target_rgbs)
        for i, rank in enumerate(ranks):
            self._target_images[i].rank = rank

        # 4
        sorted_idx = [i[0] for i in sorted(enumerate(self._target_images), key=lambda x:x[1])]

        # 5
        new_target_images = []
        new_target_thumbnails = []
        for i, widget in enumerate(scroll_frame.winfo_children()):
            widget.destroy()
            new_target_images.append(self._target_images[sorted_idx[i]])
            new_target_thumbnails.append(self._target_thumbnails[sorted_idx[i]])

        self._target_images = new_target_images
        self._target_thumbnails = new_target_thumbnails 

        for i in range(len(self._target_images)):
            new_button = tk.Button(master=scroll_frame, image=self._target_thumbnails[i], command=partial(display_tk_image_n_palettes, self._target_images[i]))
            new_button.grid(column=0, row=i, padx=0, pady=0, sticky="nsew")


        # check
        logging.info('Source main color: ' + str(source_rgb))
        logging.info('Source main color var: ' + str(self._source_image.main_color_var.get()))
        for i in range(len(self._target_images)):
            r, g, b = self._target_images[i].get_main_rgb()
            logging.info(f'Target {i} main color: {(r,g,b)}')
            logging.info(f'Target {i} main color var: {self._target_images[i].main_color_var.get()}')
            logging.info(f'Target {i} rank: {self._target_images[i].rank}')

        # 6

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

    @classmethod
    def getComplementaryColour(cls, r: int, g: int, b: int):
        '''To calculate the complementary colour for a given colour'''
        return [255-r, 255-g, 255-b]

    @classmethod
    def getClosestMatch(cls, source_colour: tuple, colour_codes: list) -> list:
        '''Get and return the index for the closest match Shirt for our pants'''
        r, g, b = source_colour
        comp_colour = cls.getComplementaryColour(r, g, b)
        minimum = 1e9
        best = -1

        ranks = []
        # Find the closest match with the minumum absolute difference
        for i in range(len(colour_codes)):
            d = np.sum(np.abs(np.subtract(comp_colour, colour_codes[i])))
            ranks.append(d)
        return ranks
