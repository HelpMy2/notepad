import tkinter as tk
class find:
    def __init__(self,text):
        self.window=tk.Tk()
        self.window.title('find')
        self.window.geometry('150x75')
        self.window.resizable(False,False)
        self.text=text
        self.search_label=tk.Label(self.window,text='text to find',font=("comic sans ms",8,"normal"))
        self.search_entry=tk.Entry(self.window,font=("comic sans ms",8,"normal"))
        self.search_button=tk.Button(self.window, text='FIND', font=("comic sans ms",12,"normal"), command=self.on_find)
        self.search_label.pack()
        self.search_entry.pack()
        self.search_button.pack()
        self.find_t=('1.0','1.0')
    def on_find(self,*args):
        self.find_t=self.text.find(self.search_entry.get())
