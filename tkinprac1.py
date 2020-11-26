import tkinter as tk

root = None

def buttonPushed():
   global root
   root.destroy()   #kill the root window

def main():
   global root
   root = tk.Tk()
   w=tk.Label(root,text = "Holla! It's a practice!!")
   w.pack()   #put the label into window
   mbt = tk.Button(root,text="Exit",command=buttonPushed)
   mbt.pack()
   root.mainloop()

main()