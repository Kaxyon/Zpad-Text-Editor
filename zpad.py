from tkinter import *
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox
import os
from typing import ContextManager, Match

root = Tk()
root.title('Zpad Text Editor')
root.geometry('1200x800')
root.wm_iconbitmap('icon.ico')

############################# main menu #############################
main_menu = Menu(root)

#file icons
new_icon = PhotoImage(file='icons/new.png')
open_icon = PhotoImage(file='icons/open.png')
save_icon = PhotoImage(file='icons/save.png')
saveas_icon = PhotoImage(file='icons/save_as.png')
exit_icon = PhotoImage(file='icons/exit.png')

file = Menu(main_menu, tearoff=0)

#edit icons
copy_icon = PhotoImage(file='icons/copy.png')
paste_icon = PhotoImage(file='icons/paste.png')
cut_icon = PhotoImage(file='icons/cut.png')
clearall_icon = PhotoImage(file='icons/clear_all.png')
find_icon = PhotoImage(file='icons/find.png')

edit = Menu(main_menu, tearoff=0)

#view icons
toolbar_icon = PhotoImage(file='icons/tool_bar.png')
statusbar_icon = PhotoImage(file='icons/status_bar.png')

view = Menu(main_menu, tearoff=0)

#color theme icons
light_default_icon = PhotoImage(file='icons/light_default.png')
light_plus_icon = PhotoImage(file='icons/light_plus.png')
dark_icon = PhotoImage(file='icons/dark.png')
red_icon = PhotoImage(file='icons/red.png')
monokai_icon = PhotoImage(file='icons/monokai.png')
night_blue_icon = PhotoImage(file='icons/night_blue.png')

colortheme = Menu(main_menu, tearoff=0)

theme_choice = StringVar()
color_icons = (light_default_icon, light_plus_icon, dark_icon, red_icon, monokai_icon, night_blue_icon)

color_dict = {
    'Light Default' : ('#000000', '#ffffff'),
    'Light Plus' : ('#474747', '#e0e0e0'),
    'Dark' : ('#c4c4c4', '#2d2d2d'),
    'Red' : ('#2d2d2d', '#ffe8e8'),
    'Monokai' : ('#d3b744', '#474747'),
    'Night Blue' : ('#ededed', '#6b9dc2')
}

# Cascade
main_menu.add_cascade(label='File', menu=file)
main_menu.add_cascade(label='Edit', menu=edit)
main_menu.add_cascade(label='View', menu=view)
main_menu.add_cascade(label='Color Theme', menu=colortheme)
############################# end main menu #############################


############################# toolbar #############################
tool_bar = ttk.Label(root)
tool_bar.pack(side=TOP, fill=X)

# font box
font_tuple = font.families()
font_family = StringVar()
font_box = ttk.Combobox(tool_bar, width=30, textvariable=font_family, state='readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0, column=0, padx=5)

# size box
size_var = IntVar()
font_size = ttk.Combobox(tool_bar, width=14, textvariable=size_var, state='readonly')
font_size['values'] = tuple(range(2, 81, 2))
font_size.current(6)
font_size.grid(row=0, column=1, padx=5)

#Buttons
# bold
bold_icon = PhotoImage(file='icons/bold.png')
bold_btn = ttk.Button(tool_bar, image=bold_icon)
bold_btn.grid(row=0, column=2, padx=5)

# italic
italic_icon = PhotoImage(file='icons/italic.png')
italic_btn = ttk.Button(tool_bar, image=italic_icon)
italic_btn.grid(row=0, column=3, padx=5)

# underline
underline_icon = PhotoImage(file='icons/underline.png')
underline_btn = ttk.Button(tool_bar, image=underline_icon)
underline_btn.grid(row=0, column=4, padx=5)

# font color
font_color_icon = PhotoImage(file='icons/font_color.png')
font_color_btn = ttk.Button(tool_bar, image=font_color_icon)
font_color_btn.grid(row=0, column=5, padx=5)

# align left
align_left_icon = PhotoImage(file='icons/align_left.png')
align_left_btn = ttk.Button(tool_bar, image=align_left_icon)
align_left_btn.grid(row=0, column=6, padx=5)

# align right
align_center_icon = PhotoImage(file='icons/align_center.png')
align_center_btn = ttk.Button(tool_bar, image=align_center_icon)
align_center_btn.grid(row=0, column=7, padx=5)

align_right_icon = PhotoImage(file='icons/align_right.png')
align_right_btn = ttk.Button(tool_bar, image=align_right_icon)
align_right_btn.grid(row=0, column=8, padx=5)
# align left
############################# end toolbar #############################


############################# text editor #############################
text_editor = Text(root)
text_editor.config(wrap=WORD, relief=FLAT)

scroll_bar = ttk.Scrollbar(root)
text_editor.focus_set()
scroll_bar.pack(side=RIGHT, fill=Y)
text_editor.pack(fill=BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)

######## font family and font size functionality
current_font_family = 'Arial'
current_font_size = 14

def change_font(root):
    global current_font_size
    current_font_family = font_family.get()
    text_editor.configure(font=(current_font_family, current_font_size))

def change_size(root):
    global current_font_size
    current_font_size = size_var.get()
    text_editor.configure(font=(current_font_family, current_font_size))

font_box.bind("<<ComboboxSelected>>", change_font)
font_size.bind("<<ComboboxSelected>>", change_size)

text_editor.configure(font=('Arial', 14))

######## buttons functionality

# bold button functionality
def change_bold():
    text_property = font.Font(font=text_editor['font'])
    if text_property.actual()['weight'] == 'normal':
        text_editor.configure(font=(current_font_family, current_font_size, 'bold'))
    if text_property.actual()['weight'] == 'bold':
        text_editor.configure(font=(current_font_family, current_font_size, 'normal'))

bold_btn.configure(command=change_bold)

# italic button functionality
def change_italic():
    text_property = font.Font(font=text_editor['font'])
    if text_property.actual()['slant'] == 'roman':
        text_editor.configure(font=(current_font_family, current_font_size, 'italic'))
    if text_property.actual()['slant'] == 'italic':
        text_editor.configure(font=(current_font_family, current_font_size, 'roman'))

italic_btn.configure(command=change_italic)

# underline button functionality
def change_underline():
    text_property = font.Font(font=text_editor['font'])
    if text_property.actual()['underline'] == 0:
        text_editor.configure(font=(current_font_family, current_font_size, 'underline'))
    if text_property.actual()['underline'] == 1:
        text_editor.configure(font=(current_font_family, current_font_size, 'normal'))

underline_btn.configure(command=change_underline)

# font color functionality
def change_font_color():
    color_var = colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])

