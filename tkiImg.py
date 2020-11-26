from tkinter import *

root = Tk()
logo = PhotoImage(file="Sourav Ganguly.gif")
w1 = Label(root,image = logo).pack(side="right")
explanation = 'This is a logo of a famous company named Adidias whose products are very costly.'
w2=Label(root,justify=LEFT,padx=10,text=explanation).pack(side="left")

root.mainloop()