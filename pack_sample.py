import tkinter as tk

root = None
count = 0

def addBt(root,sideToPack):
   global count
   name = "Button : "+str(count)+" "+sideToPack
   bt=tk.Button(root,text=name)
   bt.pack(side=sideToPack)
   count+=1

def main():
   global root
   root = tk.Tk()
   addBt(root,'left')
   addBt(root,'bottom')
   addBt(root,'right')
   addBt(root,'bottom')
   frame1 = tk.Frame(root)
   addBt(frame1,'top')
   addBt(frame1,'top')
   addBt(frame1,'top')
   addBt(frame1,'top')
   addBt(frame1,'top')
   frame1.pack()
   root.mainloop()

main()