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
    QMenuBar,
    QStackedWidget,
    QMainWindow,
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Student Information")
        self.setMinimumWidth(900)

        # Create menu bar
        menubar = self.menuBar()
        view_menu = menubar.addMenu('View')
        
        # Create actions
        notes_action = view_menu.addAction('Notes')
        notes_action.triggered.connect(lambda: self.stack.setCurrentIndex(0))
        
        info_action = view_menu.addAction('Info')
        info_action.triggered.connect(lambda: self.stack.setCurrentIndex(1))
        
        absences_action = view_menu.addAction('Absences')
        absences_action.triggered.connect(lambda: self.stack.setCurrentIndex(2))

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create stacked widget
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Add pages to stack
        self.stack.addWidget(ModernNotesApp(self.data))  # Passer tout le dictionnaire data
        self.stack.addWidget(InfoWidget(self.data.get("auth", {})))
        self.stack.addWidget(AbsencesWidget(self.data.get("absences", {})))

class InfoWidget(QWidget):
    def __init__(self, info_data):
        super().__init__()
        layout = QVBoxLayout(self)
        
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        info_layout = QVBoxLayout(info_frame)
        
        for key, value in info_data.items():
            row = QHBoxLayout()
            key_label = QLabel(f"{key}:")
            key_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
            value_label = QLabel(str(value))
            value_label.setStyleSheet("color: #34495e;")
            
            row.addWidget(key_label)
            row.addWidget(value_label)
            row.addStretch()
            
            info_layout.addLayout(row)
        
        layout.addWidget(info_frame)
        layout.addStretch()

class AbsencesWidget(QWidget):
    def __init__(self, absences_data):
        super().__init__()
        layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll_layout = QVBoxLayout(content)

        # Sort dates
        sorted_dates = sorted(absences_data.keys())
        
        for date in sorted_dates:
            # Filtrer les absences pour ne garder que les absences et retards
            relevant_absences = [
                absence for absence in absences_data[date] 
                if absence['statut'] in ['absent', 'retard']
            ]
            
            # Ne créer le cadre que s'il y a des absences pertinentes
            if relevant_absences:
                date_frame = QFrame()
                date_frame.setStyleSheet("""
                    QFrame {
                        background-color: #ecf0f1;
                        border-radius: 10px;
                        padding: 15px;
                        margin-bottom: 10px;
                    }
                """)
                
                date_layout = QVBoxLayout(date_frame)
                
                date_label = QLabel(date)
                date_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
                date_layout.addWidget(date_label)
                
                
                for absence in relevant_absences:
                    absence_info = QLabel(
                        f"De {absence['debut']}h à {absence['fin']}h - "
                        f"Status: {absence['statut']} - "
                        f"Justifié: {'Oui' if absence['justifie'] else 'Non'} - "
                        f"Enseignant: {absence['enseignant']}"
                    )
                    # Colorer en rouge pour absent, orange pour retard
                    color = "#e74c3c" if absence['statut'] == 'absent' else "#f39c12"
                    absence_info.setStyleSheet(f"color: {color};")
                    date_layout.addWidget(absence_info)
                
                scroll_layout.addWidget(date_frame)
        
        scroll_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

class ModernNotesApp(QWidget):
    def __init__(self, notes):
        super().__init__()
        self.data = notes
        self.ressources = self.data.get("relevé", {}).get("ressources", {})
        self.notes = self.data.get("relevé", {}).get("ues", {})
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
            for resource_id, res_details in resources.items():
                res_layout = QHBoxLayout()
                res_layout.setSpacing(15)
                
                # Récupérer les détails de la ressource depuis le bon dictionnaire
                resource_info = self.ressources.get(resource_id, {})
                titre = resource_info.get("titre", "Sans titre")
                res_name = QLabel(f"{resource_id} - {titre}")
                res_name.setWordWrap(True)
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
        return json.load(file)

def main():
    app = QApplication(sys.argv)

    try:
        data = read_notes("data.json")
        window = MainWindow(data)
        window.show()
        sys.exit(app.exec_())
    except FileNotFoundError:
        print("Error: data.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in data.json")