'''
Created on Aug 14, 2016

@author: Hanna
'''

import ow_stats_gui
import ow_database
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    ow_stats_gui.ow_stats_gui(root).pack(side="top", fill="both", expand=True)
    root.mainloop() 