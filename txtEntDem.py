import tkinter as tk

root = None

entryBox = None

def btPush():
   global entryBox
   text = entryBox.get()
   print("Your text : ",text)

def crtTxtBox(parent):
   global entryBox
   entryBox = tk.Entry(parent)
   entryBox.pack()

def main():
   global root
   root = tk.Tk()
   mbt = tk.Button(root,text="Show text",command=btPush)
   mbt.pack()
   crtTxtBox(root)
   root.mainloop()

main()