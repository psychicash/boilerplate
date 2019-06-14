from tkinter import *
from tkinter.ttk import *
from tkinter import Menu, RAISED, Entry, filedialog, scrolledtext, messagebox
from os import listdir, walk, path, remove, startfile
import json
from errno import ENOTDIR
from shutil import copyfile, copy, copytree
from sys import platform

print("imports are done")

SCREEN_WIDTH = "580"
SCREEN_HEIGHT = "480"
#background color 203, 219, 252 or #cbdbfc
BG_COLOR_HEX = '#cbdbfc'
BG_COLOR_RBG = (203, 219, 252)
BUT_COLOR_HEX = '#639bff'

class popupWindow(object):
    def __init__(self, win):
        self.win = win
        top = self.top = Toplevel(win)
        top.geometry('220x120')
        self.l = Label(top, text="Settings")
        self.l.grid(column = 0, columnspan = 4, row = 0, pady = 10)
        self.l = Label(top, text = "Author:")
        self.l.grid(column = 0, row = 1, rowspan = 2, padx = 10)
        self.e = Entry(top, textvariable = self.win.author)
        self.e.grid(column = 1, row = 1, rowspan = 2)
        self.b = Button(top, text='Ok', command = self.cleanup)
        self.b.grid(column = 0, columnspan = 4, row = 4, rowspan = 2, pady = 10, padx = 20)

    def cleanup(self):
        self.value = self.e.get()
        self.win.author = self.value
        self.settings_data = {'Project Author': ''}
        self.settings_data.update([('Project Author', self.win.author)])
        with open('settings.json', 'r') as infile:
            data = json.load(infile)
            data[0]['Project Author'] = self.win.author

        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        self.top.destroy()


