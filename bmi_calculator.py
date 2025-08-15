import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

DATA_FILE = "bmi_data.csv"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Name", "Date", "Weight", "Height", "BMI"]).to_csv(DATA_FILE, index=False)

def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # cm to meters
        if height <= 0 or weight <= 0:
            raise ValueError("Invalid height or weight")
        
        bmi = round(weight / (height ** 2), 2)
        result_label.config(text=f"Your BMI is {bmi}")
        
        # Categorize BMI
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"
        category_label.config(text=f"Category: {category}")

        # Save to file
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.read_csv(DATA_FILE)
        df.loc[len(df)] = [name, date, weight, height * 100, bmi]
        df.to_csv(DATA_FILE, index=False)

        messagebox.showinfo("Saved", "BMI record saved!")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input.\n{e}")

def view_history():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter your name")
        return
    df = pd.read_csv(DATA_FILE)
    user_data = df[df["Name"].str.lower() == name.lower()]
    if user_data.empty:
        messagebox.showinfo("No Data", "No history found for this user")
    else:
        history_window = tk.Toplevel(root)
        history_window.title(f"{name}'s BMI History")

        tree = ttk.Treeview(history_window, columns=list(user_data.columns), show="headings")
        for col in user_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for _, row in user_data.iterrows():
            tree.insert('', tk.END, values=list(row))
        tree.pack(expand=True, fill='both')

def plot_trend():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter your name")
        return
    df = pd.read_csv(DATA_FILE)
    user_data = df[df["Name"].str.lower() == name.lower()]
    if user_data.empty:
        messagebox.showinfo("No Data", "No trend data available")
    else:
        user_data["Date"] = pd.to_datetime(user_data["Date"])
        user_data = user_data.sort_values("Date")

        plt.figure(figsize=(8, 4))
        plt.plot(user_data["Date"], user_data["BMI"], marker='o', linestyle='-')
        plt.title(f"{name}'s BMI Trend")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# GUI Setup
root = tk.Tk()
root.title("Advanced BMI Calculator")

tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=5, pady=5)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Height (cm):").grid(row=2, column=0, padx=5, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Calculate BMI", command=calculate_bmi).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="View History", command=view_history).grid(row=4, column=0, pady=5)
tk.Button(root, text="Show Trend", command=plot_trend).grid(row=4, column=1, pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.grid(row=5, column=0, columnspan=2)

category_label = tk.Label(root, text="", font=("Arial", 10))
category_label.grid(row=6, column=0, columnspan=2)

root.mainloop()

