import customtkinter as ctk
from tkinter import filedialog, messagebox
from models import add_plant
from ai_logic import identify_species

def open_add_plant_popup(parent, refresh_callback):
    popup = ctk.CTkToplevel(parent)
    popup.title("Add New Plant")
    popup.geometry("200x170")
    popup.configure(fg_color="#ffffff")
    popup.after(200, lambda: popup.iconbitmap("icon.ico"))
    popup.after(10, popup.focus_force)

    name_entry = ctk.CTkEntry(popup, placeholder_text="Plant Nickname", border_color="#878787")
    name_entry.pack(pady=(30, 5), padx=20)

    img_path = []

    def select_file():
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path: img_path.append(path)

    ctk.CTkButton(popup, text="Select Image", fg_color="#DBDBDB", hover_color="#878787", text_color="#ffffff", command=select_file).pack(pady=(5, 10))
    
    def save():
        if not name_entry.get() or not img_path:
            return messagebox.showerror("Error", "Name and Image required")
        
        species = identify_species(img_path[-1])
        add_plant(name_entry.get(), img_path[-1], species)
        refresh_callback()
        popup.destroy()

    ctk.CTkButton(popup, text="Save Plant", fg_color="#75b538", hover_color="#467B16", text_color="#EFEFEF", command=save).pack(pady=(10, 20))