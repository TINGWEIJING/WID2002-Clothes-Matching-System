import tkinter as tk

window = tk.Tk()
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