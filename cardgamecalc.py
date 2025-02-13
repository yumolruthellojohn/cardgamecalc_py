import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.stats import hypergeom

def calculate_probability():
    try:
        population_size = int(entry_N.get())
        success_population = int(entry_K.get())
        sample_size = int(entry_n.get())
        success_sample = int(entry_k.get())
        
        if any(x <= 0 for x in [population_size, success_population, sample_size, success_sample]):
            messagebox.showerror("Input Error", "All values must be positive")
            return
        
        if success_population > population_size or sample_size > population_size:
            messagebox.showerror("Input Error", "Cards in opening hand and copies of wanted card must be less than or equal to cards in deck.")
            return
        
        prob = hypergeom.pmf(success_sample, population_size, success_population, sample_size)
        result_label.config(text=f"Probability: {prob * 100:.2f}%")
        
        plot_distribution(population_size, success_population, sample_size)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integer values.")

def plot_distribution(N, K, n):
    global canvas
    k_values = np.arange(1, min(n, K) + 1)
    probabilities = hypergeom.pmf(k_values, N, K, n)
    
    ax.clear()
    ax.bar(k_values, probabilities * 100, color='blue', alpha=0.6, edgecolor='black')
    ax.set_xlabel("Copies of wanted card in opening hand")
    ax.set_xticks(k_values)
    ax.set_xticklabels(k_values.astype(int))
    ax.set_ylabel("Probability (%)")
    ax.set_title("Hypergeometric Distribution")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    canvas.draw()

def clear_graph():
    entry_N.delete(0, tk.END)
    entry_K.delete(0, tk.END)
    entry_n.delete(0, tk.END)
    entry_k.delete(0, tk.END)
    ax.clear()
    ax.set_title("Hypergeometric Distribution")
    canvas.draw()
    result_label.config(text="Probability: ")

# GUI Setup
root = tk.Tk()

# Center the window on the screen
def center_window(window, width=600, height=600):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

center_window(root)

root.title("Card Game Hypergeometric Calculator")

# Input Fields
tk.Label(root, text="Cards in deck:", font=("Arial", 12)).grid(row=0, column=0)
entry_N = tk.Entry(root, font=("Arial", 12))
entry_N.grid(row=0, column=1)

tk.Label(root, text="Cards in opening hand:", font=("Arial", 12)).grid(row=1, column=0)
entry_K = tk.Entry(root, font=("Arial", 12))
entry_K.grid(row=1, column=1)

tk.Label(root, text="Copies of wanted card in deck:", font=("Arial", 12)).grid(row=2, column=0)
entry_n = tk.Entry(root, font=("Arial", 12))
entry_n.grid(row=2, column=1)

tk.Label(root, text="Copies of wanted card in opening hand:", font=("Arial", 12)).grid(row=3, column=0)
entry_k = tk.Entry(root, font=("Arial", 12))
entry_k.grid(row=3, column=1)

# Buttons
calc_button = tk.Button(root, text="Calculate", font=("Arial", 12), command=calculate_probability)
calc_button.grid(row=4, column=0, pady=10)

clear_button = tk.Button(root, text="Clear", font=("Arial", 12), command=clear_graph)
clear_button.grid(row=4, column=1, pady=10)

# Result Label
result_label = tk.Label(root, text="Probability: ", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=2)

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title("Hypergeometric Distribution")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=6, column=0, columnspan=2)

root.mainloop()