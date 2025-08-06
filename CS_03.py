import re
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

class PasswordChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Complexity Checker")
        self.root.geometry("500x400")
        self.root.configure(bg="#121212")
        
        # Custom neon style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#121212')
        self.style.configure('TLabel', background='#121212', foreground='#00ff00', font=('Courier', 12))
        self.style.configure('TButton', background='#121212', foreground='#00ff00', 
                            font=('Courier', 10), borderwidth=1, relief='solid')
        self.style.map('TButton', background=[('active', '#222222')], 
                      foreground=[('active', '#00ffff')])
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Password Strength Analyzer", 
                              font=('Courier', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Password entry
        self.password_var = tk.StringVar()
        self.password_var.trace_add('write', self.check_password)
        
        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(fill='x', pady=10)
        
        ttk.Label(entry_frame, text="Enter Password:").pack(side='left')
        self.password_entry = ttk.Entry(entry_frame, textvariable=self.password_var, 
                                      show="•", font=('Courier', 12), width=30)
        self.password_entry.pack(side='left', padx=10)
        self.password_entry.focus()
        
        # Show/hide button
        self.show_var = tk.IntVar()
        show_check = ttk.Checkbutton(entry_frame, text="Show", variable=self.show_var, 
                                    command=self.toggle_show)
        show_check.pack(side='left')
        
        # Strength meter
        self.strength_var = tk.StringVar(value="Strength: None")
        strength_label = ttk.Label(main_frame, textvariable=self.strength_var, 
                                 font=('Courier', 12, 'bold'))
        strength_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(main_frame, orient='horizontal', 
                                      length=300, mode='determinate')
        self.progress.pack(pady=5)
        
        # Criteria frame
        criteria_frame = ttk.Frame(main_frame)
        criteria_frame.pack(fill='x', pady=10)
        
        self.criteria_vars = {
            "length": tk.BooleanVar(),
            "uppercase": tk.BooleanVar(),
            "lowercase": tk.BooleanVar(),
            "digit": tk.BooleanVar(),
            "special": tk.BooleanVar(),
            "common": tk.BooleanVar(value=True)
        }
        
        ttk.Label(criteria_frame, text="Password Criteria:").pack(anchor='w')
        
        criteria_list = [
            ("At least 8 characters", "length"),
            ("Contains uppercase letters", "uppercase"),
            ("Contains lowercase letters", "lowercase"),
            ("Contains numbers", "digit"),
            ("Contains special characters", "special"),
            ("Not a common password", "common")
        ]
        
        for text, key in criteria_list:
            check = ttk.Checkbutton(criteria_frame, text=text, variable=self.criteria_vars[key], 
                                   state='disabled')
            check.pack(anchor='w')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        copy_btn = ttk.Button(button_frame, text="Copy Password", command=self.copy_password)
        copy_btn.pack(side='left', padx=5)
        
        generate_btn = ttk.Button(button_frame, text="Generate Strong", command=self.generate_password)
        generate_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_password)
        clear_btn.pack(side='left', padx=5)
    
    def toggle_show(self):
        if self.show_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def check_password(self, *args):
        password = self.password_var.get()
        
        if not password:
            self.strength_var.set("Strength: None")
            self.progress['value'] = 0
            for var in self.criteria_vars.values():
                var.set(False)
            return
        
        # Check criteria
        length_ok = len(password) >= 8
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[^A-Za-z0-9]', password))
        not_common = password.lower() not in self.get_common_passwords()
        
        self.criteria_vars["length"].set(length_ok)
        self.criteria_vars["uppercase"].set(has_upper)
        self.criteria_vars["lowercase"].set(has_lower)
        self.criteria_vars["digit"].set(has_digit)
        self.criteria_vars["special"].set(has_special)
        self.criteria_vars["common"].set(not_common)
        
        # Calculate strength score (0-100)
        score = 0
        if length_ok:
            score += 20
            if len(password) >= 12:
                score += 10
        if has_upper: score += 15
        if has_lower: score += 15
        if has_digit: score += 15
        if has_special: score += 15
        if not_common: score += 10
        
        # Cap at 100
        score = min(score, 100)
        
        # Update UI
        self.progress['value'] = score
        
        if score < 40:
            strength = "Weak"
            self.progress.configure(style='red.Horizontal.TProgressbar')
        elif score < 70:
            strength = "Moderate"
            self.progress.configure(style='yellow.Horizontal.TProgressbar')
        elif score < 90:
            strength = "Strong"
            self.progress.configure(style='green.Horizontal.TProgressbar')
        else:
            strength = "Very Strong"
            self.progress.configure(style='blue.Horizontal.TProgressbar')
        
        self.strength_var.set(f"Strength: {strength} ({score}%)")
    
    def get_common_passwords(self):
        # List of common passwords
        return {
            'password', '123456', '12345678', '1234', 'qwerty', '12345', 
            'dragon', 'baseball', 'football', 'letmein', 'monkey', 'abc123',
            'mustang', 'access', 'shadow', 'master', 'michael', 'superman'
        }
    
    def copy_password(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Empty", "No password to copy")
    
    def generate_password(self):
        import random
        import string
        
        length = 12
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(random.choice(chars) for _ in range(length))
        
        self.password_var.set(password)
        self.show_var.set(1)
        self.toggle_show()
    
    def clear_password(self):
        self.password_var.set("")
        self.show_var.set(0)
        self.toggle_show()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Custom progressbar styles
    style = ttk.Style()
    style.configure('red.Horizontal.TProgressbar', troughcolor='#121212', 
                   background='#ff0000', bordercolor='#121212', 
                   darkcolor='#ff0000', lightcolor='#ff0000')
    style.configure('yellow.Horizontal.TProgressbar', troughcolor='#121212', 
                   background='#ffff00', bordercolor='#121212', 
                   darkcolor='#ffff00', lightcolor='#ffff00')
    style.configure('green.Horizontal.TProgressbar', troughcolor='#121212', 
                   background='#00ff00', bordercolor='#121212', 
                   darkcolor='#00ff00', lightcolor='#00ff00')
    style.configure('blue.Horizontal.TProgressbar', troughcolor='#121212', 
                   background='#00ffff', bordercolor='#121212', 
                   darkcolor='#00ffff', lightcolor='#00ffff')
    
    app = PasswordChecker(root)
    root.mainloop()