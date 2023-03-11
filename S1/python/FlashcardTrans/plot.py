import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import csv
import pandas as pd

def change_value_in_file(file_path, line_num, col_num, separator, new_value):
    with open(file_path, "r+") as f:
        lines = f.readlines()
        line = lines[line_num - 1]
        columns = line.split(separator)
        columns[col_num - 1] = new_value
        new_line = separator.join(columns) + "\n"
        lines[line_num - 1] = new_line
        f.seek(0)
        f.writelines(lines)

def saveprogress(word_count):
    now = datetime.now() 
    day_weekday = now.strftime("%d %A")
    word_counts = {}
    filename = "./data/progress.csv"
    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                word_counts[row[0]] = row[1]
                
            if day_weekday in word_counts:
                word_counts[day_weekday] = int(word_count)+int(word_counts[day_weekday])            
    except FileNotFoundError:
        with open(filename, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Day of Week", "Word Count"]) 

    with open(filename,  'w', newline='') as f:
        writer = csv.writer(f)
        for day, count in word_counts.items():
            writer.writerow([day, count])
            

    
    

def plotprogress():
    filename = "./data/progress.csv"
    df = pd.read_csv(filename)
    df['Day of Week'] = pd.to_datetime(df['Day of Week'].apply(lambda x: datetime.strptime(x, "%d %A")))    
    weekday_counts = df.groupby('Day of Week')['Word Count'].mean()

    fig, ax = plt.subplots()
    ax.plot(weekday_counts.index.strftime('%A'), weekday_counts.values)
    ax.set_xlabel('Weekday')
    ax.set_ylabel('Mean Word Count')
    root = tk.Tk()
    root.geometry("500x400")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    tk.mainloop()


 
