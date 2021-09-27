import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import colorchooser
from threading import Thread
import json

#from GUI.edit import find
class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl regular expression syntax.
        '''

        start = self.index('1.0')
        end = self.index(tk.END)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")
class notepad:
    def __init__(self,file : "to open" = '' ,text: "text to display" = '' ,safe: "only to read" = False,settings:dict={}):
        self.settings=settings
        self.window=tk.Tk()
        self.window.geometry(settings['geometry'])
        self.window.title('notepad')
        self.window.bind('<Configure>',self.on_configure)
        self.window.bind('<Key>',self.key_event)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        # open file
        try:
            f = open(file)
            self.text=f.read() # чтение содержимого файла
            self.file_path=file
            f.close()
            del f
        except FileNotFoundError as error: # если произошла ошибка открытия файла
            if file!='':# если параметр file был изменён
                mb.showerror('OPEN FILE ERROR',error) # вызов окна ошибки
            self.text=text
            self.file_path=None
        except Exception as error:
            print(error)

        # создание поля редактирования
        if safe:
            self.text_entry=tk.Label(self.window,text=self.text,bg=settings['bg'],fg=settings['fg'],font=settings['font'])
            width,height= settings['geometry'].split('+')[0].split('x')
            self.text_entry.place(width=width,height=height)
        else:
            self.text_entry=CustomText(self.window,bg=settings['bg'],fg=settings['fg'],bd=settings['bd'],insertbackground=settings['fg'],undo=True,font=settings['font'])
            self.text_entry.insert('1.0', self.text)
            width,height= settings['geometry'].split('+')[0].split('x')
            self.text_entry.place(width=width,height=height)
            tk.Scrollbar(self.text_entry,command=self.text_entry.yview).pack(side=tk.RIGHT, fill=tk.Y)

        #file,edit,.. menus
        self.menu=tk.Menu(self.window)
        self.window.config(menu=self.menu)
        #file menu
        self.filemenu = tk.Menu(self.menu,tearoff=0)
        self.filemenu.add_command(label='Open',command=self.open)
        self.filemenu.add_command(label='New',command=lambda:Thread(target=self.new).start())
        self.filemenu.add_command(label='Save',command=self.save)
        self.filemenu.add_command(label='Save as',command=self.save_as)
        #edit menu
        self.editmenu = tk.Menu(self.menu, tearoff=0)
        self.editmenu.add_command(label='Find',command=self.find)
        #add menus
        self.menu.add_cascade(label="File",menu=self.filemenu)
        self.menu.add_cascade(label="Edit",menu=self.editmenu)
        #self.menu.add_command(label='Settings', command=self.Settings)
        Thread(target=self.upd, daemon=True).start()
    def on_configure(self,*args):
        self.text_entry.place(width=self.window.winfo_width(),height=self.window.winfo_height())
        self.text_entry.update()
        print(args,self.window.winfo_width())
    def new(self,*args,file=''):
        settings=self.settings
        g=settings['geometry']
        g=[s.split('x') for s in g.split('+')]
        g[1][0]=(int(g[1][0])+50)%400
        g[2][0] = (int(g[2][0])+50)%400
        settings['geometry']=str(g[0][0])+'x'+str(g[0][1])+'+'+str(g[1][0])+'+'+str(g[2][0])
        work=notepad(settings=settings,file=file)
        work.window.mainloop()
    def open(self,*args):
        f = filedialog.askopenfile('r',initialfile=self.file_path)
        if self.text_entry.get('1.0',tk.END)=='' and self.file_path!=None:
            self.text_entry.delete('1.0',tk.END)
            self.text_entry.insert('1.0',f.read)
        else:
            self.new(file=f.name)
        f.close()
        del f
    def save(self,*args):
        if self.file_path!='':
            try:
                f=open(self.file_path,'w')
            except Exception as error:
                print(error)
        else:
            f = filedialog.asksaveasfile('w',initialfile=self.file_path)
        f.write(self.text_entry.get("1.0",tk.END))
        f.close()
        del f
    def save_as(self,*args):
        f = filedialog.asksaveasfile('w')
        f.write(self.text_entry.get("1.0",tk.END))
        f.close()
        del f
    def find(self,*args):
        find_window=tk.Tk()
        find_window.title('find')
        find_window.geometry('150x75')
        find_window.resizable(False,False)
        self.search_label = tk.Label(find_window, text='text to find', font=("comic sans ms", 8, "normal"))
        self.search_entry = tk.Entry(find_window, font=("comic sans ms", 8, "normal"))
        self.search_button = tk.Button(find_window, text='FIND', font=("comic sans ms", 8, "normal"),command=self.on_find)
        self.clear_button = tk.Button(find_window, text='CLEAR', font=("comic sans ms", 8, "normal"),command=self.find_clear)
        self.search_label.pack()
        self.search_entry.pack()
        self.search_button.place(rely=0.6,relx=0.1)
        self.clear_button.place(rely=0.6,relx=0.6)
    def on_find(self,*args):
        self.text_entry.tag_configure("find", foreground=self.settings['find_color'])
        to_find = self.search_entry.get()
        self.text_entry.highlight_pattern(to_find,"find",'1.0',tk.END)
    def find_clear(self):
        to_clear=self.text_entry.get('1.0',tk.END)
        self.text_entry.tag_delete("find")
    def key_event(self,event):
        if event.char=='\x0e':
            self.new()
        elif event.char=='\x11':
            self.window.destroy()
        elif event.char=='\x0f':
            self.open()
        elif event.char=='\x13':
            self.save()
        else:
            print(event.char)
    def Settings(self,*args):
        settings_window=tk.Tk()
        settings_window.configure(bg=self.settings['bg'])
        settings_window.title('settings')
        settings_window.geometry('360x512')
        settings_window.resizable(False,False)
        # settings tabs
        tabControl = ttk.Notebook(settings_window)
        font_tab=ttk.Frame(tabControl)
        color_tab=ttk.Frame(tabControl)
        tabControl.add(font_tab,text="font")
        tabControl.add(color_tab,text="colors")
        tabControl.pack(expand=1, fill="both")
        ttk.Label(font_tab, text='NOTHING').grid()
        ttk.Button(color_tab,text='BACKGROUND',command=lambda:self.settings_set('bg',colorchooser.askcolor(title ="Choose color")[-1])).grid(column=1,row=0)
        ttk.Button(color_tab,text='FOREGROUND',command=lambda:self.settings_set('fg',colorchooser.askcolor(title ="Choose color")[-1])).grid(column=1,row=1)

    def settings_set(self,name='',value=''):
        if type(name)==str:
            self.settings[name]=value
        elif type(name)==type(value)==list:
            for n,v in name,value:
                self.settings[n]=v
        self.update()
    def update(self):
        settings=self.settings
        self.text_entry.configure(bg=settings['bg'],fg=settings['fg'],bd=settings['bd'],insertbackground=settings['fg'],font=settings['font'])
    def on_closing(self,*args):
        with open('settings.json', 'w') as sf:
            sf.write(json.dumps(self.settings, separators=(',\n    ', ':')))
            sf.close()
        self.window.quit()
    def upd(self):
        import time
        while True:
            time.sleep(1)
            self.settings['geometry'] = self.window.geometry()