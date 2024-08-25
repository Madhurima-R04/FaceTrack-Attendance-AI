import tkinter as tk
from tkinter import messagebox

def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text = text,
        activebackground='black',
        activeforeground='white',
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=20,
        font=("Helvetica bold", 20)
    )
    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    inputtext= tk.Text(window,
                       height=2,
                       width=15,
                       font=("Arial",32))

    return inputtext

def msg_box(title, description):
    messagebox.showinfo(title, description)

def main_window(parent, text, bg, command, fg='white'):
    return tk.Button(parent, text=text, bg=bg, fg=fg, command=command)










