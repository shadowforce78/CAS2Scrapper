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
        self.setMinimumWidth(900)  # Augmentation de la largeur minimale

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Adjusted margins

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
        scroll_layout.setContentsMargins(10, 10, 10, 10)  # Adjusted margins

        # Populate notes
        for ue, details in self.notes.items():
            ue_frame = QFrame()
            ue_frame.setStyleSheet(
                """
                QFrame {
                    background-color: #ecf0f1;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 10px;
                }
            """
            )

            ue_layout = QVBoxLayout(ue_frame)
            ue_layout.setSpacing(8)

            # UE title
            ue_title = QLabel(details.get("titre", "No title"))
            ue_title.setWordWrap(True)
            ue_title.setStyleSheet(
                """
                font-size: 18px;
                font-weight: bold;
                color: #2980b9;
                margin-bottom: 10px;
            """
            )
            ue_layout.addWidget(ue_title)

            # Resources
            resources = details.get("ressources", {})
            for resource, res_details in resources.items():
                res_layout = QHBoxLayout()
                res_layout.setSpacing(15)
                
                titre = res_details.get("titre", "No title")
                res_name = QLabel(f"{resource} - {titre}")
                res_name.setWordWrap(True)
                res_name.setMinimumWidth(200)
                res_name.setMaximumWidth(600)
                res_name.setStyleSheet(
                    """
                    color: #34495e;
                    font-size: 14px;
                """
                )

                res_note = str(res_details.get("moyenne", "~"))

                note_label = QLabel(res_note)
                note_label.setStyleSheet(
                    """
                    color: #2ecc71;
                    font-size: 16px;
                    font-weight: bold;
                """
                )

                res_layout.addWidget(res_name, stretch=1)
                res_layout.addWidget(note_label, alignment=Qt.AlignRight)

                ue_layout.addLayout(res_layout)

            # SAEs
            saes = details.get("saes", {})
            for sae, sae_details in saes.items():
                sae_layout = QHBoxLayout()
                sae_layout.setSpacing(15)
                
                titre = sae_details.get("titre", "No title")
                sae_name = QLabel(f"{sae} - {titre}")
                sae_name.setWordWrap(True)
                sae_name.setMinimumWidth(200)
                sae_name.setMaximumWidth(600)
                sae_name.setStyleSheet(
                    """
                    color: #34495e;
                    font-size: 14px;
                """
                )

                sae_note = str(sae_details.get("moyenne", "~"))

                sae_note_label = QLabel(sae_note)
                sae_note_label.setStyleSheet(
                    """
                    color: #e74c3c;
                    font-size: 16px;
                    font-weight: bold;
                """
                )

                sae_layout.addWidget(sae_name, stretch=1)
                sae_layout.addWidget(sae_note_label, alignment=Qt.AlignRight)

                ue_layout.addLayout(sae_layout)

            scroll_layout.addWidget(ue_frame)

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
        releve = data.get("relevé", {})
        notes = releve.get("ues", {})
        ressources = releve.get("ressources", {})
        saes = releve.get("saes", {})

        # Créer un dictionnaire de correspondance pour les titres
        ressources_titres = {code: res["titre"] for code, res in ressources.items()}
        saes_titres = {code: sae["titre"] for code, sae in saes.items()}

        # Mettre à jour les titres dans les UEs
        for ue in notes.values():
            # Mise à jour des titres des ressources
            for code in ue.get("ressources", {}):
                if code in ressources_titres:
                    ue["ressources"][code]["titre"] = ressources_titres[code]

            # Mise à jour des titres des SAEs
            for code in ue.get("saes", {}):
                if code in saes_titres:
                    ue["saes"][code]["titre"] = saes_titres[code]

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