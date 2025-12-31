import customtkinter as ctk
from tkinter import filedialog, messagebox
from db import init_db
from models import *
from ai_logic import diagnose_disease
from ui.add_plant_popup import open_add_plant_popup
from ui.widgets import load_image
from CTkMessagebox import CTkMessagebox

init_db()

ctk.set_appearance_mode("light")

COLOURS = {
    "bg_main": "#ffffff",        # main background
    "bg_sidebar": "#DBDBDB",     # sidebar and logs background
    "text_primary": "#000000",   # dark text
    "accent": "#75b538",         # apple green
    "accent_hover": "#467B16",   # darker green hover
    "accent_text": "#EFEFEF",    # text on buttons
    "border_hover": "#878787",   # border on hover
    "danger": "#e74c3c",         # delete red
    "danger_hover": "#c0392b",   # delete hover red
}

class GardenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Garden")
        self.root.iconbitmap("icon.ico")
        self.root.geometry("850x550")
        self.selected_plant_id = None

        self.font_main = ctk.CTkFont(family="SF Pro Display", size=13)
        self.font_bold = ctk.CTkFont(family="SF Pro Display", size=13, weight="bold")
        self.font_header = ctk.CTkFont(family="SF Pro Display", size=20, weight="bold")

        self.sidebar = ctk.CTkFrame(root, width=220, fg_color=COLOURS["bg_sidebar"])
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="MY PLANTS:",
            font=self.font_bold,
            text_color=COLOURS["text_primary"],
        ).pack(pady=(10, 0))

        self.plant_frame = ctk.CTkScrollableFrame(
            self.sidebar, fg_color=COLOURS["bg_sidebar"]
        )
        self.plant_frame.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Add new",
            fg_color=COLOURS["accent"],
            hover_color=COLOURS["accent_hover"],
            text_color=COLOURS["accent_text"],
            command=lambda: open_add_plant_popup(self.root, self.refresh_sidebar),
        ).pack(side="bottom", pady=10)

        self.main = ctk.CTkFrame(root, fg_color=COLOURS["bg_main"])
        self.main.pack(side="right", expand=True, fill="both")

        self.display_area = ctk.CTkFrame(self.main, fg_color="white")
        self.display_area.pack(expand=True, fill="both")

        self.refresh_sidebar()

        if not get_all_plants():
            open_add_plant_popup(self.root, self.refresh_sidebar)

    def refresh_sidebar(self):
        for widget in self.plant_frame.winfo_children():
            widget.destroy()

        self.plants = get_all_plants()
        for idx, (plant_id, name, species, img) in enumerate(self.plants, 1):
            row = ctk.CTkFrame(self.plant_frame, fg_color=COLOURS["bg_sidebar"])
            row.pack(fill="x", pady=2, padx=2)

            btn = ctk.CTkButton(
                row,
                text=f"{idx}. {name}",
                fg_color="white",
                text_color=COLOURS["text_primary"],
                hover_color=COLOURS["border_hover"],
                anchor="w",
                command=lambda pid=plant_id: self.select_plant(pid),
            )
            btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

            del_btn = ctk.CTkButton(
                row,
                text="✕",
                width=25,
                fg_color=COLOURS["danger"],
                hover_color=COLOURS["danger_hover"],
                text_color="white",
                command=lambda pid=plant_id: self.delete_plant(pid),
            )
            del_btn.pack(side="right")

    def select_plant(self, plant_id):
        self.selected_plant_id = plant_id
        plant = [p for p in get_all_plants() if p[0] == plant_id][0]
        self.display_plant_page(plant)

    def delete_plant(self, plant_id):
        msg = CTkMessagebox(
            title="Confirm Deletion", 
            message="Are you sure you want to delete this plant and all its logs?",
            icon="warning", 
            option_1="Cancel", 
            option_2="Delete",
            button_color=COLOURS["danger"],
            button_hover_color=COLOURS["danger_hover"]
        )
        
        if msg.get() == "Delete":
            delete_plant(plant_id)
            self.refresh_sidebar()
            for w in self.display_area.winfo_children():
                w.destroy()

    def display_plant_page(self, plant):
        for w in self.display_area.winfo_children():
            w.destroy()

        plant_id, name, species, image_path = plant

        ctk.CTkLabel(
            self.display_area, text=name, font=self.font_header
        ).pack(pady=(20, 0))
        ctk.CTkLabel(
            self.display_area,
            text=species or "Unknown species",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray",
        ).pack()

        img = load_image(image_path, size=(250, 250))
        lbl = ctk.CTkLabel(self.display_area, image=img, text="")
        lbl.image = img
        lbl.pack(pady=5)

        ctk.CTkButton(
            self.display_area,
            text="Upload image",
            fg_color=COLOURS["accent"],
            hover_color=COLOURS["accent_hover"],
            text_color=COLOURS["accent_text"],
            command=self.upload_new_image,
        ).pack(pady=5)

        ctk.CTkLabel(
            self.display_area,
            text="DIGITAL GARDEN LOG:",
            font=self.font_bold,
        ).pack(pady=5)

        log_scroll = ctk.CTkScrollableFrame(self.display_area, fg_color="white", width=500, height=200)
        log_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        logs = get_logs(plant_id)

        if not logs:
            ctk.CTkLabel(
                log_scroll,
                text="No logs yet. Upload a plant image to generate one!",
                text_color="gray",
                font=ctk.CTkFont(size=12, slant="italic"),
            ).pack(pady=10)
            return

        # display only the 10 most recent logs
        latest_logs = logs[-10:]
        for ts, disease, cause, solution in latest_logs:
            frame = ctk.CTkFrame(log_scroll, corner_radius=6, border_width=0, fg_color=COLOURS["bg_sidebar"])
            frame.pack(fill="x", padx=5, pady=4)
            
            header = ctk.CTkFrame(frame, fg_color="transparent")
            header.pack(fill="x", padx=10, pady=(6,2))
            header.columnconfigure(0, weight=1) #HMM

            ctk.CTkLabel(header, text=f"{ts} | {disease}", font=self.font_bold).pack(side="left")
            
            ctk.CTkButton(
                header, text="✕", width=24, height=24,
                fg_color=COLOURS["danger"], hover_color=COLOURS["danger_hover"],
                command=lambda t=ts: self.remove_log(t)
            ).pack(side="right")

            ctk.CTkLabel(frame, text=f"Diagnosis: {cause}", wraplength=500, justify="left").pack(anchor="w", padx=10)
            ctk.CTkLabel(frame, text=f"Next steps: {solution}", wraplength=500, justify="left").pack(anchor="w", padx=10, pady=(2, 10))

    def upload_new_image(self):
        if not self.selected_plant_id:
            return
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if not path:
            return

        update_latest_image(self.selected_plant_id, path)

        plant = [p for p in get_all_plants() if p[0] == self.selected_plant_id][0]
        _, name, species, _ = plant

        diagnosis = diagnose_disease(path, species)
        add_log(self.selected_plant_id, diagnosis["disease"], diagnosis["cause"], diagnosis["solution"])

        messagebox.showinfo("Diagnosis complete", f"{name} diagnosed with: {diagnosis['disease']}")
        self.select_plant(self.selected_plant_id)

    def remove_log(self, timestamp):
        msg = CTkMessagebox(
            title="Delete Log?", 
            message="Are you sure you want to delete this log entry? This cannot be undone.",
            icon="warning", 
            option_1="No", 
            option_2="Delete",
            justify="center",
            button_color=COLOURS["danger"],
            button_hover_color=COLOURS["danger_hover"]
        )
        
        if msg.get() == "Delete":
            delete_log(timestamp)
            self.select_plant(self.selected_plant_id)

if __name__ == "__main__":
    root = ctk.CTk()
    app = GardenApp(root)
    root.mainloop()
