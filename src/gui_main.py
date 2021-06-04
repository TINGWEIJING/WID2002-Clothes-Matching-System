import tkinter as tk
from tkinter import filedialog
from tkinter.constants import W
import os
from functools import partial
from utils import ImageMatching

# =================================================================
# Global variables
# -----------------------------------------------------------------
# Grid settings
GRID_COL_NUM = 5
GRID_ROW_NUM = 10
PADDING = 5
# Widgets settings
E_WIDTH = 140
E_HEIGHT = 40
# Main windows settings
ZOOM_FACTOR = 1.4
WIN_WIDTH = int((E_WIDTH + PADDING) * GRID_COL_NUM + PADDING)
WIN_HEIGHT = int((E_HEIGHT + PADDING) * GRID_ROW_NUM + PADDING)
WIN_TITLE = 'Cloths Matching'
COLORS_CSV_FILE = r'src/colors.csv'
COLOR_2_RGB_DICT = {}
RGB_2_COLOR_DICT = {}

# =================================================================
# Root initialization
# -----------------------------------------------------------------
CLOTH_MATCHING = ImageMatching()

root = tk.Tk()
root.geometry(f"{int(WIN_WIDTH*ZOOM_FACTOR)}x{int(WIN_HEIGHT*ZOOM_FACTOR)}")
root.title(WIN_TITLE)
root.minsize(WIN_WIDTH, WIN_HEIGHT)
for x in range(GRID_COL_NUM):
    if x != GRID_COL_NUM - 1:
        root.grid_columnconfigure(x, weight=1, minsize=E_WIDTH)
    else:
        root.grid_columnconfigure(x, weight=0, minsize=E_WIDTH)

for y in range(GRID_ROW_NUM):
    root.grid_rowconfigure(y, weight=1, minsize=E_HEIGHT)

color_chart_win = None

# =================================================================
# Event methods
# -----------------------------------------------------------------


