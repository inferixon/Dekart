# All comments in this file must be written in English only.
import sys
import random
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton,
                                 QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt
from PIL import Image

FONT_NAME = 'Palatino Linotype'
VERSION = '1.3.0'

letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ")

# Generates a random chart with letters placed on a grid
# Returns a dictionary of positions and the path to the saved chart image
def generate_random_chart():
    grid_range = range(-5, 6)
    all_coords = [(x, y) for x in grid_range for y in grid_range if (x != 0 and y != 0)]
    random.shuffle(all_coords)
    selected_coords = all_coords[:len(letters)]

    positions = dict(zip(letters, selected_coords))

    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-5.5, 5.5)
    ax.set_xticks(range(-5, 6))
    ax.set_yticks(range(-5, 6))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='both', length=0)

    axis_linewidth = 1
    ax.annotate('', xy=(5.5, 0), xytext=(-5.5, 0),
                arrowprops=dict(arrowstyle='->', color='black', linewidth=axis_linewidth))
    ax.annotate('', xy=(0, 5.5), xytext=(0, -5.5),
                arrowprops=dict(arrowstyle='->', color='black', linewidth=axis_linewidth))

    ax.text(5.2, -0.2, 'x', fontsize=22, fontstyle='italic', ha='center', va='center')
    ax.text(-0.2, 5.2, 'y', fontsize=22, fontstyle='italic', ha='center', va='center')

    for x in range(-5, 6):
        if x != 0:
            ax.text(x, 0.2, str(x), fontsize=14, ha='center', va='center', fontname=FONT_NAME)
    for y in range(-5, 6):
        if y != 0:
            ax.text(0.2, y, str(y), fontsize=14, ha='center', va='center', fontname=FONT_NAME)
    ax.text(0.2, 0.2, '0', fontsize=15, ha='center', va='center', fontname=FONT_NAME, fontweight='bold')

    tick_length = 0.18
    for x in range(-5, 6):
        if x != 0:
            ax.plot([x, x], [-tick_length/4, tick_length/4], color='black', linewidth=1)
    for y in range(-5, 6):
        if y != 0:
            ax.plot([-tick_length/4, tick_length/4], [y, y], color='black', linewidth=1)

    for letter, (x, y) in positions.items():
        ax.text(x, y, letter, fontsize=24, ha='center', va='center', fontname=FONT_NAME, fontweight='bold')

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.tight_layout()
    chart_path = "chart.png"
    plt.savefig(chart_path)
    plt.close()
    return positions, chart_path

# Main application window class
class DekartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"DEKART v{VERSION}")
        self.setFixedSize(1500, 900)  # increased by another 50px
        self.setStyleSheet("background: #fff;")

        self.letter_positions, self.chart_path = generate_random_chart()
        self.allowed_chars = set(self.letter_positions.keys())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Left side
        left_panel = QVBoxLayout()
        self.entry = QLineEdit()
        self.entry.setFont(QFont("Palatino", 24))
        self.entry.returnPressed.connect(self.on_submit)
        self.entry.setStyleSheet("background: #fff; color: #222; border-radius: 0; border: 1px solid #bbb; box-shadow: 0 2px 6px #eee, 0 1.5px 0 #fff inset;")
        self.entry.setValidator(None)  # Remove any previous validators
        self.entry.textChanged.connect(self.filter_norwegian_letters)
        left_panel.addWidget(self.entry)

        btn_row = QHBoxLayout()
        submit_btn = QPushButton("🆗")
        submit_btn.setFont(QFont("Palatino", 24))
        submit_btn.clicked.connect(self.on_submit)
        submit_btn.setStyleSheet("background: #f5f5f5; color: #222; border-radius: 0; border: 1px solid #bbb; min-width: 60px; min-height: 60px; box-shadow: 0 2px 6px #ddd, 0 1.5px 0 #fff inset;")
        btn_row.addWidget(submit_btn)

        regen_btn = QPushButton("🔄")
        regen_btn.setFont(QFont("Palatino", 24))
        regen_btn.clicked.connect(self.regenerate_chart)
        regen_btn.setStyleSheet("background: #f5f5f5; color: #222; border-radius: 0; border: 1px solid #bbb; min-width: 60px; min-height: 60px; box-shadow: 0 2px 6px #ddd, 0 1.5px 0 #fff inset;")
        btn_row.addWidget(regen_btn)

        left_panel.addLayout(btn_row)

        self.output_label = QLabel()
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setFont(QFont("Palatino", 34))
        self.output_label.setFixedSize(500, 700)
        self.output_label.setStyleSheet("background-color: #fff; color: #222; border: none; box-shadow: 0 2px 8px #eee, 0 1.5px 0 #fff inset;")
        left_panel.addWidget(self.output_label)

        main_layout.addLayout(left_panel)

        # Right side (image)
        self.image_label = QLabel()
        self.image_label.setStyleSheet("background: #fff; border: none; box-shadow: 0 2px 8px #eee, 0 1.5px 0 #fff inset;")
        main_layout.addWidget(self.image_label)

        self.update_image()
        self.entry.setFocus()

    # Updates the displayed image
    def update_image(self):
        image = Image.open(self.chart_path)
        orig_width, orig_height = image.size
        image = image.resize((int(orig_width * 0.9), int(orig_height * 0.9)), Image.LANCZOS)
        image.save("chart_resized.png")
        pixmap = QPixmap("chart_resized.png")
        self.image_label.setPixmap(pixmap)

    # Regenerates the chart and updates the image
    def regenerate_chart(self):
        self.letter_positions, self.chart_path = generate_random_chart()
        self.allowed_chars = set(self.letter_positions.keys())
        self.update_image()
        self.output_label.setText("")
        self.entry.clear()

    def filter_norwegian_letters(self, text):
        allowed = ''.join([c for c in text.upper() if c in self.letter_positions])
        if text != allowed:
            cursor_pos = self.entry.cursorPosition()
            self.entry.blockSignals(True)
            self.entry.setText(allowed)
            self.entry.setCursorPosition(cursor_pos - (len(text) - len(allowed)))
            self.entry.blockSignals(False)

    # Handles the submit action
    def on_submit(self):
        word = self.entry.text().upper()
        if not word:
            return
        coords = [f"{self.letter_positions[c][0]}, {self.letter_positions[c][1]}" for c in word]
        result = "\n".join(coords)
        self.output_label.setText(result)
        QApplication.clipboard().setText(result)
        self.entry.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DekartApp()
    window.show()
    sys.exit(app.exec())
