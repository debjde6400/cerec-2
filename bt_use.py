from tkinter import *

class App:
   def __init__(self,master):
       frame = Frame(master)
       frame.pack()
       self.button = Button(frame,text='QUIT',fg='red',command=frame.quit)
       self.button.pack(side=LEFT)
       self.slogan = Button(frame,text='Holla',fg='green',command=self.write_slogan)
       self.slogan.pack(side=LEFT)
   def write_slogan(self):
       print('SENSEX(Sensitivity Index) is a measure of performance of Indian stock market.')

root = Tk()
app = App(root)
root.mainloop()