def open_select_source_image(can_image: tk.Canvas, scroll_frame: tk.Frame):
    filetypes = (
        ('Image file', '*.jpg;*.jpeg;*.png'),
    )

    filename = filedialog.askopenfilename(
        title='Import source image',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    if len(filename) > 0 and can_image:
        CLOTH_MATCHING.set_source_image(filename=filename, can_image=can_image, scroll_frame=scroll_frame)


def analyse(scroll_frame: tk.Frame):
    CLOTH_MATCHING.generate_source_color_pallets(scroll_frame=scroll_frame)


def match(can_image: tk.Canvas, scroll_frame: tk.Frame, palette_frame: tk.Frame):
    CLOTH_MATCHING.generate_matching_results(can_image=can_image, scroll_frame=scroll_frame, palette_frame=palette_frame)

def open_select_matching_images(can_image: tk.Canvas, scroll_frame: tk.Frame, palette_frame: tk.Frame):
    filetypes = (
        ('Image file', '*.jpg;*.png'),
    )

    filenames = filedialog.askopenfilenames(
        title='Import matching images',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    if len(filenames) > 0 and scroll_frame and can_image:
        CLOTH_MATCHING.set_target_images(filenames=filenames, can_image=can_image, scroll_frame=scroll_frame, palette_frame=palette_frame)


def open_color_chart():
    '''
    Open new windom for color chart
    https://pythonprogramming.altervista.org/tkinter-open-a-new-window-and-just-one/
    '''
    global color_chart_win
    global COLOR_2_RGB_DICT
    global RGB_2_COLOR_DICT

    def on_closing():
        global color_chart_win
        color_chart_win.destroy()
        color_chart_win = None

    if color_chart_win:
        color_chart_win.focus()
    else:
        # create new window
        color_chart_win = tk.Toplevel()
        color_chart_win.geometry("400x400")
        color_chart_win["bg"] = "navy"
        color_chart_win.protocol("WM_DELETE_WINDOW", on_closing)
        color_chart_win.grid_columnconfigure(0, weight=1, minsize=E_WIDTH)
        color_chart_win.grid_rowconfigure(0, weight=1, minsize=E_HEIGHT)
        # create scrolledWindow
        sw = ScrolledWindow(parent=color_chart_win, canv_h=100)
        row = 0
        col = 0
        for color_name, rgb in ImageMatching.COLOR_2_RGB_DICT.items():
            r, g, b = rgb
            e = tk.Label(master=sw.scrollwindow, text=color_name, background=ImageMatching.rgb2hex(r, g, b))
            e.grid(row=row, column=col, sticky='EW')
            row += 1
            if (row > 20):
                row = 0
                col += 1
        sw.grid(row=0, column=0, sticky='EW')


# =================================================================
# Testing
# -----------------------------------------------------------------
# Layout
for x in range(GRID_COL_NUM):
    for y in range(GRID_ROW_NUM):
        tk.Label(master=root, bg='black').grid(column=x, row=y, padx=PADDING, pady=PADDING, sticky="nsew")

# Button
# tk.Button(master=root, text='Button').grid(column=0, row=0, padx=PADDING, pady=PADDING, sticky="nsew")
# tk.Button(master=root, text='Button').grid(column=1, row=0, padx=PADDING, pady=PADDING, sticky="nsew")
# tk.Button(master=root, text='Button').grid(column=2, row=0, padx=PADDING, pady=PADDING, sticky="nsew")
# tk.Button(master=root, text='Button').grid(column=3, row=0, padx=PADDING, pady=PADDING, sticky="nsew")
# tk.Button(master=root, text='Button').grid(column=4, row=0, padx=PADDING, pady=PADDING, sticky="nsew")

# Label
tk.Label(master=root, text='Image 1').grid(column=0, row=1, columnspan=2, rowspan=7, padx=PADDING, pady=PADDING, sticky="nsew")
tk.Label(master=root, text='Image 2').grid(column=2, row=1, columnspan=2, rowspan=7, padx=PADDING, pady=PADDING, sticky="nsew")
tk.Label(master=root, text='List').grid(column=4, row=1, columnspan=1, rowspan=7, padx=PADDING, pady=PADDING, sticky="nsew")
tk.Label(master=root, text='Pallet').grid(column=0, row=8, columnspan=GRID_COL_NUM, rowspan=2, padx=PADDING, pady=PADDING, sticky="nsew")

# =================================================================
# Special class
# -----------------------------------------------------------------


class ScrolledWindow(tk.Frame):
    """
    https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected 
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """

    def __init__(self, parent, canv_w=400, canv_h=400, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas
        """
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # creating a scrollbars
        self.xscrlbr = tk.Scrollbar(self.parent, orient='horizontal')
        self.xscrlbr.grid(column=0, row=1, sticky='ew', columnspan=2)
        self.yscrlbr = tk.Scrollbar(self.parent)
        self.yscrlbr.grid(column=1, row=0, sticky='ns')
        # creating a canvas
        self.canv = tk.Canvas(self.parent)
        self.canv.config(relief='flat',
                         width=10,
                         heigh=10, bd=0)
        # placing a canvas into frame
        self.canv.grid(column=0, row=0, sticky='nsew')
        # accociating scrollbar comands to canvas scroling
        self.xscrlbr.config(command=self.canv.xview)
        self.yscrlbr.config(command=self.canv.yview)

        # creating a frame to insert to canvas
        self.scrollwindow = tk.Frame(self.parent)

        self.canv.create_window(0, 0, window=self.scrollwindow, anchor='nw')

        self.canv.config(xscrollcommand=self.xscrlbr.set,
                         yscrollcommand=self.yscrlbr.set,
                         scrollregion=(0, 0, 100, 100))

        self.yscrlbr.lift(self.scrollwindow)
        self.xscrlbr.lift(self.scrollwindow)
        self.scrollwindow.bind('<Configure>', self._configure_window)
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

        return

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        self.canv.config(scrollregion='0 0 %s %s' % size)
        if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canv.config(width=self.scrollwindow.winfo_reqwidth())
        if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canv.config(height=self.scrollwindow.winfo_reqheight())
# =================================================================
# Widget
# -----------------------------------------------------------------


# 1
BT_OPEN_IMAGE_1 = tk.Button(master=root, text='Import Image 1')
BT_OPEN_IMAGE_1.grid(column=0, row=0, padx=PADDING, pady=PADDING, sticky="nsew")
# 2
BT_ANALYSE = tk.Button(master=root, text='Analyze')
BT_ANALYSE.grid(column=1, row=0, padx=PADDING, pady=PADDING, sticky="nsew")
# 3
BT_COLOR_CHART = tk.Button(master=root, text='Color Chart', command=open_color_chart)
BT_COLOR_CHART.grid(column=2, row=0, padx=PADDING, pady=PADDING, sticky="nsew")
# 4
BT_MATCH = tk.Button(master=root, text='Match')
BT_MATCH.grid(column=3, row=0, padx=PADDING, pady=PADDING, sticky="nsew")
# 5
BT_OPEN_IMAGE_LIST = tk.Button(master=root, text='Import Matching Images')
BT_OPEN_IMAGE_LIST.grid(column=4, row=0, padx=PADDING, pady=PADDING, sticky="nsew")

# Image 1
CAN_IMAGE_1 = tk.Canvas(master=root, width=10, height=10, background='beige')
CAN_IMAGE_1.grid(column=0, row=1, columnspan=2, rowspan=7, padx=PADDING, pady=PADDING, sticky="nsew")

# Image 2
CAN_IMAGE_2 = tk.Canvas(master=root, width=10, height=10, background='beige')
CAN_IMAGE_2.grid(column=2, row=1, columnspan=2, rowspan=7, padx=PADDING, pady=PADDING, sticky="nsew")

# Image list
FRAME_LIST = tk.Frame(master=root, width=10, height=10, background='white')
FRAME_LIST.grid(column=4, row=1, columnspan=1, rowspan=7, padx=PADDING, pady=PADDING, sticky="nsew")
FRAME_LIST.grid_columnconfigure(0, weight=1, minsize=100)
FRAME_LIST.grid_rowconfigure(0, weight=1, minsize=E_HEIGHT)
FRAME_LIST.grid_columnconfigure(1, weight=0, minsize=0)
FRAME_LIST.grid_rowconfigure(1, weight=0, minsize=0)
FRAME_LIST.grid_propagate(0)
SCROLL_FRAME_LIST = ScrolledWindow(parent=FRAME_LIST, canv_h=80)
SCROLL_FRAME_LIST.grid(row=0, column=0, sticky='EW')
tk.Label(master=SCROLL_FRAME_LIST.scrollwindow, text='Image List').grid(column=0, row=0, columnspan=1, rowspan=1, padx=0, pady=0, sticky="nsew")

# Pallets 1
FRAME_PALLET_1 = tk.Frame(master=root, width=10, height=10, background='white')
FRAME_PALLET_1.grid(column=0, row=8, columnspan=3, rowspan=2, padx=PADDING, pady=PADDING, sticky="nsew")
FRAME_PALLET_1.grid_columnconfigure(0, weight=1, minsize=E_WIDTH)
FRAME_PALLET_1.grid_rowconfigure(0, weight=1, minsize=E_HEIGHT)
FRAME_PALLET_1.grid_columnconfigure(1, weight=0, minsize=0)
FRAME_PALLET_1.grid_rowconfigure(1, weight=0, minsize=0)
FRAME_PALLET_1.configure(background='white')
FRAME_PALLET_1.grid_propagate(0)
SCROLL_FRAME_PALLET_1 = ScrolledWindow(parent=FRAME_PALLET_1, canv_h=80)
SCROLL_FRAME_PALLET_1.grid(row=0, column=0, sticky='EW')
SCROLL_FRAME_PALLET_1.configure(background='white')
tk.Label(master=SCROLL_FRAME_PALLET_1.scrollwindow, text='Pallet').grid(column=0, row=0, columnspan=1, rowspan=1, padx=0, pady=0, sticky="nsew")
SCROLL_FRAME_PALLET_1.scrollwindow.configure(background='grey')

# Pallets 2
FRAME_PALLET_2 = tk.Frame(master=root, width=10, height=10, background='white')
FRAME_PALLET_2.grid(column=3, row=8, columnspan=2, rowspan=2, padx=PADDING, pady=PADDING, sticky="nsew")
FRAME_PALLET_2.grid_columnconfigure(0, weight=1, minsize=E_WIDTH)
FRAME_PALLET_2.grid_rowconfigure(0, weight=1, minsize=E_HEIGHT)
FRAME_PALLET_2.grid_columnconfigure(1, weight=0, minsize=0)
FRAME_PALLET_2.grid_rowconfigure(1, weight=0, minsize=0)
FRAME_PALLET_2.configure(background='white')
FRAME_PALLET_2.grid_propagate(0)
SCROLL_FRAME_PALLET_2 = ScrolledWindow(parent=FRAME_PALLET_2, canv_h=80, canv_w=80)
SCROLL_FRAME_PALLET_2.grid(row=0, column=0, sticky='EW')
SCROLL_FRAME_PALLET_2.configure(background='white')
tk.Label(master=SCROLL_FRAME_PALLET_2.scrollwindow, text='Pallet').grid(column=0, row=0, columnspan=1, rowspan=1, padx=0, pady=0, sticky="nsew")
SCROLL_FRAME_PALLET_2.scrollwindow.configure(background='blue', width=80)

# Commands
BT_OPEN_IMAGE_1.configure(command=partial(open_select_source_image, CAN_IMAGE_1, SCROLL_FRAME_PALLET_1.scrollwindow))
BT_ANALYSE.configure(command=partial(analyse, SCROLL_FRAME_PALLET_1.scrollwindow))
BT_MATCH.configure(command=partial(match, CAN_IMAGE_2, SCROLL_FRAME_LIST.scrollwindow, SCROLL_FRAME_PALLET_2.scrollwindow))
BT_OPEN_IMAGE_LIST.configure(command=partial(open_select_matching_images, CAN_IMAGE_2, SCROLL_FRAME_LIST.scrollwindow, SCROLL_FRAME_PALLET_2.scrollwindow))


# =================================================================
root.mainloop()
