import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

def read_notes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        notes = data.get('relevé', {}).get('ressources', {})
        return notes

def display_notes(notes):
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    for module, details in notes.items():
        module_label = QLabel(f"Module: {module}")
        layout.addWidget(module_label)
        evaluations = details.get('evaluations', [])
        for evaluation in evaluations:
            note = evaluation.get('note', {}).get('value', 'N/A')
            description = evaluation.get('description', 'No description')
            evaluation_label = QLabel(f"  - {description}: {note}")
            layout.addWidget(evaluation_label)

    window.setLayout(layout)
    window.setWindowTitle('Notes')
    window.show()
    app.exec_()

if __name__ == "__main__":
    notes = read_notes('data.json')
    display_notes(notes)
