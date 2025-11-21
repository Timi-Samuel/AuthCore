import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

BASE_URL = 'http://127.0.0.1:5001/users'


class AuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AuthCore Client")
        self.create_main_menu()

    def create_main_menu(self):
        # Clear previous widgets
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="AuthCore Client",
                 font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Sign Up", width=20,
                  command=self.sign_up).pack(pady=5)
        tk.Button(self, text="Login", width=20,
                  command=self.login).pack(pady=5)
        tk.Button(self, text="Forgot Password", width=20,
                  command=self.forgot_password).pack(pady=5)
        tk.Button(self, text="Exit", width=20,
                  command=self.destroy).pack(pady=5)

    def sign_up(self):
        email = simpledialog.askstring("Email", "Enter your email:")
        password = simpledialog.askstring(
            "Password", "Enter your password:", show="*")
        if not email or not password:
            messagebox.showwarning(
                "Input Error", "Email and password required.")
            return

        # Send verification code
        response = requests.post(f"{BASE_URL}/verify_account",
                                 json={"email": email, "password": password})
        if response.status_code == 409:
            messagebox.showinfo("Info", "User already exists.")
            return
        elif response.status_code != 200:
            messagebox.showerror(
                "Error", f"Failed to send verification code: {response.json().get('message')}")
            return

        code = simpledialog.askstring(
            "Verification Code", "Enter the code sent to your email:")
        if not code:
            messagebox.showwarning(
                "Input Error", "Verification code required.")
            return

        # Register user with code
        response = requests.post(
            f"{BASE_URL}/add", json={"email": email, "password": password, "code": code})
        if response.status_code == 201:
            messagebox.showinfo("Success", "Account created successfully.")
        else:
            messagebox.showerror(
                "Error", f"Failed: {response.json().get('message')}")

    def login(self):
        email = simpledialog.askstring("Email", "Enter your email:")
        password = simpledialog.askstring(
            "Password", "Enter your password:", show="*")
        if not email or not password:
            messagebox.showwarning(
                "Input Error", "Email and password required.")
            return

        response = requests.post(f"{BASE_URL}/validate",
                                 json={"email": email, "password": password})
        if response.status_code == 200:
            messagebox.showinfo("Success", "Login successful.")
        else:
            messagebox.showerror(
                "Error", f"Login failed: {response.json().get('message')}")

    def forgot_password(self):
        email = simpledialog.askstring("Email", "Enter your email:")
        if not email:
            messagebox.showwarning("Input Error", "Email required.")
            return

        response = requests.post(
            f"{BASE_URL}/forgot_password/", json={"email": email})
        if response.status_code == 200:
            messagebox.showinfo(
                "Info", "Verification code sent to your email.")
            self.change_password(email)
        else:
            messagebox.showerror(
                "Error", f"Failed: {response.json().get('message')}")

    def change_password(self, email):
        code = simpledialog.askstring(
            "Verification Code", "Enter the code sent to your email:")
        new_password = simpledialog.askstring(
            "New Password", "Enter your new password:", show="*")
        if not code or not new_password:
            messagebox.showwarning(
                "Input Error", "Code and new password required.")
            return

        response = requests.post(f"{BASE_URL}/change_password/",
                                 json={"email": email, "password": new_password, "code": code})
        if response.status_code == 200:
            messagebox.showinfo("Success", "Password updated successfully.")
        else:
            messagebox.showerror(
                "Error", f"Failed: {response.json().get('message')}")


if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()
