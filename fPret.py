import tkinter as tk
from tkinter.filedialog import askopenfilename

root=tk.Tk()
tk.Tk.withdraw(root)
filename = askopenfilename()
print(filename)