font_color_btn.configure(command=change_font_color)

# align functionality
#==left
def align_left():
    text_content = text_editor.get(1.0, END)
    text_editor.tag_config(LEFT, justify=LEFT)
    text_editor.delete(1.0, END)
    text_editor.insert(INSERT, text_content, LEFT)

align_left_btn.configure(command=align_left)


#==center
def align_center():
    text_content = text_editor.get(1.0, END)
    text_editor.tag_config(CENTER, justify=CENTER)
    text_editor.delete(1.0, END)
    text_editor.insert(INSERT, text_content, CENTER)

align_center_btn.configure(command=align_center)


#==right
def align_right():
    text_content = text_editor.get(1.0, END)
    text_editor.tag_config(RIGHT, justify=RIGHT)
    text_editor.delete(1.0, END)
    text_editor.insert(INSERT, text_content, RIGHT)

align_right_btn.configure(command=align_right)
############################# end text editor #############################


############################# status bar #############################
status_bar = ttk.Label(root, text='Status Bar')
status_bar.pack(side=BOTTOM)

text_changed = False
def changed(event=None):
    global text_changed
    text_changed = True
    if text_editor.edit_modified():
        words = len(text_editor.get(1.0, 'end-1c').split())
        chararcters = len(text_editor.get(1.0, 'end-1c'))
        status_bar.config(text=f"Characters : {chararcters} Words : {words}")
    text_editor.edit_modified(False)
text_editor.bind('<<Modified>>', changed)
############################# end status bar #############################

############################# main menu functionality#############################

## variable
url = ''

## new functionality
def new_file(event=None):
    global url
    url = ''
    text_editor.delete(1.0, END)

## open functionality
def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '*.txt'), ('All Files', '*.*')))
    try:
        with open(url, 'r') as fr:
            text_editor.delete(1.0, END)
            text_editor.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except:
        return
    root.title(os.path.basename(url))

## save functionality
def save_file(event=None):
    global url 
    try:
        if url:
            content = str(text_editor.get(1.0, END))
            with open(url, 'w', encoding='utf-8') as fw:
                fw.write(content)
        else:
            url = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
            content2 = text_editor.get(1.0, END)
            url.write(content2)
            url.close()
    except:
        return 

## save as functionality
def save_as_file(event=None):
    global url 
    try:
        content = text_editor.get(1.0, END)
        url = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
        url.write(content)
        url.close()
    except:
        return

## exit functionality
def exit_func(event=None):
    global url, text_changed
    try:
        if text_changed:
            mbox = messagebox.askyesnocancel('Warning', 'Do you want to save the file?')         
            if mbox is True:
                if url:
                    content = text_editor.get(1.0, END)
                    with open(url, 'w', encoding='utf-8') as wf:
                        wf.write(content)
                        root.destroy()
                else:
                    content2 = str(text_editor.get(1.0, END))
                    url = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
                    url.write(content2)
                    url.close()
                    root.destroy()
            elif mbox is False:
                root.destroy()
        else:
            root.destroy()   
    except:
        return
