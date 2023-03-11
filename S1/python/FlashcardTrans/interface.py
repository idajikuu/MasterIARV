import tkinter as tk
import tkinter.messagebox
import customtkinter
from flip import ToplevelselfFlip 
from toplevelwindow import ToplevelWindow
from tkinter import PhotoImage,Text,colorchooser
from functools import partial
import csv
import os
import pandas as pd
from googletrans import Translator
import plot
translator = Translator()

customtkinter.set_appearance_mode("Light") 
customtkinter.set_default_color_theme("blue") # Modes: "System" (standard), "Dark", "Light"
 # Themes: "blue" (standard), "green", "dark-blue"
fg_value="slategrey"

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Language cards')
        self.win = tk.Tk()
        self.geometry("500x700")
        
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        
        self.tabview = customtkinter.CTkTabview(self, width=470, height=650,
                                                text_color="white",
                                                fg_color=fg_value,
                                                segmented_button_selected_color="slategrey",
                                                segmented_button_unselected_hover_color='steelblue')
        
        self.tabview.add("Testing flashcards")
        
        self.tabview.grid(padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.toplevel_window = None
        self.toplevelwindow = None
        self.image1 = tk.PhotoImage(file="./images/blacktrash.png")
        self.image2 = tk.PhotoImage(file="./images/edit.png")
        self.image3 = tk.PhotoImage(file="./images/blackadd.png")
        
        self.tabview.tab("Testing flashcards").button_1 = customtkinter.CTkButton(master=self.tabview.tab("Testing flashcards"),
                                     border_width=0,
                                     fg_color=fg_value,
                                     corner_radius=100,
                                     width=30,
                                     height=30,
                                     text="",
                                     image=PhotoImage(file="./images/add.png"),
                                     command=self.open_toplevel)
        self.tabview.tab("Testing flashcards").button_2 = customtkinter.CTkButton(master=self.tabview.tab("Testing flashcards"),
                                     border_width=0,
                                     fg_color=fg_value,
                                     corner_radius=100,
                                     width=30,
                                     height=30,
                                     text="",
                                     image=PhotoImage(file="./images/plot.png"),
                                     command=plot.plotprogress)
        self.tabview.tab("Testing flashcards").button_1.place(relx=1.0, rely=1.0, anchor="se")
        self.tabview.tab("Testing flashcards").button_2.place(relx=1.0, rely=1.0, anchor="se",x=-60)
        self.line_num=0
        self.destroy=1
        self.buildCanvas()
        
    def save_value_click(self,event,csvfile):
        with open("./test/txt.txt",'w') as f:
            f.write(str(csvfile))
        self.open_fliptoplevel()
    def open_fliptoplevel(self):
        if self.toplevelwindow is None or not self.toplevelwindow.winfo_exists():
            self.toplevelwindow = ToplevelselfFlip(self)  
        else:
            self.toplevelwindow.focus()
    def open_toplevel(self):
        self.destroy = 0
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.after(10000, self.destroytoplevel_window)
        elif self.toplevel_window.winfo_viewable():
            self.toplevel_window.focus()
               
            
        
    def destroytoplevel_window(self):
        self.toplevel_window.destroy()
        self.destroy=0
        self.buildCanvas()
    def delete_flashcard(self,event,line_delete):
        with open("./test/test.txt", "r") as fr:
            lines = fr.readlines()
            with open("./test/test.txt", "w") as fw:
                for line in lines:
                    if line != line_delete:
                        fw.write(line)
        self.destroy=0
        self.buildCanvas()
                
    def show_menu(self, event,index):
        self.index=index
        self.edit_menu.post(event.x_root, event.y_root)

    def edit_color(self,line_num):
        self.color = colorchooser.askcolor()
        if self.color:
            self.change_value_in_file(self.index, 2,'-t', self.color[1]) 
        self.buildCanvas()
    def edit_name(self,line_num):
        dialog = customtkinter.CTkInputDialog(text="Type the value of your card:", title="Card")
        new_data = dialog.get_input()
        self.change_value_in_file(self.index, 0,'-t', new_data) 
        self.buildCanvas()
        
    def add_card(self,event,flashcardcsv):
        filename = "./data/"+flashcardcsv
        dialog = customtkinter.CTkInputDialog(text="Type the value of your card:", title="Card")
        text_to_translate = dialog.get_input()
        translated_text = translator.translate(text_to_translate, dest='en').text
        if os.path.exists(filename):
            with open(filename, mode='a', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([text_to_translate,translated_text])
                file.close()
        else:
            with open(filename, mode='w', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["column0", "column1"])
                writer.writerow([text_to_translate,translated_text])
                file.close()
        self.buildCanvas()
            
    def change_value_in_file(self,line_num, col_num, separator, new_value):
        with open("./test/test.txt", "r+") as f:
            lines = f.readlines()
            line = lines[line_num]
            columns = line.split(separator)
            columns[col_num] = new_value
            new_line = separator.join(str(v) for v in columns) 
            lines[line_num] = new_line
            f.seek(0)
            f.writelines(lines)
    def destroyCanvas(self):
        self.line_num -= 1
        
        while self.line_num>=0:
            self.CanvasIndex[self.line_num].destroy()
            self.line_num -=1

    def buildCanvas(self):
        if self.destroy==0:
            self.destroyCanvas()
        self.CanvasIndex = [tk.Canvas() for i in range(100)]
        self.i=self.j=0
        self.line_num=0
        with open("./test/test.txt", "r") as file:
            for line in file:
                self.flashcardCanvas(line)
                self.j += 1
                self.line_num += 1
                if self.j%2==0:
                    self.j = 0
                    self.i += 1
        file.close()
    def flashcardCanvas(self,line):
        words = line.strip().split('-t')
        canvas = tk.Canvas(self.tabview.tab("Testing flashcards"), width=220, height=100, bg=words[2])
                
        self.imgadd = canvas.create_image(153,85, image=self.image3)
        self.imgtrash = canvas.create_image(207, 85, image=self.image1)
        self.imgedit = canvas.create_image(180, 85, image=self.image2)
                
        csvfile="./data/"+words[1].replace(" ", "")
        try:
            df = pd.read_csv(csvfile)
            num_cards = len(df)
        except FileNotFoundError:
            num_cards = 0
        fscard = canvas.create_text(5,10, text=words[0], fill='black', font=('Arial', 12),width=180,anchor="nw")
        canvas.create_text(5,95, text=str(num_cards)+" total count", fill='grey', font=('Arial', 6,'bold'),anchor='sw')
        canvas.tag_bind(fscard,"<Button-1>",partial(self.save_value_click,csvfile=csvfile))
        canvas.tag_bind(self.imgtrash, '<Button-1>',partial(self.delete_flashcard,line_delete=line))
        canvas.tag_bind(self.imgadd, '<Button-1>',partial(self.add_card,flashcardcsv=words[1]))
        canvas.tag_bind(self.imgedit, '<Button-1>',partial(self.show_menu,index=self.line_num))
                
        
                
        self.menu_frame = tk.Frame(self.win)
        self.menu_frame.pack(side="left", fill="both", expand=True)
    
        self.edit_menu = tk.Menu(self.menu_frame, tearoff=0)
        self.edit_menu.add_command(label='Edit Color',command=partial(self.edit_color,line_num=line))
        self.edit_menu.add_command(label='Edit Name',command=partial(self.edit_name,line_num=line))
                
    
                
        canvas.config(highlightthickness=0, borderwidth=0)
        canvas.grid(row=self.i,column=self.j,padx=20,pady=20, columnspan=1, rowspan=1)
        self.CanvasIndex[self.line_num] = canvas
        self.destroy=1

        
                
if __name__ == "__main__":
    app = App()
    app.mainloop()
