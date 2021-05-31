import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid_dim = 10
        self.grid(row=0, column=0, sticky="nsew")
        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()
        print(top)
        top.grid_columnconfigure(0, weight=1)
        top.grid_rowconfigure(0, weight=1)
        top.minsize(800, 400)
        for x in range(self.grid_dim):
            self.grid_columnconfigure(x, weight=1, minsize=50)
            self.grid_rowconfigure(x, weight=1, minsize=50)
            tk.Button(self, text='Quit', command=self.quit).grid(row=x, column=x,padx=5, pady=5, sticky="nsew")
        # self.bt_quit = tk.Button(self, text='Quit', command=self.quit)
        # self.bt_quit.grid(row=0, column=0,
        #                   sticky=tk.N+tk.S+tk.E+tk.W)


app = Application()
app.master.title('Sample application')
app.mainloop()
print(app)

window = tk.Tk()
print(window)
window.geometry("1000x500")
window.resizable(False, False)
window.title('Cloths Matching')

# geet screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()


greeting = tk.Label(text="Hello, Tkinter",
                    width=10,
                    height=10)
# register Label component
greeting.pack()

button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)

button.pack()


entry = tk.Entry(fg="yellow", bg="blue", width=50)
entry.pack()


# start event loop
window.mainloop()


# get mouse position
# x = window.winfo_pointerx()
# y = window.winfo_pointery()
# abs_coord_x = window.winfo_pointerx() - window.winfo_vrootx()
# abs_coord_y = window.winfo_pointery() - window.winfo_vrooty()

# image crop
# https://stackoverflow.com/questions/52375035/cropping-an-image-in-tkinter/52375463
