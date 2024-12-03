import json
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QHBoxLayout,
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


class ModernNotesApp(QWidget):
    def __init__(self, notes):
        super().__init__()
        self.notes = notes
        self.initUI()

    def initUI(self):
        # Set up main window
        self.setWindowTitle("Student Notes")
        self.setGeometry(100, 100, 600, 700)

        # Main layout
        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel("Bulletin UVSQ")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 15px;
            border-bottom: 2px solid #3498db;
        """
        )
        main_layout.addWidget(title_label)

        # Scroll area for notes
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(20, 20, 20, 20)

        # Populate notes
        for module, details in self.notes.items():
            module_frame = QFrame()
            module_frame.setStyleSheet(
                """
                QFrame {
                    background-color: #ecf0f1;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 10px;
                }
            """
            )

            module_layout = QVBoxLayout(module_frame)

            # Module name
            module_name = QLabel(module)
            module_name.setStyleSheet(
                """
                font-size: 18px;
                font-weight: bold;
                color: #2980b9;
                margin-bottom: 10px;
            """
            )
            module_layout.addWidget(module_name)

            # Evaluations
            evaluations = details.get("evaluations", [])
            for evaluation in evaluations:
                eval_layout = QHBoxLayout()

                description = evaluation.get("description", "No description")
                note = str(evaluation.get("note", {}).get("value", "N/A"))

                desc_label = QLabel(description)
                desc_label.setStyleSheet(
                    """
                    color: #34495e;
                    font-size: 14px;
                """
                )

                note_label = QLabel(note)
                note_label.setStyleSheet(
                    """
                    color: #2ecc71;
                    font-size: 16px;
                    font-weight: bold;
                """
                )

                eval_layout.addWidget(desc_label)
                eval_layout.addStretch()
                eval_layout.addWidget(note_label)

                module_layout.addLayout(eval_layout)

            scroll_layout.addWidget(module_frame)

        # Finalize scroll area
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: none;
            }
        """
        )

        main_layout.addWidget(scroll_area)

        # Set the main layout
        self.setLayout(main_layout)

        # Set application-wide style
        self.setStyleSheet(
            """
            QWidget {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """
        )


def read_notes(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

        notes = data.get("relevé", {}).get("ressources", {})
        return notes


def main():
    app = QApplication(sys.argv)

    try:
        notes = read_notes("data.json")
        window = ModernNotesApp(notes)
        window.show()
        sys.exit(app.exec_())
    except FileNotFoundError:
        print("Error: data.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in data.json")


# if __name__ == "__main__":
#     main()
