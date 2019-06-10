import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import Menu, RAISED, Entry, filedialog, scrolledtext, messagebox
from pathlib import Path
import os
from os import listdir, walk, path
import json


SCREEN_WIDTH = "580"
SCREEN_HEIGHT = "380"

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.template_dir = './boilerplates/'
        self.templates = ['']
        self.template_dict = {}
        self.init_window()




    def init_window(self):
        self.master.title("Python pygame manager")  #changes window name
        self.menu_init()
        self.build_interface()
        self.find_boiler()

    def menu_init(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        new_item = Menu(menu, tearoff = 0)

        new_item.add_command(label='New', command = self.new_project)
        new_item.add_separator()
        new_item.add_command(label='Save', command = self.save_project)
        new_item.add_command(label='Save As...', command = self.save_project_as)
        new_item.add_separator()
        new_item.add_command(label='Exit', command = self.client_exit)
        menu.add_cascade(label='File', menu=new_item)



    def build_interface(self):

        self.project_dir_4json = tk.StringVar()


        frame_1 = tk.Frame(width = 640, background = '#cbdbfc')
        frame_1.grid(row = 0, sticky='w')

        self.dir_text = tk.StringVar(frame_1, value="select a project directory")

        #rows 0-1
        project_name1 = tk.Label(frame_1, text = "Project Name:", fg='black', bg = '#cbdbfc', font=("./manager_images/future.ttf", 16))
        project_name1.grid(column = 0, columnspan = 2, ipadx = 10, ipady = 20, row = 0, rowspan = 1)

        self.project_name_txt = tk.Entry(frame_1, width=30, font=("./manager_images/future.ttf", 12))
        self.project_name_txt_value = tk.StringVar(value = self.project_name_txt.get())
        self.project_name_txt.grid(column = 2, columnspan = 2, padx = 5, pady = 20, row = 0, rowspan = 1)

        #project_name_btn = tk.Button(frame_1, text = "Set Name", bg = '#639bff', font=("./manager_images/future.ttf", 16), command=self.set_name)
        #project_name_btn.grid(column = 4, columnspan = 2, padx = 5, pady = 20, row = 0, rowspan = 1)

        project_name_status = tk.Label(frame_1, text = "", fg = 'black', bg = '#cbdbfc')
        project_name_status.grid(column = 6, columnspan = 4, padx = 5, pady = 20, row = 0, rowspan = 1)

        #rows 2-3
        project_dir = tk.Label(frame_1, text = "Project Dir:", fg='black', bg = '#cbdbfc', font=("./manager_images/future.ttf", 16))
        project_dir.grid(column=0, padx=10, ipady=20, row=2, rowspan=1)

        self.project_dir_text = Entry(frame_1, width = 45, state='disabled', textvariable= self.dir_text)
        self.project_dir_text.grid(column = 1, columnspan = 2, pady = 20, row = 2, rowspan = 1)

        project_dir_button = tk.Button(frame_1, height =32, width = 32, bg = '#639bff')
        self.folderphoto = tk.PhotoImage(file="./manager_images/folder.gif")
        project_dir_button.config(image=self.folderphoto, command = self.ask_dir)
        project_dir_button.grid(column = 4, padx = 2, pady = 20, row = 2, rowspan = 1)

        ###################

        #frame 2
        frame_2 = tk.Frame(width=640, background='#cbdbfc')
        frame_2.grid(sticky='w', row=4, column=0)
        #4

        summary_lbl = tk.Label(frame_2, text = "Summary:", fg='black', bg = '#cbdbfc', font = ("./manager_images/future.ttf", 16))
        summary_lbl.grid(column=0, padx = 10, ipady = 15, row = 0, columnspan = 3)

        #5 - 9 left / row = 0 -5

        self.summary_scrolltext = scrolledtext.ScrolledText(frame_2, width=40, height = 8)
        self.summary_scrolltext.grid(column=0, columnspan = 3, padx = 3, row = 1, rowspan = 4)


        #frame_3
        #frame_3 = tk.Frame(width= 600, background='#cbdbfc')
        #frame_3.grid(row = 4, column = 0, sticky = 'e')

        type_lbl = tk.Label(frame_2, text= "Boilerplate Type:", fg='black', bg = '#cbdbfc', font = ('./manager_images/future.ttf', 16))
        type_lbl.grid(column = 4, columnspan = 2, row = 0, padx = 10, pady = 5)

        self.combo_box = Combobox(frame_2)
        self.combo_box['values'] = ['']
        self.combo_box['command'] = self.refresh()
        self.combo_box.current(0)
        self.combo_box.grid(column = 4, row = 1)


        #frame 4
        #frame_4 = tk.Frame(width = 200, background = '#cbdbfc')
        #frame_4.grid()

        #10
        copy_button = tk.Button(frame_2, height = 2, width = 20, bg = '#639bff')
        copy_button.config(text="Create boilerplate", command = self.create_boiler)
        copy_button.grid(column=4, columnspan = 2, row = 4, sticky='w', padx = 10)

    def find_boiler(self):
        d = ['']


        for (_, dirnames, _) in walk(self.template_dir):
            if dirnames == '':
                d.extend(dirnames[0])
                pass
            else:
                temp_name = self.pull_json_info(self.template_dir + dirnames[0] + '/template_info.json')
                d.extend(temp_name)
            break
        self.combo_box['values'] = d
        self.combo_box.current(0)
        print(d)



    def del_manager_dir(self, list):
        manager_dir = ['.idea', 'manager_images', 'venv']
        return [elem for elem in list if elem not in manager_dir]

    def pull_json_info(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            print("This is data" + data[0].get('Template Name'))
            self.template_dict["tn_" + data[0].get('Template Name')] = data[0].get('Template Name')
            self.template_dict["tn_" + data[0].get('Template Name') + "_author"] = data[0].get('author')
            self.template_dict["tn_" + data[0].get('Template Name') + "_summary"] = data[0].get('summary')
            self.template_dict["tn_" + data[0].get('Template Name') + "_License"] = data[0].get('License')
            self.template_dict["tn_" + data[0].get('Template Name') + "_Engine_Language"] = data[0].get('Engine or Language')
            return data[0].get('Template Name')

    def print_dict(self):
        print(self.template_dict)

    def refresh(self):
        if self.combo_box.get() in self.template_dict.values():
            print("entry found")
            self.summary_scrolltext.delete(1.0,END)
            self.summary_scrolltext.insert(INSERT, self.template_dict["tn_" + str(self.combobox.get()) + "_summary"])


    def create_boiler(self):



        pass

    def ask_dir(self):

        self.project_dir_text_var = tk.filedialog.askdirectory()

        text = tk.StringVar(value = self.project_dir_text_var)
        self.project_dir_text['textvariable'] = str(text) if self.project_dir_text_var else self.dir_text
        self.project_dir_4json = self.project_dir_text.get()


    #def set_name(self):
    #    self.project_name_4json = self.project_name_txt.get()
    #    print(self.project_name_4json)

    def new_project(self):
        pass

    def save_project(self):
        pass

    def save_project_as(self):
        pass

    def client_exit(self):
        exit()

    def create_json(self):
        json_pname = self.project_name_txt_value
        json



root = tk.Tk()
root.resizable(False, False)
#background color 203, 219, 252 or #cbdbfc
root.configure(background='#cbdbfc')
root.geometry(SCREEN_WIDTH + "x" + SCREEN_HEIGHT)  #defines the size of the window
app = Window(root)
#app.print_dict()
root.mainloop()


####
#dirname = tkinter.filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')

#project_folder = dirname

#print(dirname)

# print("Please select your project directory.")
# print("Note, the directory you select will be the main")
# print("repository for your projects. The project")
# print("manager \(no karen you can't speak with him\)")
# print("will make a sub-directory in this folder for each")
# print("individual project.")



