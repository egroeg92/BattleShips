import Tkinter as tk
from Tkinter import *
import os
root = tk.Tk()
root.wm_title("BattleShip")
embed = tk.Frame(root, width = 600 +30, height = 500) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = LEFT) #packs window to the left
    
global buttonwin
buttonwin = tk.Frame(root, width = 600, height = 500)
buttonwin.pack(side =  TOP)

messageFrame = tk.Frame(buttonwin,width = 200, height = 0)
messageFrame.pack(side = TOP)
scrollbar = Scrollbar(messageFrame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(messageFrame)
listbox.pack(side=TOP,fill = Y)

for i in range(100):
    listbox.insert(END, i)

    # attach listbox to scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)


mainloop()