# All comments in this file must be written in English only.
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import random
import os

#CONFIG
FONT_NAME = 'Palatino Linotype'
VERSION = '1.3.0'

# Norwegian alphabet with extended letters
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ")

# Generate dynamic coordinates and chart
def generate_random_chart():
    grid_range = range(-5, 6)
    all_coords = [(x, y) for x in grid_range for y in grid_range if (x != 0 and y != 0)]
    random.shuffle(all_coords)
    selected_coords = all_coords[:len(letters)]

    positions = dict(zip(letters, selected_coords))

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-5.5, 5.5)
    ax.set_xticks(range(-5, 6))
    ax.set_yticks(range(-5, 6))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Hide tick marks
    ax.tick_params(axis='both', which='both', length=0)

    # Draw axes with arrowheads, both 1px thick
    axis_linewidth = 1
    ax.annotate(
        '', xy=(5.5, 0), xytext=(-5.5, 0),
        arrowprops=dict(arrowstyle='->', color='black', linewidth=axis_linewidth)
    )
    ax.annotate(
        '', xy=(0, 5.5), xytext=(0, -5.5),
        arrowprops=dict(arrowstyle='->', color='black', linewidth=axis_linewidth)
    )

    # Axis labels (large, italic, near axes)
    ax.text(5.2, -0.2, 'x', fontsize=22, fontstyle='italic', ha='center', va='center')
    ax.text(-0.2, 5.2, 'y', fontsize=22, fontstyle='italic', ha='center', va='center')

    # Place coordinate labels along axes
    for x in range(-5, 6):
        if x != 0:
            ax.text(x, 0.2, str(x), fontsize=14, ha='center', va='center', fontname=FONT_NAME)
    for y in range(-5, 6):
        if y != 0:
            ax.text(0.2, y, str(y), fontsize=14, ha='center', va='center', fontname=FONT_NAME)
    ax.text(0.2, 0.2, '0', fontsize=15, ha='center', va='center', fontname=FONT_NAME, fontweight='bold')

    # Draw ticks near numbers along axes
    tick_length = 0.18
    for x in range(-5, 6):
        if x != 0:
            ax.plot([x, x], [-tick_length/4, tick_length/4], color='black', linewidth=1)
    for y in range(-5, 6):
        if y != 0:
            ax.plot([-tick_length/4, tick_length/4], [y, y], color='black', linewidth=1)

    # Plot letters
    for letter, (x, y) in positions.items():
        ax.text(x, y, letter, fontsize=24, ha='center', va='center', fontname=FONT_NAME, fontweight='bold')


    ax.set_xticklabels([])
    ax.set_yticklabels([])

    plt.tight_layout()
    chart_path = "chart.png"
    plt.savefig(chart_path)
    plt.close()
    return positions, chart_path

# Generate chart and get new positions
global letter_positions
letter_positions, chart_path = generate_random_chart()

allowed_chars = set(letter_positions.keys())

def on_submit(event=None):
    word = entry.get().upper()
    if not all(char in letter_positions for char in word):
        messagebox.showerror("Error", "Only Norwegian letters A–Z + Æ Ø Å are allowed")
        return
    coords = [f"{letter_positions[c][0]}, {letter_positions[c][1]}" for c in word]
    result = "\n".join(coords)
    output_var.set(result)
    root.clipboard_clear()
    root.clipboard_append(result)
    entry.delete(0, tk.END)

def validate_input(P):
    return all(char.upper() in allowed_chars or char == "" for char in P)

root = tk.Tk()
root.title("DEKART v" + VERSION)
root.resizable(False, False)

def force_focus(event=None):
    root.after(100, root.focus_force)

root.after(200, root.focus_force)           # Focus on start
root.bind("<FocusOut>", force_focus)        # Focus on lost

window_width = 1300
window_height = 900
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coord = (screen_width // 2) - (window_width // 2)
y_coord = (screen_height // 2) - (window_height // 2) - 50
root.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

root.bind("<FocusIn>", lambda event: entry.focus_set())

main_frame = tk.Frame(root)
main_frame.pack(side=tk.LEFT, padx=10, pady=10)

vcmd = (root.register(validate_input), '%P')
entry = tk.Entry(main_frame, font=('Palatino', 24), validate="key", validatecommand=vcmd)
entry.pack(pady=10)
entry.bind('<Return>', on_submit)

def regenerate_chart():
    global letter_positions, chart_path, photo
    letter_positions, chart_path = generate_random_chart()
    allowed_chars.clear()
    allowed_chars.update(letter_positions.keys())
    # Update the image
    image = Image.open(chart_path)
    orig_width, orig_height = image.size
    image = image.resize((int(orig_width * 0.9), int(orig_height * 0.9)), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo
    output_var.set("")
    entry.delete(0, tk.END)

button_frame = tk.Frame(main_frame)
button_frame.pack(pady=5)

submit_button = tk.Button(button_frame, text="🆗", command=on_submit, font=('Palatino', 24))
submit_button.pack(side=tk.LEFT, padx=(0, 10))

regen_button = tk.Button(button_frame, text="🔄", command=regenerate_chart, font=('Palatino', 24))
regen_button.pack(side=tk.LEFT)

output_var = tk.StringVar()
output_label = tk.Label(main_frame, textvariable=output_var, font=('Palatino', 34), width=14, height=20,
                        justify="center", anchor="center", bg=root.cget("bg"))
output_label.pack(pady=10)
output_label.bind("<Button-1>", lambda e: root.clipboard_append(output_var.get()))

# Load and display generated chart
image = Image.open(chart_path)
orig_width, orig_height = image.size
image = image.resize((int(orig_width * 0.9), int(orig_height * 0.9)), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.image = photo
image_label.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()

# Cleanup chart if needed (optional)
# os.remove(chart_path)