# file commmands
file.add_command(label='New', image=new_icon, compound=LEFT, accelerator='Ctrl+N', command=new_file)
file.add_command(label='Open', image=open_icon, compound=LEFT, accelerator='Ctrl+O', command=open_file)
file.add_command(label='Save', image=save_icon, compound=LEFT, accelerator='Ctrl+S', command=save_file)
file.add_command(label='Save As', image=saveas_icon, compound=LEFT, accelerator='Ctrl+Alt+S', command=save_as_file)
file.add_command(label='Exit', image=exit_icon, compound=LEFT, accelerator='Ctrl+Q', command=exit_func)

## find functionality
def find_func(event=None):

    def find():
        word = find_entry.get()
        text_editor.tag_remove('match', '1.0', END)
        matches = 0
        if word:
            start_pos = '1.0'
            while True:
                start_pos = text_editor.search(word, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                text_editor.tag_add('match', start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                text_editor.tag_config('match',foreground='red', background='yellow')

    def replace(event=None):
        word = find_entry.get()
        replace_word = replace_entry.get()
        content = text_editor.get(1.0, END)
        new_content = content.replace(word, replace_word)
        text_editor.delete(1.0, END)
        text_editor.insert(1.0 ,new_content)





    find_dialogue = Toplevel()
    find_dialogue.geometry('450x250+500+200')
    find_dialogue.title('Find')
    find_dialogue.resizable(0,0)

    # frame
    find_frame = LabelFrame(find_dialogue, text='Find/Replace')
    find_frame.pack(pady=20)

    # label
    text_find_label = ttk.Label(find_frame, text='Find : ')
    text_replace_label = ttk.Label(find_frame, text='Replace : ')

    # entry box
    find_entry = ttk.Entry(find_frame, width=30)
    replace_entry = ttk.Entry(find_frame, width=30)

    # buttons
    find_btn = ttk.Button(find_frame, text='Find', command=find)
    replace_btn = ttk.Button(find_frame, text='Replace', command=replace)

    # label grid
    text_find_label.grid(row=0, column=0, padx=4, pady=4)
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)

    # entry box grid
    find_entry.grid(row=0, column=1, padx=4, pady=4)
    replace_entry.grid(row=1, column=1, padx=4, pady=4)

    # buttons grid
    find_btn.grid(row=2, column=0, padx=8, pady=4)
    replace_btn.grid(row=2, column=1, padx=8, pady=4)

    find_dialogue.mainloop()



# edit commmands
edit.add_command(label='Copy', image=copy_icon, compound=LEFT, accelerator='Ctrl+C', command=lambda : text_editor.event_generate('<Control c>'))
edit.add_command(label='Paste', image=paste_icon, compound=LEFT, accelerator='Ctrl+V', command=lambda : text_editor.event_generate('<Control v>'))
edit.add_command(label='Cut', image=cut_icon, compound=LEFT, accelerator='Ctrl+X', command=lambda : text_editor.event_generate('<Control x>'))
edit.add_command(label='Clear All', image=clearall_icon, compound=LEFT, accelerator='Ctrl+Shift+X', command=lambda : text_editor.delete(1.0, END))
edit.add_command(label='Find', image=find_icon, compound=LEFT, accelerator='Ctrl+F', command=find_func)

# view commmands
show_toolbar = BooleanVar()
show_toolbar.set(True)
show_statusbar = BooleanVar()
show_statusbar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar.pack_forget()
        show_toolbar = False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=TOP, fill=X)
        text_editor.pack(fill=BOTH, expand=True)
        status_bar.pack(side=BOTTOM)
        show_toolbar = True

def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar = False
    else:
        status_bar.pack(side= BOTTOM)
        show_statusbar = True

view.add_checkbutton(label='Tool Bar', onvalue=True, offvalue=False, variable=show_toolbar,image=toolbar_icon, compound=LEFT, command=hide_toolbar)
view.add_checkbutton(label='Status Bar', onvalue=True, offvalue=False, variable=show_statusbar,image=statusbar_icon, compound=LEFT, command=hide_statusbar)

# color theme commmands
def change_theme():
    chosen_theme = theme_choice.get()
    color_tuple = color_dict.get(chosen_theme)
    fg_color, bg_color = color_tuple[0], color_tuple[1]
    text_editor.config(background=bg_color, foreground=fg_color)

count = 0
for i in color_dict:
    colortheme.add_radiobutton(label=i, image=color_icons[count], variable=theme_choice, compound=LEFT, command=change_theme)
    count += 1
############################# end main menu functionality#############################

root.config(menu=main_menu)

## shortcut keys
root.bind('<Control-n>', new_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-s>', save_file)
root.bind("<Control-Alt-s>", save_as_file)
root.bind('<Control-q>', exit_func)
root.bind('<Control-f>', find_func)
root.mainloop()