class Window(Frame):
    def __init__(self, master=None):
        global BG_COLOR_HEX, BUT_COLOR_HEX
        Frame.__init__(self, master)
        self.author = StringVar()
        self.author.set('')
        self.master = master
        self.template_dir = './boilerplates/'
        self.dir_local = "select a project directory"
        self.templates = ['']
        self.template_dict = {}
        self.pull_settings_info()
        self.init_window()

    def pull_settings_info(self):
        with open('settings.json') as json_file:
            data = json.load(json_file)
            try:
                self.author.set(data[0].get('Project Author'))
                if data[0].get('Project Directory') != '' and data[0].get('Project Directory') != self.dir_local:
                    self.dir_local = data[0].get('Project Directory')
                else:
                    print("directory failed to load")
                print("settings hath been loaded")
            except:
                print("settings did not load")
                pass

    def init_window(self):
        self.master.title("Template Manager")
        self.menu_init()
        self.build_interface()
        self.find_boiler()

    def menu_init(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        new_item = Menu(menu, tearoff = 0)

        new_item.add_command(label='New', command = self.new_project)
        new_item.add_separator()
        new_item.add_command(label='Settings', command=self.edit_settings)
        new_item.add_separator()
        new_item.add_command(label='Exit', command = self.client_exit)
        menu.add_cascade(label='File', menu=new_item)

    def edit_settings(self):
        self.w = popupWindow(self)
        self.master.wait_window(self.w.top)

    def build_interface(self):
        self.project_dir_4json = StringVar()

        frame_1 = Frame(width = 640, background = BG_COLOR_HEX)
        frame_1.grid(row = 0, sticky='w')

        self.dir_text = StringVar(frame_1, value=self.dir_local)

        #rows 0-1
        project_name1 = Label(frame_1, text = "Project Name:", fg='black', bg = BG_COLOR_HEX, font=("./manager_images/future.ttf", 16))
        project_name1.grid(column = 0, columnspan = 2, ipadx = 10, ipady = 20, row = 0, rowspan = 1)

        self.project_name_txt = Entry(frame_1, width=30, font=("./manager_images/future.ttf", 12))
        self.project_name_txt_value = StringVar(value = self.project_name_txt.get())
        self.project_name_txt.grid(column = 2, columnspan = 2, padx = 5, pady = 20, row = 0, rowspan = 1)

        project_name_status = Label(frame_1, text = "", fg = 'black', bg = BG_COLOR_HEX)
        project_name_status.grid(column = 6, columnspan = 4, padx = 5, pady = 20, row = 0, rowspan = 1)

        #rows 2-3
        project_dir = Label(frame_1, text = "Project Dir:", fg='black', bg = BG_COLOR_HEX, font=("./manager_images/future.ttf", 16))
        project_dir.grid(column=0, padx=10, ipady=20, row=2, rowspan=1)

        self.project_dir_text = Entry(frame_1, width = 45, state='disabled', textvariable= self.dir_text)
        self.project_dir_text.grid(column = 1, columnspan = 2, pady = 20, row = 2, rowspan = 1)

        project_dir_button = Button(frame_1, height =32, width = 32, bg = BUT_COLOR_HEX)
        self.folderphoto = PhotoImage(file="./manager_images/folder.gif")
        project_dir_button.config(image=self.folderphoto, command = self.ask_dir)
        project_dir_button.grid(column = 4, padx = 2, pady = 20, row = 2, rowspan = 1)

        #frame 2
        frame_2 = Frame(width=640, background=BG_COLOR_HEX)
        frame_2.grid(sticky='w', row=4, column=0)

        #4
        summary_lbl = Label(frame_2, text = "Summary:", fg='black', bg = BG_COLOR_HEX, font = ("./manager_images/future.ttf", 16))
        summary_lbl.grid(column=0, padx = 10, ipady = 15, row = 0, columnspan = 3)

        #5 - 9 left / row = 0 -5

        self.summary_scrolltext = scrolledtext.ScrolledText(frame_2, width=40, height = 10)
        self.summary_scrolltext.grid(column=0, columnspan = 3, padx = 3, row = 1, rowspan = 4)


        type_lbl = Label(frame_2, text= "Boilerplate Type:", fg='black', bg = BG_COLOR_HEX, font = ('./manager_images/future.ttf', 16))
        type_lbl.grid(column = 4, columnspan = 2, row = 0, padx = 10)

        self.combo_box = Combobox(frame_2, state='readonly')
        self.combo_box.bind("<<ComboboxSelected>>", self.tk_ref)
        self.combo_box['values'] = ['']
        self.combo_box.current(0)
        self.combo_box.grid(column = 4, row = 1)

        self.language_lbl = Label(frame_2, text = "Language/Engine", fg='black', bg=BG_COLOR_HEX, font=('./manager_images/future.ttf', 16))
        self.language_lbl.grid(column = 4, row = 2, padx =10, pady=5)

        self.lang_entry_value = StringVar()
        self.lang_entry = Entry(frame_2, width = 25, textvariable=self.lang_entry_value)
        self.lang_entry.grid(column= 4, columnspan = 2, row = 3, padx = 3)

        self.license_lbl = Label(frame_2, text="License:", fg='black', bg=BG_COLOR_HEX,
                                    font=("./manager_images/future.ttf", 16))
        self.license_lbl.grid(column=4, row=4, padx=10)

        self.license_combo = Combobox(frame_2, state='readonly')
        self.license_list = ('None', 'CC Attribution 4.0', 'Apache', 'GNU Public', 'GNU Lesser', 'GNU Ver 3.0', 'MIT', 'Mozilla Public', 'Unlicense')
        self.license_combo['values'] = ['None', 'CC Attribution 4.0', 'Apache', 'GNU Public', 'GNU Lesser', 'GNU Ver 3.0', 'MIT', 'Mozilla Public', 'Unlicense']
        self.license_local = {'None': '', 'CC Attribution 4.0': 'cca4point0.txt', 'Apache': 'apache.txt',
                              'GNU Public': 'gnu_general_public.txt', 'GNU Lesser': 'gnu_lesser_public.txt',
                              'GNU Ver 3.0': 'gnuver3.txt', 'MIT': 'mit.txt',
                              'Mozilla Public': 'mozilla_public.txt', 'Unlicense': 'unlicense.txt'}
        self.license_combo.current(0)
        self.license_combo.grid(column=4, row=5, pady=5)

        #frame 4
        frame_4 = Frame(width = 200, background = BG_COLOR_HEX)
        frame_4.grid()

        #10
        copy_button = Button(frame_4, height = 2, width = 20, bg = BUT_COLOR_HEX)
        copy_button.config(text="Create boilerplate", command = self.create_boiler)
        copy_button.grid(column=4, columnspan = 2, row = 4, sticky='w', padx = 10, pady = 5)

    def find_boiler(self):
        d = ['']

        for (_, dirnames, _) in walk(self.template_dir):

            for i in range(len(dirnames)):
                if dirnames[i] == '':
                    d.extend(dirnames[i])

                    pass
                else:
                    temp_name = self.pull_json_info(self.template_dir + dirnames[i] + '/template_info.json')
                    d.append(temp_name)

            break
        self.combo_box['values'] = d
        self.combo_box.current(0)

    def del_manager_dir(self, list):
        manager_dir = ['.idea', 'manager_images', 'venv']
        return [elem for elem in list if elem not in manager_dir]

    def pull_json_info(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            self.template_dict["tn_" + data[0].get('Template Name')] = data[0].get('Template Name')
            self.template_dict["tn_" + data[0].get('Template Name') + "_author"] = data[0].get('author')
            self.template_dict["tn_" + data[0].get('Template Name') + "_Summary"] = data[0].get('Summary')
            self.template_dict["tn_" + data[0].get('Template Name') + "_License"] = data[0].get('License')
            self.template_dict["tn_" + data[0].get('Template Name') + "_Engine_Language"] = data[0].get('Engine or Language')
            return data[0].get('Template Name')

    def print_dict(self):
        print(self.template_dict)

    def tk_ref(self, event):
        if self.combo_box.get() in self.template_dict.values() and self.combo_box.get() != '':
            
            self.summary_scrolltext.delete('1.0', END)
            self.summary_scrolltext.insert(INSERT, self.template_dict.get("tn_" + str(self.combo_box.get()) + "_Summary"))
            self.lang_entry.delete(0, END)
            self.lang_entry.insert(0, self.template_dict.get("tn_" + str(self.combo_box.get()) + "_Engine_Language"))
            if self.template_dict.get("tn_" + str(self.combo_box.get()) + "_License"):
                x = self.license_list.index(self.template_dict.get("tn_" + str(self.combo_box.get()) + "_License"))
            else:
                x = 0
            self.license_combo.current(x)
        else:
            pass

    def create_boiler(self):

        if self.project_dir_text.get() == '' and self.project_dir_text.get() == self.dir_text:
            pass
        else:
            try:
                #make directory at the path provided based on the name
                my_path = self.project_dir_text.get() + '/' + self.project_name_txt.get()
                ''.join(e for e in my_path if e.isalnum())

                #copy contents of the selected template to the directory in question
                self.source_dir = ''

                for (_, dirnames, _) in walk(self.template_dir):

                    for i in range(len(dirnames)):
                        working_dir = self.template_dir + dirnames[i] + '/template_info.json'
                        with open(working_dir) as json_file:
                            data = json.load(json_file)
                            if data[0].get('Template Name') == self.combo_box.get():
                                self.source_dir = self.template_dir + dirnames[i]
                    break

                self.source = self.source_dir
                #self.source_dir = self.source_dir + '/template_info.json'
                self.copyanything(self.source, my_path)

                self.create_json()

                #then copy over the temp json file with the settings/desc

                copyfile('./json_temp.json', my_path + '/project_info.json')
                # rename json file in target dir

                # del tempfile in manager dir
                remove('./json_temp.json')

                #copy the license over and rename it
                if self.license_combo.get() == 'None':
                    pass
                else:
                    license_file = self.license_local.get(self.license_combo.get())
                    location = './licenses/' + license_file
                    copyfile(location, my_path + '/license.txt')

                #remove template json with old info
                remove(my_path + '/template_info.json')

                if platform == "linux" or platform == "linux2":
                    # linux
                    messagebox.showinfo("Task Complete", "Your you new project directory has been created.")
                    pass
                elif platform == "darwin":
                    # OS X
                    messagebox.showinfo("Task Complete", "Your you new project directory has been created.")
                    pass
                elif platform == "win32":
                    # Windows...
                    if messagebox.askyesno("Task Complete", "Your you new project directory has been created. Open project directory?"):
                        startfile(my_path)
                    else:
                        pass
                else:
                    pass

            except FileExistsError as error:
                messagebox.showerror("Error - File Exsists", "There is already a project by this name in the project directory. Please rename or remove the old project.")


    def copyanything(self, src, dst):
        try:
            copytree(src, dst)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                copy(src, dst)
            else:
                raise

    def ask_dir(self):

        self.project_dir_text_var = filedialog.askdirectory()

        text = StringVar(value = self.project_dir_text_var)
        self.project_dir_text['textvariable'] = str(text) if self.project_dir_text_var else self.dir_text
        self.project_dir_4json = self.project_dir_text.get()

        try:
            with open('settings.json', 'r') as infile:
                data = json.load(infile)
                data[0]['Project Directory'] = self.project_dir_4json

            with open('settings.json', 'w') as outfile:
                json.dump(data, outfile, indent=4)
        except ValueError as e:
            if str(e) != 'json.decoder.JSONDecodeError':
                raise
            else:
                self.settings_dict = {"Project Author": self.author, "Project Directory": self.project_dir_4json}

                with open('settings.json', 'w') as f:
                    json.dump(self.settings_dict, f, indent = 4)






    def new_project(self):
        self.project_name_txt.delete(0, 'end')
        self.project_dir_text['textvariable'] = self.dir_text
        self.summary_scrolltext.delete('1.0', END)
        self.combo_box.current(0)
        self.lang_entry.delete(0, 'end')


    def save_project(self):
        pass

    def save_project_as(self):
        pass

    def client_exit(self):
        exit()

    def create_json(self):
        json_data = {'Project Name': '', 'Project Summary': '', 'Project Language': '', 'Project License': '', 'Project Author': ''}

        json_data.update([('Project Name', self.project_name_txt.get())])
        json_data.update([('Project Summary', self.summary_scrolltext.get('1.0', 'end-1c'))])
        json_data.update([('Project Language', self.lang_entry.get())])
        json_data.update([('Project Author', str(self.author.get()))])
        json_data.update([('Project License', self.license_combo.get())])
        with open('json_temp.json', 'w') as outfile:
            json.dump(json_data, outfile, indent = 4)



root = Tk()
root.resizable(False, False)
root.configure(background=BG_COLOR_HEX)
root.geometry(SCREEN_WIDTH + "x" + SCREEN_HEIGHT)
app = Window(root)

root.mainloop()