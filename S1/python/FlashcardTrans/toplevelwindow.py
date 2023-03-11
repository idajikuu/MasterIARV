import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import PhotoImage,Text
from tkinter import colorchooser
import audio

customtkinter.set_appearance_mode("Light") 
customtkinter.set_default_color_theme("blue") # Modes: "System" (standard), "Dark", "Light"
 # Themes: "blue" (standard), "green", "dark-blue"
fg_value="slategrey"
import audio
class ToplevelWindow(customtkinter.CTkToplevel):
    def getText(self):
        text = str(self.textbox.get("0.0", "end-1c").replace("\n",""))
        csv=text.replace(" ","")+".csv"
        txt = text+"-t"+ csv +"-t"+str(self.color[1])+"-t \n"
        with open("./test/test.txt", "a") as file:
            file.write(txt)
    def getAudio(self):
        audio.playSound("give me the name of the flashcard?")
        a = audio.getAudio()
        convert = audio.audioToText(a)
        self.textbox.insert("0.0",convert)
    def choose_color(self):
        self.color = colorchooser.askcolor(title="Choose color")
        if self.color:
            # set the label background to the chosen color
            self.textbox.configure(fg_color=self.color[1])
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Add a Flashcard')
        self.value_changed=False
        self.geometry("300x200")
        self.configure(fg_color=fg_value)
        
        self.textbox = customtkinter.CTkTextbox(self, width=220, height=100)
        self.textbox.insert("0.0", "Flashcard name")
        self.textbox.pack(anchor='nw',padx=10, pady=20)
        self.button_1 = customtkinter.CTkButton(master=self,
                                         image=PhotoImage(file="./images/microw.png"),
                                         border_width=0,
                                         fg_color=fg_value,
                                         corner_radius=100,
                                         width=30,
                                         height=30,
                                         text="",
                                         command=self.getAudio)
         
        self.button_2 = customtkinter.CTkButton(master=self,
                                        image=PhotoImage(file="./images/right1.png"),
                                        border_width=0,
                                        fg_color=fg_value,
                                        corner_radius=100,
                                        width=30,
                                        height=30,
                                        text="",
                                        command=self.getText)
        
        self.button = customtkinter.CTkButton(master=self,
                                              border_width=0,
                                              fg_color=fg_value,
                                              corner_radius=100,
                                              width=30,
                                              height=30,
                                              text="",
                                              image=PhotoImage(file="./images/paint.png"),
                                              command=self.choose_color)
        self.button.pack(side='right', anchor='se',padx=6, pady=5)
        self.button_1.pack(side='right', anchor='se',padx=6, pady=5)
        self.button_2.pack(side='right', anchor='se',padx=6, pady=5)

        
if __name__ == "__main__":
    app = ToplevelWindow()
    app.mainloop()
        
        


