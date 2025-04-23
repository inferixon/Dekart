# All comments in this file must be written in English only.
import sys
import random
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton,
                                 QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTabWidget)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt
from PIL import Image

FONT_NAME = 'Palatino Linotype'
VERSION = '1.3.1'

letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ")

# Generates a random chart with letters placed on a grid
# Returns a dictionary of positions and the path to the saved chart image
def generate_random_chart(size=900):
    grid_range = range(-5, 6)
    all_coords = [(x, y) for x in grid_range for y in grid_range if (x != 0 and y != 0)]
    random.shuffle(all_coords)
    selected_coords = all_coords[:len(letters)]

    positions = dict(zip(letters, selected_coords))

    fig, ax = plt.subplots(figsize=(size/100, size/100), dpi=100)
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
        self.setFixedSize(1500, 1000)
        self.setStyleSheet("background: #fff;")

        self.letter_positions, self.chart_path = generate_random_chart()
        self.allowed_chars = set(self.letter_positions.keys())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Add QTabWidget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { min-width: 120px; min-height: 40px; font-size: 18px; color: #000; font-family: '" + FONT_NAME + "'; } QTabBar::tab:selected { background: #e0e0e0; color: #000; font-family: '" + FONT_NAME + "'; } QTabWidget::pane { border: 1px solid #bbb; }")
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)
        main_layout.addWidget(self.tabs)

        # First tab: KodeGen
        self.tab_kodegen = QWidget()
        self.tabs.addTab(self.tab_kodegen, "KodeGen")
        kodegen_layout = QHBoxLayout()
        self.tab_kodegen.setLayout(kodegen_layout)

        # Move all previous main_layout content to kodegen_layout
        left_panel = QVBoxLayout()
        self.entry = QLineEdit()
        palatino_font = QFont(FONT_NAME, 24)
        self.entry.setFont(palatino_font)
        self.entry.returnPressed.connect(self.on_submit)
        self.entry.setStyleSheet("background: #fff; color: #000; border-radius: 0; border: 1px solid #bbb; box-shadow: 0 2px 6px #eee, 0 1.5px 0 #fff inset;")
        self.entry.setValidator(None)  # Remove any previous validators
        self.entry.textChanged.connect(self.filter_norwegian_letters)
        left_panel.addWidget(self.entry)

        btn_row = QHBoxLayout()
        submit_btn = QPushButton("🆗")
        submit_btn.setFont(QFont(FONT_NAME, 24))
        submit_btn.clicked.connect(self.on_submit)
        submit_btn.setStyleSheet("background: #f5f5f5; color: #000; border-radius: 0; border: 1px solid #bbb; min-width: 60px; min-height: 60px; box-shadow: 0 2px 6px #ddd, 0 1.5px 0 #fff inset;")
        btn_row.addWidget(submit_btn)

        regen_btn = QPushButton("🔄")
        regen_btn.setFont(QFont(FONT_NAME, 24))
        regen_btn.clicked.connect(self.regenerate_chart)
        regen_btn.setStyleSheet("background: #f5f5f5; color: #000; border-radius: 0; border: 1px solid #bbb; min-width: 60px; min-height: 60px; box-shadow: 0 2px 6px #ddd, 0 1.5px 0 #fff inset;")
        btn_row.addWidget(regen_btn)

        left_panel.addLayout(btn_row)

        self.output_label = QLabel()
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setFont(QFont(FONT_NAME, 34))
        self.output_label.setFixedSize(500, 700)
        self.output_label.setStyleSheet("background-color: #fff; color: #000; border: none; box-shadow: 0 2px 8px #eee, 0 1.5px 0 #fff inset;")
        left_panel.addWidget(self.output_label)

        kodegen_layout.addLayout(left_panel)

        self.image_label = QLabel()
        self.image_label.setStyleSheet("background: #fff; border: none; box-shadow: 0 2px 8px #eee, 0 1.5px 0 #fff inset;")
        kodegen_layout.addWidget(self.image_label)

        # Second tab: KodeSpill (Game)
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "KodeSpill")
        spill_layout = QHBoxLayout()
        self.tab2.setLayout(spill_layout)

        # --- KodeSpill intro widgets ---
        self.spill_intro_widget = QWidget()
        self.spill_intro_layout = QVBoxLayout()
        self.spill_intro_widget.setLayout(self.spill_intro_layout)
        self.spill_intro_label = QLabel("Skriv inn ordet\nsom er kryptert i koordinatene.\nDu har 7 forsøk. Lykke til!")
        self.spill_intro_label.setFont(QFont(FONT_NAME, 29))
        self.spill_intro_label.setStyleSheet("color: #000;")
        self.spill_intro_label.setAlignment(Qt.AlignCenter)
        self.spill_intro_layout.addStretch()
        self.spill_intro_layout.addWidget(self.spill_intro_label)
        self.spill_intro_start_btn = QPushButton("⭐️")
        self.spill_intro_start_btn.setFont(QFont(FONT_NAME, 43))
        self.spill_intro_start_btn.setStyleSheet("color: #000; background: #f5f5f5; border: 1px solid #bbb; min-width: 80px; min-height: 80px;")
        self.spill_intro_start_btn.clicked.connect(self.spill_start_game)
        self.spill_intro_start_btn.setDefault(True)
        self.spill_intro_start_btn.setAutoDefault(True)
        self.spill_intro_layout.addWidget(self.spill_intro_start_btn, alignment=Qt.AlignHCenter)
        self.spill_intro_layout.addStretch()
        # Add intro widget to layout, hide game widgets initially
        spill_layout.addWidget(self.spill_intro_widget, alignment=Qt.AlignCenter)

        self.spill_image_label = QLabel()
        self.spill_image_label.setStyleSheet("background: #fff; border: none;")
        self.spill_image_label.hide()

        # Left panel for game controls and results
        left_game_panel = QVBoxLayout()
        # Result label — centered, larger font, 100px lower
        self.spill_result_label = QLabel()
        self.spill_result_label.setFont(QFont(FONT_NAME, 40))
        self.spill_result_label.setText("")
        self.spill_result_label.setStyleSheet("color: #000;")
        self.spill_result_label.setAlignment(Qt.AlignCenter)
        left_game_panel.addSpacing(100)
        left_game_panel.addWidget(self.spill_result_label, alignment=Qt.AlignCenter)

        # Textbox — shorter, centered, 150px higher
        self.spill_entry = QLineEdit()
        self.spill_entry.setFont(QFont(FONT_NAME, 32))
        self.spill_entry.setStyleSheet("background: #fff; color: #000; border-radius: 0; border: 1px solid #bbb;")
        self.spill_entry.setFixedWidth(300)
        self.spill_entry.setAlignment(Qt.AlignCenter)
        self.spill_entry.returnPressed.connect(self.spill_check_answer)
        self.spill_entry.setEnabled(False)
        self.spill_entry.textChanged.connect(self.filter_norwegian_letters_spill)

        # Cipher label above textbox, with 20px spacing above
        self.spill_task_label = QLabel()
        self.spill_task_label.setAlignment(Qt.AlignCenter)
        self.spill_task_label.setFont(QFont(FONT_NAME, 34))
        self.spill_task_label.setFixedSize(500, 700)
        self.spill_task_label.setStyleSheet("background-color: #fff; color: #000; border: none;")
        left_game_panel.addSpacing(30)
        left_game_panel.addWidget(self.spill_entry, alignment=Qt.AlignCenter)
        left_game_panel.addSpacing(30)
        left_game_panel.addWidget(self.spill_task_label, alignment=Qt.AlignCenter)

        self.spill_start_btn = QPushButton("START")
        self.spill_start_btn.setFont(QFont(FONT_NAME, 22))
        self.spill_start_btn.setStyleSheet("color: #000; background: #f5f5f5; border: 1px solid #bbb;")
        self.spill_start_btn.clicked.connect(self.spill_start_game)
        self.spill_start_btn.setDefault(True)
        self.spill_start_btn.setAutoDefault(True)
        left_game_panel.addWidget(self.spill_start_btn)

        spill_layout.addLayout(left_game_panel)

        # Right panel for chart (KodeSpill)
        right_game_panel = QVBoxLayout()
        right_game_panel.addStretch(1)
        right_game_panel.addWidget(self.spill_image_label, alignment=Qt.AlignCenter)
        right_game_panel.addStretch(1)
        spill_layout.addLayout(right_game_panel)

        self.tabs.currentChanged.connect(self.on_tab_changed)

        # Game state
        self.spill_words = []
        self.spill_current_word = ""
        self.spill_current_coords = ""
        self.spill_round = 0
        self.spill_results = []
        self.spill_total_rounds = 7

        palatino_font_24 = QFont(FONT_NAME, 24)
        palatino_font_22 = QFont(FONT_NAME, 22)
        palatino_font_29 = QFont(FONT_NAME, 29)
        palatino_font_32 = QFont(FONT_NAME, 32)
        palatino_font_40 = QFont(FONT_NAME, 40)
        palatino_font_12 = QFont(FONT_NAME, 12)
        # KodeGen tab
        self.entry.setFont(palatino_font_24)
        self.output_label.setFont(palatino_font_32)
        submit_btn.setFont(palatino_font_24)
        regen_btn.setFont(palatino_font_24)
        self.image_label.setFont(palatino_font_12)
        # KodeSpill tab
        self.spill_result_label.setFont(palatino_font_32)
        self.spill_task_label.setFont(palatino_font_32)
        self.spill_entry.setFont(palatino_font_32)
        self.spill_start_btn.setFont(palatino_font_22)
        self.spill_image_label.setFont(palatino_font_12)
        self.spill_intro_label.setFont(palatino_font_29)
        self.spill_intro_start_btn.setFont(palatino_font_40)

        self.update_image()
        self.entry.setFocus()

    # Updates the displayed image
    def update_image(self):
        self.letter_positions, self.chart_path = generate_random_chart(size=900)
        pixmap = QPixmap(self.chart_path)
        self.image_label.setPixmap(pixmap)

    # Regenerates the chart and updates the image
    def regenerate_chart(self):
        self.letter_positions, self.chart_path = generate_random_chart()
        self.allowed_chars = set(self.letter_positions.keys())
        self.update_image()
        self.output_label.setText("")
        self.entry.clear()
        self.entry.setFocus()

    def filter_norwegian_letters(self, text):
        allowed = ''.join([c for c in text.upper() if c in self.letter_positions])
        if text != allowed:
            cursor_pos = self.entry.cursorPosition()
            self.entry.blockSignals(True)
            self.entry.setText(allowed)
            self.entry.setCursorPosition(cursor_pos - (len(text) - len(allowed)))
            self.entry.blockSignals(False)

    def filter_norwegian_letters_spill(self, text):
        allowed = ''.join([c for c in text.upper() if c in self.letter_positions])
        if text != allowed:
            cursor_pos = self.spill_entry.cursorPosition()
            self.spill_entry.blockSignals(True)
            self.spill_entry.setText(allowed)
            self.spill_entry.setCursorPosition(cursor_pos - (len(text) - len(allowed)))
            self.spill_entry.blockSignals(False)

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

    def on_tab_changed(self, idx):
        if self.tabs.tabText(idx) == "KodeSpill":
            # Show intro, hide game widgets
            self.spill_intro_label.setText("Skriv inn ordet\nsom er kryptert i koordinatene.\nDu har 7 forsøk. Lykke til!")
            self.spill_intro_widget.show()
            self.spill_intro_label.show()
            self.spill_intro_start_btn.show()
            self.spill_result_label.hide()
            self.spill_task_label.hide()
            self.spill_entry.hide()
            self.spill_start_btn.hide()
            self.spill_image_label.hide()
            self.spill_result_label.setText("")
            self.spill_task_label.setText("")
            self.spill_entry.clear()
            self.spill_entry.setEnabled(False)
            self.spill_start_btn.setEnabled(True)
            self.spill_image_label.clear()
            self.spill_words = []
            self.spill_current_word = ""
            self.spill_current_coords = ""
            self.spill_round = 0
            self.spill_results = []

    def spill_start_game(self):
        self.spill_intro_widget.hide()
        self.spill_result_label.show()
        self.spill_task_label.show()
        self.spill_entry.show()
        self.spill_start_btn.hide()
        self.spill_image_label.show()
        # Load words from ord.txt
        try:
            with open("ord.txt", encoding="utf-8") as f:
                words = [w.strip().upper() for w in f if w.strip()]
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить ord.txt: {e}")
            return
        if len(words) < self.spill_total_rounds:
            QMessageBox.critical(self, "Ошибка", f"В ord.txt должно быть не менее {self.spill_total_rounds} слов.")
            return
        self.spill_words = random.sample(words, self.spill_total_rounds)
        self.spill_result_label.setText("")
        self.spill_results = []
        self.spill_round = 0
        self.spill_start_btn.setEnabled(False)
        self.spill_entry.setEnabled(True)
        self.spill_entry.clear()
        self.spill_entry.setFocus()
        self.spill_next_round()

    def spill_next_round(self):
        if self.spill_round >= self.spill_total_rounds:
            # Game over
            score = self.spill_results.count('✅')
            self.spill_result_label.hide()
            self.spill_task_label.hide()
            self.spill_entry.hide()
            self.spill_image_label.hide()
            self.spill_intro_label.setText(f"Resultat: {score}/{self.spill_total_rounds}\n{' '.join(self.spill_results)}")
            self.spill_intro_label.show()
            self.spill_intro_start_btn.show()
            self.spill_intro_widget.show()
            return
        # Generate new chart and update image
        self.letter_positions, self.chart_path = generate_random_chart()
        self.update_spill_image()
        word = self.spill_words[self.spill_round]
        self.spill_current_word = word
        coords = [f"{self.letter_positions[c][0]}, {self.letter_positions[c][1]}" for c in word]
        self.spill_current_coords = '\n'.join(coords)
        self.spill_task_label.setText(self.spill_current_coords)
        self.spill_entry.clear()
        self.spill_entry.setFocus()

    def update_spill_image(self):
        self.letter_positions, self.chart_path = generate_random_chart(size=900)
        pixmap = QPixmap(self.chart_path)
        self.spill_image_label.setPixmap(pixmap)

    def spill_check_answer(self):
        answer = self.spill_entry.text().strip().upper()
        correct = answer == self.spill_current_word
        self.spill_results.append('✅' if correct else '❌')
        self.spill_result_label.setText(' '.join(self.spill_results))
        self.spill_round += 1
        self.spill_next_round()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DekartApp()
    window.show()
    sys.exit(app.exec())
