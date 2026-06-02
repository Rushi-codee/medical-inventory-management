import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import os
import csv

# Modern Color Palette Constants
BG_DARK = "#0F172A"       # Deep Slate (Main dashboard background)
BG_CARD = "#1E293B"       # Slate 800 (Sidebar, panels, cards)
BG_INPUT = "#334155"      # Slate 700 (Input field background)
FG_LIGHT = "#F8FAFC"      # Slate 50 (Primary high-contrast text)
FG_MUTED = "#94A3B8"      # Slate 400 (Secondary descriptive text)

# Accent Colors
ACCENT_TEAL = "#0D9488"   # Teal 600 (Primary system color, focus state)
ACCENT_TEAL_HOVER = "#0F766E" # Teal 700

ACCENT_GREEN = "#10B981"  # Emerald 500 (Success, Add actions)
ACCENT_GREEN_HOVER = "#059669" # Emerald 600

ACCENT_RED = "#EF4444"    # Red 500 (Danger, Delete, Exit actions)
ACCENT_RED_HOVER = "#DC2626"   # Red 600

ACCENT_AMBER = "#F59E0B"  # Amber 500 (Warnings, Updates)
ACCENT_AMBER_HOVER = "#D97706" # Amber 600

ACCENT_BLUE = "#3B82F6"   # Blue 500 (Info, Reports, Queries)
ACCENT_BLUE_HOVER = "#2563EB"  # Blue 600

# Console Area
CONSOLE_BG = "#090D16"    # Terminal black
CONSOLE_FG = "#38BDF8"    # Sky Blue output

FONT_FAMILY = "Segoe UI"
FONT_MONO = "Consolas"

class LoginGUI:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login - Medical Inventory Management")
        self.root.geometry("450x420")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        # Center the login window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 420) // 2
        self.root.geometry(f"450x420+{x}+{y}")

        # Top Header Area
        header_frame = tk.Frame(self.root, bg=BG_DARK)
        header_frame.pack(pady=25)

        header_label = tk.Label(header_frame, text="ADMIN LOGIN",
                               font=(FONT_FAMILY, 20, 'bold'), fg=ACCENT_TEAL, bg=BG_DARK)
        header_label.pack()

        sub_label = tk.Label(header_frame, text="Medical Inventory Management System",
                             font=(FONT_FAMILY, 10), fg=FG_MUTED, bg=BG_DARK)
        sub_label.pack(pady=5)

        # Content Card
        card_frame = tk.Frame(self.root, bg=BG_CARD, padx=30, pady=30)
        card_frame.pack(padx=40, fill='both', expand=True)

        # Username Field
        tk.Label(card_frame, text="USERNAME", font=(FONT_FAMILY, 9, 'bold'), fg=FG_MUTED, bg=BG_CARD, anchor='w').pack(fill='x', pady=(0, 4))
        self.username_entry = tk.Entry(card_frame, font=(FONT_FAMILY, 11), bg=BG_INPUT, fg=FG_LIGHT,
                                       insertbackground=FG_LIGHT, bd=0, relief="flat",
                                       highlightthickness=1, highlightbackground="#475569", highlightcolor=ACCENT_TEAL)
        self.username_entry.pack(fill='x', ipady=6, pady=(0, 15))
        self.username_entry.focus()

        # Password Field
        tk.Label(card_frame, text="PASSWORD", font=(FONT_FAMILY, 9, 'bold'), fg=FG_MUTED, bg=BG_CARD, anchor='w').pack(fill='x', pady=(0, 4))
        self.password_entry = tk.Entry(card_frame, show="*", font=(FONT_FAMILY, 11), bg=BG_INPUT, fg=FG_LIGHT,
                                       insertbackground=FG_LIGHT, bd=0, relief="flat",
                                       highlightthickness=1, highlightbackground="#475569", highlightcolor=ACCENT_TEAL)
        self.password_entry.pack(fill='x', ipady=6, pady=(0, 20))

        # Action Button
        login_btn = tk.Button(card_frame, text="Log In to System", command=self.authenticate,
                              bg=ACCENT_TEAL, fg=FG_LIGHT, activebackground=ACCENT_TEAL_HOVER, activeforeground=FG_LIGHT,
                              font=(FONT_FAMILY, 11, 'bold'), relief='flat', bd=0, cursor='hand2')
        login_btn.pack(fill='x', ipady=8)
        
        # Hover binding
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg=ACCENT_TEAL_HOVER))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg=ACCENT_TEAL))

        # Enter key triggers authentication for desktop convenience
        self.username_entry.bind("<Return>", lambda e: self.authenticate())
        self.password_entry.bind("<Return>", lambda e: self.authenticate())

        # Status message label
        self.status_label = tk.Label(self.root, text="", bg=BG_DARK, fg="#EF4444", font=(FONT_FAMILY, 10))
        self.status_label.pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.status_label.config(text="Please enter both username and password")
            return

        try:
            exe_path = os.path.join(os.path.dirname(__file__), '..', 'MedicalInventory.exe')
            result = subprocess.run([exe_path, "authenticate", username, password],
                                   capture_output=True, text=True, cwd=os.path.dirname(exe_path))

            if result.returncode == 0 and "Authentication successful" in result.stdout:
                self.root.destroy()
                self.on_login_success()
            else:
                self.status_label.config(text="Invalid username or password")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")


class MedicalInventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Inventory Management System")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=BG_DARK)

        # Style standard scrollbar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Vertical.TScrollbar", gripcount=0,
                        background="#334155", darkcolor="#1E293B", lightcolor="#1E293B",
                        troughcolor="#0F172A", bordercolor="#0F172A")

        # Layout Setup
        # 1. Left Sidebar
        sidebar = tk.Frame(self.root, bg=BG_CARD, width=300)
        sidebar.pack(side=tk.LEFT, fill='y')
        sidebar.pack_propagate(False)

        # Sidebar Brand Logo/Header
        brand_frame = tk.Frame(sidebar, bg=BG_CARD, pady=20)
        brand_frame.pack(fill='x')
        
        brand_title = tk.Label(brand_frame, text="MIMS CONSOLE", font=(FONT_FAMILY, 16, 'bold'), fg=ACCENT_TEAL, bg=BG_CARD)
        brand_title.pack()
        
        brand_sub = tk.Label(brand_frame, text="v1.0.0 Stable", font=(FONT_FAMILY, 8, 'italic'), fg=FG_MUTED, bg=BG_CARD)
        brand_sub.pack()

        brand_divider = tk.Frame(sidebar, height=1, bg="#334155")
        brand_divider.pack(fill='x', padx=15, pady=5)

        # 2. Right Main Panel
        right_panel = tk.Frame(self.root, bg=BG_DARK)
        right_panel.pack(side=tk.RIGHT, fill='both', expand=True)

        # Top Header Bar in Right Panel
        header_frame = tk.Frame(right_panel, bg=BG_CARD, padx=25, pady=15)
        header_frame.pack(fill='x')

        header_title = tk.Label(header_frame, text="Medical Inventory Management System",
                                font=(FONT_FAMILY, 20, 'bold'), fg=FG_LIGHT, bg=BG_CARD, anchor='w')
        header_title.pack(side=tk.LEFT)

        header_sub = tk.Label(header_frame, text="• Dashboard Console",
                              font=(FONT_FAMILY, 11), fg=ACCENT_TEAL, bg=BG_CARD, anchor='w')
        header_sub.pack(side=tk.LEFT, padx=10, pady=(5, 0))

        # Bottom header colored bar accent
        header_line = tk.Frame(right_panel, height=2, bg=ACCENT_TEAL)
        header_line.pack(fill='x')

        # Form Card Container for input fields
        form_card = tk.Frame(right_panel, bg=BG_CARD, padx=20, pady=15)
        form_card.pack(fill='x', padx=25, pady=(20, 10))

        form_title = tk.Label(form_card, text="MEDICINE DETAIL FORM", font=(FONT_FAMILY, 11, 'bold'), fg=FG_LIGHT, bg=BG_CARD, anchor='w')
        form_title.pack(anchor='w', pady=(0, 10))

        # Fields Grid Layout inside Form Card
        grid_frame = tk.Frame(form_card, bg=BG_CARD)
        grid_frame.pack(fill='x')
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        self.name_entry = self.create_grid_entry(grid_frame, "MEDICINE NAME", 0, 0)
        self.batch_entry = self.create_grid_entry(grid_frame, "BATCH ID", 0, 1)
        self.expiry_entry = self.create_grid_entry(grid_frame, "EXPIRY DATE (YYYY-MM-DD)", 1, 0)
        self.quantity_entry = self.create_grid_entry(grid_frame, "STOCK QUANTITY", 1, 1)
        self.price_entry = self.create_grid_entry(grid_frame, "UNIT PRICE ($)", 2, 0)
        self.threshold_entry = self.create_grid_entry(grid_frame, "LOW STOCK THRESHOLD", 2, 1)
        self.delta_entry = self.create_grid_entry(grid_frame, "QUANTITY DELTA (+/-)", 3, 0)

        # Informative helper tip in the grid
        tip_frame = tk.Frame(grid_frame, bg=BG_CARD)
        tip_frame.grid(row=3, column=1, padx=10, pady=8, sticky='ew')
        tip_label = tk.Label(tip_frame, text="* Hint: For searches, only the Name field is required.",
                             fg=FG_MUTED, bg=BG_CARD, font=(FONT_FAMILY, 9, 'italic'), anchor='w')
        tip_label.pack(fill='x', pady=(15, 0))

        # 3. Console Output Screen (Bottom half of Right Panel)
        console_card = tk.Frame(right_panel, bg=BG_CARD, padx=20, pady=15)
        console_card.pack(fill='both', expand=True, padx=25, pady=(10, 20))

        console_title = tk.Label(console_card, text="SYSTEM TERMINAL LOG", font=(FONT_FAMILY, 11, 'bold'), fg=FG_LIGHT, bg=BG_CARD, anchor='w')
        console_title.pack(anchor='w', pady=(0, 10))

        scroll_frame = tk.Frame(console_card, bg=BG_CARD)
        scroll_frame.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(scroll_frame, yscrollcommand=scrollbar.set,
                                   bg=CONSOLE_BG, fg=CONSOLE_FG, insertbackground=CONSOLE_FG,
                                   font=(FONT_MONO, 11), relief='flat', bd=0)
        self.output_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=self.output_text.yview)

        # Sidebar Buttons System
        # Group 1: Database operations
        tk.Label(sidebar, text="DATABASE ACTIONS", font=(FONT_FAMILY, 8, 'bold'), fg=FG_MUTED, bg=BG_CARD, anchor='w').pack(fill='x', padx=15, pady=(15, 5))
        self.create_sidebar_button(sidebar, "Add New Medicine", self.add_medicine, ACCENT_GREEN, ACCENT_GREEN_HOVER)
        self.create_sidebar_button(sidebar, "Update Quantity", self.update_quantity, ACCENT_AMBER, ACCENT_AMBER_HOVER)
        self.create_sidebar_button(sidebar, "Update Expiry Date", self.update_expiry, ACCENT_AMBER, ACCENT_AMBER_HOVER)
        self.create_sidebar_button(sidebar, "Delete Medicine", self.delete_medicine, ACCENT_RED, ACCENT_RED_HOVER)
        self.create_sidebar_button(sidebar, "Clear Expired Stock", self.remove_expired, ACCENT_RED, ACCENT_RED_HOVER)

        # Group 2: Queries & Filters
        tk.Label(sidebar, text="INVENTORY QUERIES", font=(FONT_FAMILY, 8, 'bold'), fg=FG_MUTED, bg=BG_CARD, anchor='w').pack(fill='x', padx=15, pady=(15, 5))
        self.create_sidebar_button(sidebar, "Display All Medicines", self.display_all, ACCENT_TEAL, ACCENT_TEAL_HOVER)
        self.create_sidebar_button(sidebar, "Search Medicine File", self.search_medicine, ACCENT_TEAL, ACCENT_TEAL_HOVER)
        self.create_sidebar_button(sidebar, "Show Expired Inventory", self.show_expired, ACCENT_BLUE, ACCENT_BLUE_HOVER)
        self.create_sidebar_button(sidebar, "Show Low Stock Items", self.show_low_stock, ACCENT_BLUE, ACCENT_BLUE_HOVER)

        # Group 3: Reporting & System Control
        tk.Label(sidebar, text="REPORTS & SYSTEM", font=(FONT_FAMILY, 8, 'bold'), fg=FG_MUTED, bg=BG_CARD, anchor='w').pack(fill='x', padx=15, pady=(15, 5))
        self.create_sidebar_button(sidebar, "Generate Expired Report", self.generate_expired_report, ACCENT_BLUE, ACCENT_BLUE_HOVER)
        self.create_sidebar_button(sidebar, "Generate Low Stock Report", self.generate_low_stock_report, ACCENT_BLUE, ACCENT_BLUE_HOVER)
        
        # Spacer & System Control
        tk.Label(sidebar, text="", bg=BG_CARD).pack(fill='y', expand=True) # Fills middle space pushing Exit button to bottom
        self.create_sidebar_button(sidebar, "Exit Application", self.exit_app, ACCENT_RED, ACCENT_RED_HOVER)

        # Global System Status Bar
        self.status_label = tk.Label(root, text="System: Ready", anchor=tk.W, bg=BG_CARD, fg=FG_MUTED, font=(FONT_FAMILY, 9), padx=15, pady=6)
        
        # Border divider above status bar
        status_divider = tk.Frame(root, height=1, bg="#334155")
        status_divider.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Hotkeys: Escape exits full-screen mode
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))

    def create_grid_entry(self, parent, label_text, row, col):
        # Styled cell frame containing label on top of modern flat input field
        cell = tk.Frame(parent, bg=BG_CARD)
        cell.grid(row=row, column=col, padx=10, pady=8, sticky='ew')
        
        label = tk.Label(cell, text=label_text, fg=FG_MUTED, bg=BG_CARD, font=(FONT_FAMILY, 8, 'bold'), anchor='w')
        label.pack(fill='x', pady=(0, 2))
        
        entry = tk.Entry(cell, font=(FONT_FAMILY, 11), bg=BG_INPUT, fg=FG_LIGHT,
                         insertbackground=FG_LIGHT, bd=0, relief="flat",
                         highlightthickness=1, highlightbackground="#475569", highlightcolor=ACCENT_TEAL)
        entry.pack(fill='x', ipady=5)
        return entry

    def create_sidebar_button(self, parent, text, command, base_color, hover_color):
        # Modern flat sidebar buttons with custom colors and cursor hover indicators
        button = tk.Button(parent, text=text, command=command, bg=base_color, fg=FG_LIGHT,
                           activebackground=hover_color, activeforeground=FG_LIGHT,
                           font=(FONT_FAMILY, 9, 'bold'), relief='flat', bd=0, cursor='hand2')
        button.pack(fill='x', padx=15, pady=4, ipady=6)
        
        # Register mouse hover transitions
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=base_color))
        return button

    def update_status(self, message):
        self.status_label.config(text=f"System: {message}")
        self.root.update_idletasks()

    def check_threshold_alert(self, name, batch):
        try:
            csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory.csv')
            if os.path.exists(csv_path):
                with open(csv_path, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 6 and row[0] == name and row[1] == batch:
                            qty = int(row[3])
                            threshold = int(row[5])
                            if qty <= threshold:
                                messagebox.showwarning("Threshold Alert", f"Threshold reached for {name} (Batch: {batch}). Please order the medicine.")
                            break
        except Exception as e:
            pass

    def check_threshold_alert_for_name(self, name):
        try:
            csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory.csv')
            if os.path.exists(csv_path):
                with open(csv_path, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 6 and row[0] == name:
                            qty = int(row[3])
                            threshold = int(row[5])
                            batch = row[1]
                            if qty <= threshold:
                                messagebox.showwarning("Threshold Alert", f"Threshold reached for {name} (Batch: {batch}). Please order the medicine.")
        except Exception as e:
            pass

    def check_threshold_alert_for_all(self):
        try:
            csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory.csv')
            if os.path.exists(csv_path):
                with open(csv_path, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 6:
                            name = row[0]
                            batch = row[1]
                            qty = int(row[3])
                            threshold = int(row[5])
                            if qty <= threshold:
                                messagebox.showwarning("Threshold Alert", f"Threshold reached for {name} (Batch: {batch}). Please order the medicine.")
        except Exception as e:
            pass

    def run_command(self, args):
        self.update_status("Processing Command...")
        try:
            exe_path = os.path.join(os.path.dirname(__file__), '..', 'MedicalInventory.exe')
            result = subprocess.run([exe_path] + args, capture_output=True, text=True, cwd=os.path.dirname(exe_path))
            if result.returncode == 0:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, result.stdout)
                self.update_status("Ready")
                return True
            else:
                messagebox.showerror("Error", result.stderr)
                self.update_status("Error occurred")
                return False
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status("Error occurred")
            return False

    def add_medicine(self):
        name = self.name_entry.get()
        batch = self.batch_entry.get()
        expiry = self.expiry_entry.get()
        qty = self.quantity_entry.get()
        price = self.price_entry.get()
        threshold = self.threshold_entry.get()
        if not all([name, batch, expiry, qty, price, threshold]):
            messagebox.showerror("Error", "All fields are required for adding medicine.")
            return
        try:
            qty = int(qty)
            price = float(price)
            threshold = int(threshold)
        except ValueError:
            messagebox.showerror("Error", "Invalid number format.")
            return
        self.run_command(["add", name, batch, expiry, str(qty), str(price), str(threshold)])
        self.check_threshold_alert(name, batch)
        self.name_entry.delete(0, tk.END)
        self.batch_entry.delete(0, tk.END)
        self.expiry_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.threshold_entry.delete(0, tk.END)

    def update_quantity(self):
        name = self.name_entry.get()
        batch = self.batch_entry.get()
        delta = self.delta_entry.get()
        if not all([name, batch, delta]):
            messagebox.showerror("Error", "Name, Batch, and Delta are required.")
            return
        try:
            delta = int(delta)
        except ValueError:
            messagebox.showerror("Error", "Delta must be an integer.")
            return
        if self.run_command(["update_qty", name, batch, str(delta)]):
            self.check_threshold_alert(name, batch)
            self.name_entry.delete(0, tk.END)
            self.batch_entry.delete(0, tk.END)
            self.delta_entry.delete(0, tk.END)

    def update_expiry(self):
        name = self.name_entry.get()
        batch = self.batch_entry.get()
        expiry = self.expiry_entry.get()
        if not all([name, batch, expiry]):
            messagebox.showerror("Error", "Name, Batch, and Expiry are required.")
            return
        self.run_command(["update_expiry", name, batch, expiry])

    def remove_expired(self):
        self.run_command(["remove_expired"])

    def display_all(self):
        self.run_command(["display_all"])
        self.check_threshold_alert_for_all()

    def show_expired(self):
        self.run_command(["show_expired"])

    def show_low_stock(self):
        self.run_command(["show_low_stock"])

    def delete_medicine(self):
        name = self.name_entry.get()
        batch = self.batch_entry.get()
        if not all([name, batch]):
            messagebox.showerror("Error", "Name and Batch are required.")
            return
        if self.run_command(["delete_medicine", name, batch]):
            self.name_entry.delete(0, tk.END)
            self.batch_entry.delete(0, tk.END)

    def search_medicine(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required for search.")
            return
        self.run_command(["search", name])
        self.check_threshold_alert_for_name(name)

    def generate_expired_report(self):
        self.run_command(["generate_expired_report"])

    def generate_low_stock_report(self):
        self.run_command(["generate_low_stock_report"])

    def exit_app(self):
        self.root.quit()
        self.root.destroy()

def launch_dashboard():
    dashboard_root = tk.Tk()
    MedicalInventoryGUI(dashboard_root)
    dashboard_root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    LoginGUI(login_root, launch_dashboard)
    login_root.mainloop()
