import langid
import pandas
import customtkinter
BACKGROUND_COLOR = "whitesmoke"
import random
from tkinter import Canvas,PhotoImage
import pandas as pd
import tkinter.font
from gtts import gTTS
from playsound import playsound
from PyDictionary import PyDictionary
import os
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
import threading
from plyer import notification
import plot



#------------------------ Generating a french word ----------
class ToplevelselfFlip(customtkinter.CTkToplevel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Cards')
        self.word_count=0
        self.geometry("500x400")
        self.to_learn = {}
        self.current_card = {}
        with open("./test/txt.txt", "r") as file:
            csvfile = file.read().replace(' ', '')
        
        try: 
            data = pandas.read_csv(csvfile)
        except FileNotFoundError:
            original_data = pandas.read_csv(csvfile)
            print(original_data)
            self.to_learn = original_data.to_dict(orient="records")
        else:
            self.to_learn = data.to_dict(orient="records")
        
        
        self.configure(padx=50, pady=50, fg_color=BACKGROUND_COLOR)   
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)   
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.flip_timer = self.after(10000, func=self.flip_card) 
        
        self.canvas = Canvas(self,width=500, height=360)
        self.card_front_img = PhotoImage(file="./images/paper12.png")
        self.image = PhotoImage(file="./images/speaker.png")
        self.card_background = self.canvas.create_image(300, 150, image=self.card_front_img)
        
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
        
        
        self.card_word = self.canvas.create_text(280, 107, text="Word", font= ("Times",40), tags="word")
        self.img = self.canvas.create_image(500, 140, anchor='w', image=self.image)
        self.card_explanation = self.canvas.create_text(10, 175, text="", font= ("Times",13,"italic"), tags="word", width=600,anchor='nw')
        self.card_synonyms = self.canvas.create_text(10, 230, text="", font= ("Times",13,"italic"), tags="word", width=600,anchor='nw')
        
        cross_image = PhotoImage(file="./images/question.png")
        self.unknown_button = customtkinter.CTkButton(master=self,image=cross_image,text="I didn't know this word",
                                                      fg_color='#FFE5E4',
                                                      text_color='#FF4136',
                                                      hover_color='#DC143C',
                                                      width=600,
                                                      height=50,
                                                      command =self.flip_card)
        
        
        check_image = PhotoImage(file="./images/checkmark.png")
        self.known_button = customtkinter.CTkButton(master=self,image=check_image,text="I know this word",
                                                    fg_color='#C7EA46',
                                                    hover_color='#228B22',
                                                    text_color='#008000',
                                                    width=600,
                                                    height=50,
                                                    command=self.is_known)
        self.canvas.grid(row=0, column=1, columnspan=2,rowspan=2,sticky='nsew')
        self.known_button.grid(row=2, column=1,sticky="nsew")
        self.unknown_button.grid(row=3, column=1,sticky="nsew")
        
        self.next_card()
        self.mainloop()
    
    def next_card(self):

        self.after_cancel(self.flip_timer)
        self.current_card = random.choice(self.to_learn)
        self.canvas.itemconfig(self.card_word, text=self.current_card["column0"].capitalize(), fill="navy")
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.current_word = self.current_card["column0"]
        self.current_lan,score = langid.classify(self.current_card["column0"])
        self.canvas.tag_bind(self.img, '<Button-1>',self.on_image_click )
        self.canvas.itemconfig(self.card_explanation, text="", fill = "black")
        self.canvas.itemconfig(self.card_synonyms, text="", fill = "black")
        self.flip_timer = self.after(10000, func=self.flip_card)
    def get_part_of_speech(self,tag):
        if tag.startswith('n'):
            return 'noun'
        elif tag.startswith('v'):
            return 'verb'
        elif tag.startswith('a'):
            return 'adjective'
        elif tag.startswith('r'):
            return 'adverb'
        else:
            return 'Unknown'
    def output(self,word):
        output = ""
        synsets = wordnet.synsets(word)
        try:
            pos_tag = synsets[0].pos()
            pos_name = self.get_part_of_speech(pos_tag)
            if synsets:
                pos = synsets[0].pos()
                meaning = synsets[0].definition()
                output +=  f"{pos_name}: {meaning} \n"
            else:
                output += f"No definition found for {word}.\n"
        
        
            synonyms = []
            max_synonyms = 3
            for syn in synsets:
                for lemma in syn.lemmas():
                    if lemma.name() != word:
                        synonyms.append(lemma.name())
                        if len(synonyms) >= max_synonyms:
                            break
                if len(synonyms) >= max_synonyms:
                    break
        
            if synonyms:
                output += f"synonyms of {word}: "
                for synonym in synonyms:
                    output +=  synonym +"  "
            else:
                output += f"No synonyms found for {word}.\n"
        except IndexError:
            output = ""
        return output
    def flip_card(self):
        self.remindedword = self.current_card["column0"]
        t = threading.Timer(3, self.show_notification)
        t.start()
        string = self.output(self.current_card["column1"]).split("\n")
        self.current_word = self.current_card["column1"]
        self.current_lan,score = langid.classify(self.current_card["column1"])
        self.canvas.tag_bind(self.img, '<Button-1>',self.on_image_click )
        self.canvas.itemconfig(self.card_word, text=self.current_card["column1"].capitalize(), fill = "navy")
        self.canvas.itemconfig(self.card_explanation, text=string[0], fill = "black")
        self.canvas.itemconfig(self.card_synonyms, text=string[1], fill = "black")
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        
    def on_image_click(self,event):
        print("Image clicked at ({}, {})".format(event.x, event.y))  
        self.audio_py()
    def show_notification(self):
        title = "Reminder"
        message = "Do you still remember the word: "+ self.remindedword
        notification.notify(title=title, message=message)
    def is_known(self):
        plot.saveprogress(1)
        self.remindedword = self.current_card["column0"]
        t = threading.Timer(60*60*24*30, self.show_notification)
        t.start()
        self.to_learn.remove(self.current_card)
        
        """data = pd.DataFrame(self.to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)"""

        self.next_card()
    def audio_py(self):
       speak = gTTS(text=self.current_word , lang=self.current_lan , slow=False)
         
       speak.save("./sound/captured_voice.mp3")

       playsound('./sound/captured_voice.mp3')
       os.remove('./sound/captured_voice.mp3')
       
if __name__ == "__main__":
    app = ToplevelselfFlip()
    app.mainloop()  
